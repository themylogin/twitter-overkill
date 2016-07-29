import json
import requests

__all__ = ["TwitterOverkill"]


class TwitterOverkill(object):
    def __init__(self, url):
        self.url = url

    def tweet(self, api, text):
        result = requests.post("%s/tweets" % self.url, data=json.dumps({
            "auth": {
                "consumer_key": api._consumer_key,
                "consumer_secret": api._consumer_secret,
                "access_token_key": api._access_token_key,
                "access_token_secret": api._access_token_secret,
            },
            "text": text,
        }))
        result.raise_for_status()
        return result.json()
