from flask import request
from flask_restful import abort, Resource, Api
import uuid
from voluptuous import Schema, Required, Any, MultipleInvalid

from twitter_overkill.twitter import post_tweet


class Tweets(Resource):
    def post(self):
        args = request.get_json(force=True, cache=False)

        schema = Schema({
            Required("auth"): Schema({
                Required("consumer_key"): str,
                Required("consumer_secret"): str,
                Required("access_token_key"): str,
                Required("access_token_secret"): str,
            }),
            Required("text"): Any(str, [str]),
        })
        try:
            args = schema(args)
        except MultipleInvalid as e:
            abort(400, errors={".".join(map(str, error.path)): error.error_message
                               for error in e.errors})

        id = str(uuid.uuid4())
        post_tweet.delay(id, args["auth"], args["text"] if isinstance(args["text"], list) else [args["text"]])

        return {"id": id}, 201
