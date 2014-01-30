# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from testfixtures import replace
import unittest

from twitter_overkill.twitter import *


class ChooseTweetVariantTestCase(unittest.TestCase):
    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_empty_list(self):
        self.assertEqual(choose_tweet_variant([]), None)


    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_one_variant(self):
        short_tweet = "Hello. My name is Dmitry"
        self.assertEqual(choose_tweet_variant([short_tweet]), short_tweet)


    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_two_variants_priority(self):
        short_tweet1 = "Hello. My name is Dmitry"
        short_tweet2 = "Hello. My name is Oleg"
        self.assertEqual(choose_tweet_variant([short_tweet1, short_tweet2]), short_tweet1)


    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_two_variants_first_is_too_long(self):
        short_tweet = "Hello. My name is Dmitry"
        long_tweet = "Hello. My name is Dmitry. " * 100
        self.assertEqual(choose_tweet_variant([long_tweet, short_tweet]), short_tweet)


class CutTweetTestCase(unittest.TestCase):
    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_short_tweet(self):
        short_tweet = "Hello. My name is Dmitry"
        self.assertEqual(cut_tweet(short_tweet), short_tweet)

    @replace("twitter_overkill.twitter.tweet_length", len)
    def test_long_tweet(self):
        long_tweet = "Hello. My name is Dmitry. " * 100
        self.assertEqual(cut_tweet(long_tweet), long_tweet[:139] + "…")
