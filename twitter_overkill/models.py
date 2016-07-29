import enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_enum34 import Enum

from twitter_overkill.db import db

__all__ = ["Tweet", "TweetState"]


class TweetState(enum.Enum):
    TEMPORARY_ERROR = "temporary-error"
    PERMANENT_ERROR = "permanent-error"
    POSTED = "posted"


class Tweet(db.Model):
    id              = db.Column(db.String(36), primary_key=True)
    created_at      = db.Column(db.DateTime())
    auth            = db.Column(JSONB())
    tweet_variants  = db.Column(JSONB())
    user            = db.Column(db.String(20), nullable=True)
    tweet           = db.Column(db.Text())
    state           = db.Column(Enum(TweetState, name="tweet_state"))
    state_data      = db.Column(db.Text())
    updated_at      = db.Column(db.DateTime())
