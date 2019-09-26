# -*- coding: utf-8 -*-
"""
    bottle plugin of login
    ~~~~~~~~~~~~~~~~

    login plugin for bottle.
    
    [DEPRECATED]
    please using AuthPlugin replace it.

    :copyright: 20150904 by raptor.zh@gmail.com.
"""
import sys
PY3=sys.version>"3"

import inspect
import bottle

from .webexceptions import WebUnauthorizedError

import logging

logger = logging.getLogger(__name__)


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class LoginPlugin(object):

    name = 'login'
    api = 2

    def __init__(self, login_func, keyword="login", dbkeyword="db", sessionkeyword="session"):
        self.login_func = login_func
        self.keyword = keyword
        self.dbkeyword = dbkeyword
        self.sessionkeyword = sessionkeyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, LoginPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another LoginPlugin with duplicated keyword.")

    def apply(self, callback, route):
        paramspec = inspect.signature(route.callback).parameters if PY3 else inspect.getargspec(route.callback).args

        if self.keyword not in paramspec or not self.login_func:
            return callback
        if self.dbkeyword not in paramspec or self.sessionkeyword not in paramspec:
            raise PluginError("[%s] and [%s] parameter is required, please install the specific plugin first." % (self.dbkeyword, self.sessionkeyword))

        def wrapper(*args, **kwargs):
            login = self.login_func(kwargs[self.dbkeyword], kwargs[self.sessionkeyword])
            if login:
                kwargs[self.keyword] = login
                return callback(*args, **kwargs)
            else:
                raise WebUnauthorizedError

        return wrapper
