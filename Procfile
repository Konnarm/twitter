release: cd backend/twitter_followers && python manage.py migrate
web: cd backend/twitter_followers && gunicorn twitter_followers.wsgi
worker: cd backend/twitter_followers && celery -A twitter_followers worker -B

