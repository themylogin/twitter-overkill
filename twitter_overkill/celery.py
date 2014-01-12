from __future__ import absolute_import

from celery import Celery

from twitter_overkill.config import config

celery = Celery()
celery.config_from_object(config["celery"])
