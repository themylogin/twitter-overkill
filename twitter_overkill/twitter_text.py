import execjs

_node = execjs.get("Node")
_context = execjs.compile("""
    var twitter = require('twitter-text');
""")

get_tweet_length = lambda text, options: _context.call("twitter.getTweetLength", text, options)
