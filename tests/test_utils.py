# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
