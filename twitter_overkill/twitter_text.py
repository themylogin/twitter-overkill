# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import execjs

_node = execjs.get("Node")
_context = execjs.compile("""
    var twitter = require('twitter-text');
""")

extract_urls = lambda tweet: _context.call("twitter.extractUrls", tweet)
