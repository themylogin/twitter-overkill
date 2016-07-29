from flask import Flask

import twitter_overkill.config

__all__ = ["app"]

app = Flask("twitter_overkill")
app.config.from_object(twitter_overkill.config)
