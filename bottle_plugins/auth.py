# -*- coding: utf-8 -*-
"""
    bottle plugin of auth
    ~~~~~~~~~~~~~~~~

    auth plugin for bottle.

    :copyright: 20170123 by raptor.zh@gmail.com.
"""
from functools import wraps
import sys
import inspect
import logging

import bottle

from .webexceptions import WebUnauthorizedError, WebForbiddenError


logger = logging.getLogger(__name__)

PY3 = sys.version > "3"


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class AuthPlugin(object):

    name = 'auth'
    api = 2

    def __init__(self, auth_func=None, keyword="auth", dbkeyword="db", sessionkeyword="session"):
        self.auth_func = auth_func
        self.keyword = keyword
        self.dbkeyword = dbkeyword
        self.sessionkeyword = sessionkeyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, AuthPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another AuthPlugin with duplicated keyword.")
    
    def apply(self, callback, route):
        pluginconf = route.config
        _auth_func = pluginconf.get("auth_func", self.auth_func)
        _auth_perm = pluginconf.get("auth_perm", None)
        _auth_args = pluginconf.get("auth_args", {})

        paramspec = inspect.signature(route.callback).parameters if PY3 else inspect.getargspec(route.callback).args

        if self.keyword not in paramspec or not self.auth_func:
            return callback
        if self.dbkeyword not in paramspec:
            raise PluginError(
                "[{}] parameter is required, please install the specific plugin first.".format(self.dbkeyword))
        if self.sessionkeyword not in paramspec:
            raise PluginError(
                "[{}] parameter is required, please install the specific plugin first.".format(self.sessionkeyword))

        @wraps(callback)
        def wrapper(*args, **kwargs):
            params = _auth_args.copy()
            if self.dbkeyword:
                params[self.dbkeyword] = kwargs.get(self.dbkeyword)
            if self.sessionkeyword:
                params[self.sessionkeyword] = kwargs.get(self.sessionkeyword)
            auth = _auth_func(**params)
            if auth:
                kwargs[self.keyword] = auth
                if not _auth_perm or _auth_perm(**kwargs):
                    return callback(*args, **kwargs)
                else:
                    raise WebForbiddenError
            else:
                raise WebUnauthorizedError

        return wrapper
