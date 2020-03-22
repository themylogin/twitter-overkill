from flask_restful import Api

from twitter_overkill.app import app
from twitter_overkill.db import db
from twitter_overkill.restful import TweetsResource, TweetResource


if __name__ == "__main__":
    db.create_all()

    api = Api(app)
    api.add_resource(TweetsResource, "/tweets")
    api.add_resource(TweetResource, "/tweet/<id>")
    app.run("0.0.0.0", 80)
