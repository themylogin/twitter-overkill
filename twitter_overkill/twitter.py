# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import twitter

from twitter_overkill.celery import celery
from twitter_overkill.config import config
import twitter_overkill.db as db
from twitter_overkill.twitter_text import get_tweet_length

@celery.task
def post_tweet(auth_list, tweet_variants, db_id=None):
    with db.get_connection() as connection:
        api = twitter.Api(*auth_list)

        db_tweet = None
        if db_id is not None:
            db_tweet = db.get_tweet(connection, db_id)

        if db_tweet is None:
            db_tweet = db.Tweet()
            db_tweet.created_at = datetime.now()

        db_tweet.auth_list = auth_list
        db_tweet.tweet_variants = tweet_variants

        if_error_repeat_after = 60
        try:
            try:
                db_tweet.user = api.VerifyCredentials().screen_name

                db_tweet.tweet = choose_tweet_variant(tweet_variants)
                if db_tweet.tweet is None:
                    db_tweet.tweet = cut_tweet(tweet_variants[0])

                db_tweet.state = "posted"
                db_tweet.state_data = str(api.PostUpdate(db_tweet.tweet).id)

            except twitter.TwitterError as e:
                if e.args[0][0]["code"] in [
                    32,     # Could not authenticate you
                    89,     # Invalid or expired token
                    186,    # Status is over 140 characters
                    187,    # Status is a duplicate.
                ]:
                    db_tweet.state = "permanent-error"
                    db_tweet.state_data = repr(e)
                else:
                    if e.args[0][0]["code"] == 88: # Rate limit exceeded
                        if_error_repeat_after = 900

                    raise

        except Exception as e:
            db_tweet.state = "temporary-error"
            db_tweet.state_data = repr(e)

        db_tweet.updated_at = datetime.now()
        db.update_tweet(connection, db_tweet)

        if db_tweet.state == "temporary-error":
            post_tweet.apply_async((auth_list, tweet_variants, db_tweet.id), countdown=if_error_repeat_after)


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
    if datetime.now() - help_configuration["updated_at"] > timedelta(days=1):
        help_configuration["configuration"] = twitter.Api(config["consumer_key"],
                                                          config["consumer_secret"],
                                                          config["access_token_key"],
                                                          config["access_token_secret"]).GetHelpConfiguration()
        help_configuration["updated_at"] = datetime.now()

    return help_configuration["configuration"]
