from __future__ import absolute_import

import twitter

from twitter_overkill.twitter import post_tweet

__all__ = ["tweet"]


def tweet(twitter_api, tweet_variants):
    auth_list = [twitter_api._consumer_key,
                 twitter_api._consumer_secret,
                 twitter_api._access_token_key,
                 twitter_api._access_token_secret]
    if not all(auth_list):
        raise twitter.TwitterError("API must be authenticated.")

    if not isinstance(tweet_variants, list):
        tweet_variants = [tweet_variants]

    return post_tweet.delay(auth_list, tweet_variants)
