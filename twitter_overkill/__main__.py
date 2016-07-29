from flask_restful import Api

from twitter_overkill.app import app
from twitter_overkill.db import db
from twitter_overkill.restful import Tweets


if __name__ == "__main__":
    db.create_all()

    api = Api(app)
    api.add_resource(Tweets, "/tweets")
    app.run("0.0.0.0", 80)
