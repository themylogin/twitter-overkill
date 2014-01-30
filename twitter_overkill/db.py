from __future__ import absolute_import

import json
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import BigInteger, DateTime, Enum, PickleType, String, Text
from sqlalchemy.ext.declarative import declarative_base

from twitter_overkill.config import config

__all__ = ["get_connection",
           "Tweet", "get_tweet", "update_tweet"]

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweet"

    id              = Column(BigInteger, primary_key=True)
    created_at      = Column(DateTime())
    auth_list       = Column(PickleType(pickler=json))
    tweet_variants  = Column(PickleType(pickler=json))
    user            = Column(String(20))
    tweet           = Column(Text())
    state           = Column(Enum("temporary-error",
                                  "permanent-error",
                                  "posted"))
    state_data      = Column(Text())
    updated_at      = Column(DateTime())


Base.metadata.create_all(create_engine(config["db"]))


def get_connection():
    return create_engine(config["db"]).connect()


def get_tweet(connection, id):
    tweet = connection.execute(Tweet.__table__.select().where(Tweet.id == id)).first()
    if tweet is None:
        return None

    return Tweet(**dict(tweet.items()))


def update_tweet(connection, tweet):
    if tweet.id is None:
        tweet.id = connection.execute(Tweet.__table__.insert().values(**tweet_to_dict(tweet))).inserted_primary_key[0]
    else:
        connection.execute(Tweet.__table__.update().values(**tweet_to_dict(tweet)).where(Tweet.id == tweet.id))


def tweet_to_dict(tweet):
    return {column.name: getattr(tweet, column.name)
            for column in Tweet.__table__.columns
            if column.name != "id"}
