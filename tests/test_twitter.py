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


class TweetLengthTestCase(unittest.TestCase):
    stub_url_length = lambda url: min(10, len(url))

    @replace("twitter_overkill.twitter.url_length", stub_url_length)
    def test_no_urls(self):
        tweet = "Hello. My name is Dmitry."
        self.assertEqual(tweet_length(tweet), len(tweet))

    @replace("twitter_overkill.twitter.url_length", stub_url_length)
    def test_url(self):
        long_url = "http://avtoremontniy-zavod-15.ru"
        tweet_template = "Hello. My name is Dmitry and I work in %s."
        self.assertEqual(tweet_length(tweet_template % long_url), len(tweet_template % ("*" * 10)))

    @replace("twitter_overkill.twitter.url_length", stub_url_length)
    def test_repetitive_urls(self):
        annoying_url = "http://2gis.ru/company"
        tweet_template = "Hello. My name is Igor and I work in %s. %s is cool! We even have free cookies in %s!"
        self.assertEqual(tweet_length(tweet_template % (annoying_url, annoying_url, annoying_url)),
                         len(tweet_template % ("*" * 10, "*" * 10, "*" * 10)))


class UrlLengthTestCase(unittest.TestCase):
    def stub_get_help_configuration(short_url_length, short_url_length_https):
        def get_help_configuration():
            return {
                "short_url_length": short_url_length,
                "short_url_length_https": short_url_length_https,
            }

        return get_help_configuration

    @replace("twitter_overkill.twitter.get_help_configuration", stub_get_help_configuration(5, 6))
    def test_http_url(self):
        self.assertEqual(url_length("http://yandex.ru"), 5)

    @replace("twitter_overkill.twitter.get_help_configuration", stub_get_help_configuration(5, 6))
    def test_https_url(self):
        self.assertEqual(url_length("https://yandex.ru"), 6)

    @replace("twitter_overkill.twitter.get_help_configuration", stub_get_help_configuration(10, 11))
    def test_extremely_short_url_without_schema(self):
        self.assertEqual(url_length("ya.ru"), 10)

    @replace("twitter_overkill.twitter.get_help_configuration", stub_get_help_configuration(20, 21))
    def test_not_shortened_url(self):
        url = "http://yandex.ru"
        self.assertEqual(url_length(url), len(url))
