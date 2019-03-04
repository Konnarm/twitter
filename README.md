# Twitter

##Purpose

App is designed to show counter of users that follow users following specific user.
Users that are following inputed user are omitted, aswell as user that was inputed.
Data for counter aswell as user data are preserved in database, and is only updated if certain time period passed since last update.

Frontend part should be updated in real time via Pusher service everytime twitter rate limit is hit or after whole data has been fetched.


###How to run for development purposes
* Create .env file in same folder as settings.py
This file should look like this:
TWITTER_API_KEY=your_twitter_credentials
TWITTER_API_SECRET=your_twitter_credentials
TWITTER_ACCESS_TOKEN=your_twitter_credentials
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_credentials
SECRET_KEY=secret_key
DATABASE_URL=format for postgres - postgres://user:pass@ip:port/db_name
DEBUG=True or False
REDIS_URL=eg. redis://localhost:6379
ALLOWED_HOSTS=0.0.0.0,localhost
PUSHER_APP_ID=pusher_credentials
PUSHER_KEY=pusher_credentials
PUSHER_SECRET=pusher_credentials
PUSHER_CLUSTER=eu

* Create .env file in frontend main dir
This file should contain
REACT_APP_PUSHER_API_KEY=pusher_api_key

* Install requirements to your environment "pip install -r requirements.txt" in same folder as manage.py is
run    "./manage.py runserver" in same folder as manage.py is
run    "celery -A twitter_followers worker -B" in same folder as manage.py is
then   "npm install" in frontend dir
then   "npm start" in frontend dir

* Run tests by "./manage.py" test or with coverage "coverage run --source='.' manage.py test"
Then check coverage with "coverage report"

* After passing tests deploy to Heroku is automatic via travis


##Things to do:
* Frontend UI and UX
* Implement automatic frontend app deployment to amazon S3 so there won't be need to do crazy things with package.json in main project dir(due to heroku)
* Make proper custom webpack configuration
* Make frontend index html part of backend structure with static react js from S3
* Make frontend tests
* More backend tests
* Probably better celery config
* Better documentation, including sphinx, maybe with typings
* Probably some refactoring including handling more edge cases
* Add logging
* Add pre-commit hook for black and flake8
