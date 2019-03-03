from twitter_followers.celery import app
from twitter_users.helpers import HandleTwitter


@app.task
def get_second_line_followers_task(handle, followers_slice):
    HandleTwitter(handle, followers_slice).get_second_line_followers()
