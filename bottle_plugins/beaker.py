# -*- coding: utf-8 -*-
"""
    bottle plugin of beaker session
    ~~~~~~~~~~~~~~~~

    beaker session plugins for bottle.

    :copyright: 20150904 by raptor.zh@gmail.com.
"""
from functools import wraps
import sys
import inspect
import logging

import bottle


logger = logging.getLogger(__name__)

PY3=sys.version>"3"


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class BeakerPlugin(object):

    name = 'beaker'
    api = 2

    def __init__(self, keyword="session"):
        self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, BeakerPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another BeakerPlugin with duplicated keyword.")

    def apply(self, callback, route):
        paramspec = inspect.signature(route.callback).parameters if PY3 else inspect.getargspec(route.callback).args

        if self.keyword not in paramspec:
            return callback

        @wraps(callback)
        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = bottle.request.environ.get("beaker.session")
            return callback(*args, **kwargs)

        return wrapper
