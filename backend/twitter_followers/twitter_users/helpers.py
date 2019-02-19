import math
from _datetime import timedelta
from collections import Counter

import twitter
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import TwitterUser, SecondLineFollowersCounter




def get_second_line_followers(handle, followers_slice):
    api = twitter.Api(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token_key=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
        sleep_on_rate_limit=True,
    )
    api.InitializeRateLimit()

    user = check_or_update_single_user({"screen_name": handle}, api)

    counted = get_lookup_bulk(
        user.followers_ids[:followers_slice] if followers_slice else user.followers_ids, api
    )
    print(user.screen_name, user.user_id)
    second, created = SecondLineFollowersCounter.objects.update_or_create(
        screen_name=user.screen_name, defaults={'user_id': user.user_id}
    )
    second_line_dict = {}
    counted_users = TwitterUser.objects.filter(user_id__in=counted.keys())
    for counted_user in counted_users:
        second_line_dict[counted_user.screen_name] = counted.pop(
            counted_user.user_id, 0
        )

    lookuped_users = get_user_lookups(list(counted.keys()), api)
    for user in lookuped_users:
        second_line_dict[user.screen_name] = counted.get(user.user_id, 0)

    second.followers = second_line_dict
    second.save()
    return second


def check_or_update_single_user(twitter_data, api, get_followers=True):
    print(twitter_data.get("screen_name"), " ", twitter_data.get("user_id"))

    user, created = TwitterUser.objects.update_or_create(screen_name=twitter_data.get('screen_name'), defaults=twitter_data)

    if created or (not user.user_id or not user.screen_name):
        data = api.GetUser(**twitter_data)
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
                next_cursor, prev_cursor, data = api.GetFollowerIDsPaged(
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


def get_lookup_bulk(ids, api):
    populated_users = []
    counter = Counter()

    if ids:
        for part in range(math.ceil(len(ids) / 100)):
            users = api.UsersLookup(ids[100 * part:100 * (part + 1)])
            for user in users:
                populated_user = check_or_update_single_user(
                    {"screen_name": user.screen_name, "user_id": user.id}, api
                )
                populated_users.append(populated_user)
        for u in populated_users:
            counter += Counter(u.followers_ids)

    return dict(counter)


def get_user_lookups(ids, api):
    populated_users = []

    if ids:
        for part in range(math.ceil(len(ids) / 100)):
            users = api.UsersLookup(ids[100 * part:100 * (part + 1)])
            for user in users:
                populated_user = check_or_update_single_user(
                    {"screen_name": user.screen_name, "user_id": user.id}, api,
                    get_followers=False
                )
                populated_users.append(populated_user)
    return populated_users
