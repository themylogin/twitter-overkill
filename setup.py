from setuptools import find_packages, setup

setup(
    name="twitter-overkill",
    packages=find_packages(exclude=["tests"]),
    extras_require={
        "client": [
            "requests",
        ],
        "server": [
            "celery==3.1.23",
            "Flask==0.10.1",
            "Flask_RESTful==0.3.5",
            "Flask-SQLAlchemy==2.1",
            "psycopg2==2.6.1",
            "PyExecJS==1.4.0",
            "python-twitter==3.1",
            "requests==2.10.0",
            "SQLAlchemy-Enum34==1.0.1",
            "voluptuous==0.8.11",
        ],
        "tests": [
            "nose>=1.0",
        ],
    }
)
