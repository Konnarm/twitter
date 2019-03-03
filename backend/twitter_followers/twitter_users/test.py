from django.test import TestCase
from twitter_users.models import TwitterUser


class TwitterUserTestCase(TestCase):
    def setUp(self):
        TwitterUser.objects.create(screen_name="test", user_id=5, followers_ids=[1,2,3])

    def test_created(self):
        self.assertEqual(TwitterUser.objects.all().count(), 1)
