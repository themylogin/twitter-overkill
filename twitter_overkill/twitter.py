from datetime import datetime, timedelta
import logging
import twitter

from twitter_overkill.app import app
from twitter_overkill.celery import celery
from twitter_overkill.db import db
from twitter_overkill.models import Tweet, TweetState
from twitter_overkill.twitter_text import get_tweet_length

logger = logging.getLogger(__name__)


@celery.task(acks_late=True, bind=True, max_retries=None)
def post_tweet(self, id, auth, tweet_variants):
    try:
        db_tweet = db.session.query(Tweet).get(id)

        if db_tweet is None:
            db_tweet = Tweet()
            db_tweet.id = id
            db_tweet.created_at = datetime.utcnow()
            db.session.add(db_tweet)

        db_tweet.auth = auth
        db_tweet.tweet_variants = tweet_variants

        db_tweet.tweet = choose_tweet_variant(tweet_variants)
        if db_tweet.tweet is None:
            db_tweet.tweet = cut_tweet(tweet_variants[0])

        if_error_repeat_after = 60
        try:
            try:
                api = twitter.Api(**auth)

                db_tweet.user = api.VerifyCredentials().screen_name

                db_tweet.state = TweetState.POSTED
                db_tweet.state_data = str(api.PostUpdate(db_tweet.tweet).id)

            except twitter.TwitterError as e:
                if e.args[0][0]["code"] in [
                    32,     # Could not authenticate you
                    89,     # Invalid or expired token
                    186,    # Status is over 140 characters
                    187,    # Status is a duplicate.
                ]:
                    db_tweet.state = TweetState.PERMANENT_ERROR
                    db_tweet.state_data = repr(e)
                else:
                    if e.args[0][0]["code"] == 88: # Rate limit exceeded
                        if_error_repeat_after = 900

                    raise

        except Exception as e:
            db_tweet.state = TweetState.TEMPORARY_ERROR
            db_tweet.state_data = repr(e)

        db_tweet.updated_at = datetime.utcnow()
        db.session.commit()

        if db_tweet.state == TweetState.TEMPORARY_ERROR:
            post_tweet.apply_async((id, auth, tweet_variants), countdown=if_error_repeat_after)

    except Exception:
        logger.error("post_tweet failed", exc_info=True)
        raise self.retry(countdown=5)


def choose_tweet_variant(tweet_variants):
    for variant in tweet_variants:
        if tweet_length(variant) <= 140:
            return variant


def cut_tweet(tweet):
    # TODO: Do not break hashtags, urls, etc

    if tweet_length(tweet) <= 140:
        return tweet

    while tweet_length(tweet + "…") > 140:
        tweet = tweet[:-1]

    return tweet + "…"


def tweet_length(tweet):
    return get_tweet_length(tweet, get_help_configuration())


help_configuration = {"updated_at": datetime.min}


def get_help_configuration():
    if datetime.utcnow() - help_configuration["updated_at"] > timedelta(days=1):
        api = twitter.Api(app.config["TWITTER_CONSUMER_KEY"],
                          app.config["TWITTER_CONSUMER_SECRET"],
                          app.config["TWITTER_ACCESS_TOKEN_KEY"],
                          app.config["TWITTER_ACCESS_TOKEN_SECRET"])
        help_configuration["configuration"] = api.GetHelpConfiguration()
        help_configuration["updated_at"] = datetime.utcnow()

    return help_configuration["configuration"]
