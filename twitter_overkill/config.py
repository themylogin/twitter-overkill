import os

CELERY_BROKER_URL = "amqp://rabbitmq"

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://twitter_overkill:twitter_overkill@postgres/twitter_overkill"

TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN_KEY = os.environ["TWITTER_ACCESS_TOKEN_KEY"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
