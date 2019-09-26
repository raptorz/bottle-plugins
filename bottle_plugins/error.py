# -*- coding: utf-8 -*-
"""
    bottle plugin of error process
    ~~~~~~~~~~~~~~~~

    error plugin for bottle.

    :copyright: 20170123 by raptor.zh@gmail.com.
"""
from functools import wraps
import sys
import logging

import bottle


logger = logging.getLogger(__name__)

PY3 = sys.version > "3"


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class ErrorPlugin(object):

    name = 'error'
    api = 2

    def __init__(self, error_func):
        self.error_func = error_func


    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, ErrorPlugin):
                continue

    def apply(self, callback, route):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception as e:
                raise self.error_func(e)

        return wrapper
