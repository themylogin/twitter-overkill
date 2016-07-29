FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y npm
RUN npm install -g twitter-text

RUN apt-get -y install python3 \
                       python3-dev \
                       python3-pip \
                       python3-virtualenv

RUN apt-get -y install libpq-dev

RUN python3 -m virtualenv --python=python3 /virtualenv

RUN mkdir /twitter-overkill
RUN mkdir /twitter-overkill/twitter_overkill
RUN touch /twitter-overkill/twitter_overkill/__init__.py
ADD setup.py /twitter-overkill/setup.py

WORKDIR /twitter-overkill
RUN /virtualenv/bin/python setup.py develop
RUN /virtualenv/bin/pip install twitter_overkill[server]

RUN rm -rf /twitter-overkill/twitter_overkill
ADD twitter_overkill /twitter-overkill/twitter_overkill
