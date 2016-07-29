from celery import Celery
from flask import has_request_context

from twitter_overkill.app import app
from twitter_overkill.db import db

__all__ = ["celery"]


def make_celery(app, db):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            if has_request_context():
                return super(ContextTask, self).__call__(*args, **kwargs)
            else:
                with app.app_context():
                    return super(ContextTask, self).__call__(*args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            if has_request_context():
                pass
            else:
                db.session.remove()

    celery.Task = ContextTask
    return celery


celery = make_celery(app, db)
