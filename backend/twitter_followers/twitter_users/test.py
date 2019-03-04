from django.test import TestCase
from twitter_users.models import TwitterUser, SecondLineFollowersCounter
from twitter_users.api.serializers import SecondLineFollowersSerializer


test_data_user = {"screen_name": "test", "user_id": 5, "followers_ids": [1, 2, 3]}
test_data_second_line = {"screen_name": "test", "user_id": 5, "followers": {"test": 4}}


class TwitterUserTestCase(TestCase):
    def setUp(self):
        self.user = TwitterUser.objects.create(**test_data_user)

    def test_created(self):
        self.assertEqual(TwitterUser.objects.all().count(), 1)

    def test_user_data(self):
        self.assertEqual(self.user.screen_name, test_data_user.get("screen_name"))
        self.assertEqual(self.user.user_id, test_data_user.get("user_id"))
        self.assertEqual(self.user.followers_ids, test_data_user.get("followers_ids"))

    def test_user_data_types(self):
        self.assertTrue(type(self.user.screen_name) == str)
        self.assertTrue(type(self.user.user_id) == int)
        self.assertTrue(type(self.user.followers_ids) == list)


class SecondLineFollowersCounterTestCase(TestCase):
    def setUp(self):
        self.second_followers = SecondLineFollowersCounter.objects.create(
            **test_data_second_line
        )

    def test_created(self):
        self.assertEqual(SecondLineFollowersCounter.objects.all().count(), 1)

    def test_user_data(self):
        self.assertEqual(
            self.second_followers.screen_name, test_data_second_line.get("screen_name")
        )
        self.assertEqual(
            self.second_followers.user_id, test_data_second_line.get("user_id")
        )
        self.assertEqual(
            self.second_followers.followers, test_data_second_line.get("followers")
        )

    def test_user_data_types(self):
        self.assertTrue(type(self.second_followers.screen_name) == str)
        self.assertTrue(type(self.second_followers.user_id) == int)
        self.assertTrue(type(self.second_followers.followers) == dict)


class FollowersEndpointTestCase(TestCase):
    def setUp(self):
        self.second_followers = SecondLineFollowersCounter.objects.create(
            **test_data_second_line
        )

    def test_endpoint_response_type_empty(self):
        response = self.client.get("/followers/get_followers/test2/")
        self.assertTrue(isinstance(response.data, dict))

    def test_endpoint_response_with_data(self):
        response = self.client.get(
            f'/followers/get_followers/{test_data_second_line.get("screen_name")}/'
        )
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(
            response.data.get("followers"), test_data_second_line.get("followers")
        )

    def test_serializer(self):
        serializer = SecondLineFollowersSerializer(self.second_followers)

        self.assertEqual(serializer.data, {"followers": {"test": 4}})
