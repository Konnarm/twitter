import math
import signal
from _datetime import timedelta
from collections import Counter

import twitter
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import TwitterUser, SecondLineFollowersCounter


class CustomTwitterApi(twitter.Api):
    pass
    # TODO: timer should be set on every twitter request so it updates followers if rate limit reached,
    #  but it is not working somehow
    # def _RequestUrl(self, url, verb, data=None, json=None, enforce_auth=True):
    #     signal.setitimer(signal.ITIMER_VIRTUAL, 15)
    #     return super()._RequestUrl(url, verb, data=None, json=None, enforce_auth=True)


class HandleTwitter:
    """
    Class to handle user name request.
    """

    def __init__(self, handle, followers_slice):
        self.handle = handle
        self.followers_slice = followers_slice
        self.user = None
        self.second_line_followers = None
        self.api = CustomTwitterApi(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            sleep_on_rate_limit=True,
        )
        self.counter = Counter()
        signal.signal(signal.SIGALRM, self.process_followers)

    def get_second_line_followers(self):
        """
        Checks rate limits, then creates user for inputed username and starts to fetch followers.
        :return: None
        """

        self.api.InitializeRateLimit()

        self.user = self.create_or_update_single_user({"screen_name": self.handle})

        self.second_line_followers, created = SecondLineFollowersCounter.objects.update_or_create(
            screen_name=self.user.screen_name, defaults={"user_id": self.user.user_id}
        )

        self.get_lookup_bulk(
            self.user.followers_ids[: self.followers_slice]
            if self.followers_slice
            else self.user.followers_ids
        )
        self.process_followers()

    def create_or_update_single_user(
        self, twitter_data: dict, get_followers: bool = True
    ):
        """
        Gets user data from twitter by username or user id.
        Data includes followers list(ids) and username and/or user id
        :return: (:class:`TwitterUser`)
        """
        signal.setitimer(signal.ITIMER_REAL, 15)

        print(twitter_data.get("screen_name"), " ", twitter_data.get("user_id"))
        user_id = twitter_data.get("user_id")
        if user_id:
            try:
                user, created = TwitterUser.objects.update_or_create(
                    user_id=user_id, defaults=twitter_data
                )
            except IntegrityError:
                user, created = TwitterUser.objects.update_or_create(
                    screen_name=twitter_data.get("screen_name"), defaults=twitter_data
                )
        else:
            user, created = TwitterUser.objects.update_or_create(
                screen_name=twitter_data.get("screen_name"), defaults=twitter_data
            )

        if created or (not user.user_id or not user.screen_name):
            data = self.api.GetUser(**twitter_data)
            user.twitter_id = data.id
            user.twitter_handle = data.screen_name
        if (
            (user.modified < timezone.now() - timedelta(days=1))
            or created
            or (not user.followers_ids and get_followers)
        ):
            result = []
            cursor = -1
            while True:
                try:
                    next_cursor, prev_cursor, data = self.api.GetFollowerIDsPaged(
                        screen_name=user.screen_name, cursor=cursor
                    )
                    result.extend([x for x in data])

                    if next_cursor == 0 or next_cursor == prev_cursor:
                        break
                    else:
                        cursor = next_cursor
                except twitter.TwitterError:
                    break
            user.followers_ids = result
        user.save()
        return user

    def get_lookup_bulk(self, ids):
        """
        Gets basic user informations(username) from twitter or DB by id list.
        Processes user data further to get followers.
        :param ids:
        :return:
        """
        if ids:
            for part in range(math.ceil(len(ids) / 100)):
                signal.setitimer(signal.ITIMER_REAL, 15)
                users = self.api.UsersLookup(ids[100 * part : 100 * (part + 1)])
                for user in users:
                    populated_user = self.create_or_update_single_user(
                        {"screen_name": user.screen_name, "user_id": user.id}
                    )
                    self.fetch_users_names_and_add_to_counter(
                        populated_user.followers_ids
                    )

    def fetch_users_names_and_add_to_counter(self, ids):
        """
        Gets basic user informations(username) from twitter or DB by id list.
        Then adds them to counter to calculate second line followers.
        :param ids:
        :return: None
        """
        if ids:
            for part in range(math.ceil(len(ids) / 100)):
                signal.setitimer(signal.ITIMER_REAL, 15)
                users = self.api.UsersLookup(ids[100 * part : 100 * (part + 1)])
                for user in users:
                    populated_user = self.create_or_update_single_user(
                        {"screen_name": user.screen_name, "user_id": user.id},
                        get_followers=False,
                    )
                    if (
                        populated_user.id not in self.user.followers_ids
                        and populated_user.id != self.user.id
                        and populated_user.screen_name != self.user.screen_name
                    ):
                        self.counter += Counter([populated_user.screen_name])

    def process_followers(self, *args):
        """
        Updates second line followers model in DB plus on frontend via post save signal that send message on websocket
        """
        counted = dict(self.counter)
        if self.second_line_followers:
            self.second_line_followers.followers = counted
            self.second_line_followers.save()
