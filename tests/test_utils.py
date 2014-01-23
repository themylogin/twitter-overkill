# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import Mock
from testfixtures import replace
import unittest

from twitter_overkill.utils import *


class JoinListTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(join_list([]), "")

    def test_one_item(self):
        self.assertEqual(join_list(["Мальчишки"]), "Мальчишки")

    def test_two_items(self):
        self.assertEqual(join_list(["Мальчишки", "девчонки"]), "Мальчишки и девчонки")

    def test_three_items(self):
        self.assertEqual(join_list(["Мальчишки", "девчонки", "их родители"]), "Мальчишки, девчонки и их родители")


class TweetWithListTestCase(unittest.TestCase):
    @replace("twitter_overkill.utils.tweet_with_lists", Mock())
    def test_proper_call(self, tweet_with_lists):
        tweet_with_list("Беспонтово отдыхаем", "Пьём %s", ["пиво", "вино", "водку"])
        tweet_with_lists.assert_called_with({(False,):  "Беспонтово отдыхаем",
                                             (True,):   "Пьём %s"}, [["пиво", "вино", "водку"]])


class TweetWithListsTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 8192

    def test_one_list(self):
        tweet = {
            (False,):   "Беспонтово отдыхаем",
            (True,):    "Пьём %s",
        }
        lists = [
            ["пиво", "вино", "водку"]
        ]
        self.assertListEqual(tweet_with_lists(tweet, [[]]), ["Беспонтово отдыхаем"])
        self.assertListEqual(tweet_with_lists(tweet, lists), ["Пьём пиво, вино и водку",
                                                              "Пьём пиво и вино",
                                                              "Пьём пиво",
                                                              "Беспонтово отдыхаем"])

    def test_two_lists(self):
        tweet = {
            (False, False): "Голодный день",
            (False, True):  "Пьём %s",
            (True,  False): "Едим %s",
            (True,  True):  "Едим %s, и пьём %s",
        }
        lists = [
            ["салатик", "борщ", "котлеты"],
            ["пиво", "водку"],
        ]
        self.assertListEqual(tweet_with_lists(tweet, [[], []]), ["Голодный день"])
        self.assertListEqual(tweet_with_lists(tweet, lists), ["Едим салатик, борщ и котлеты, и пьём пиво и водку",
                                                              "Едим салатик и борщ, и пьём пиво и водку",
                                                              "Едим салатик, борщ и котлеты, и пьём пиво",
                                                              "Едим салатик, и пьём пиво и водку",
                                                              "Едим салатик и борщ, и пьём пиво",
                                                              "Едим салатик, борщ и котлеты",
                                                              "Едим салатик, и пьём пиво",
                                                              "Едим салатик и борщ",
                                                              "Пьём пиво и водку",
                                                              "Едим салатик",
                                                              "Пьём пиво",
                                                              "Голодный день"])

    def test_two_lists_with_skip(self):
        tweet = {
            (False, False): "Голодный день",
            (False, True):  "Пьём %s",
            (True,  True):  "Едим %s, и пьём %s",
        }
        lists = [
            ["салатик", "борщ", "котлеты"],
            ["пиво", "водку"],
        ]
        self.assertListEqual(tweet_with_lists(tweet, [[], []]), ["Голодный день"])
        self.assertListEqual(tweet_with_lists(tweet, lists), ["Едим салатик, борщ и котлеты, и пьём пиво и водку",
                                                              "Едим салатик и борщ, и пьём пиво и водку",
                                                              "Едим салатик, борщ и котлеты, и пьём пиво",
                                                              "Едим салатик, и пьём пиво и водку",
                                                              "Едим салатик и борщ, и пьём пиво",
                                                              "Едим салатик, и пьём пиво",
                                                              "Пьём пиво и водку",
                                                              "Пьём пиво",
                                                              "Голодный день"])
