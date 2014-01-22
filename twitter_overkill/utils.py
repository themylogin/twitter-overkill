# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def join_list(l, separator=", ", last_separator=" и "):
    if len(l) == 0:
        return ""

    if len(l) == 1:
        return l[0]

    return separator.join(l[:-1]) + last_separator + l[-1]
