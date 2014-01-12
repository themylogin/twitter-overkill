from __future__ import absolute_import

import os
import yaml


class ConfigNotFound(Exception):
    pass


def find_config():
    configs = (os.path.expanduser("~/.config/twitter-overkill.yaml"), "/etc/twitter-overkill.yaml")

    for config in configs:
        if os.path.exists(config) and os.access(config, os.R_OK):
            return config

    raise ConfigNotFound("No readable config found. Places checked: %s" % (configs,))


def read_config(config):
    return yaml.load(open(config))
