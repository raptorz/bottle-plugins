# -*- coding: utf-8 -*-
"""
    botas auth
    ~~~~~~~~~~~~~~~~

    auth plugins for bottle.

    :copyright: 20150426 by raptor.zh@gmail.com.
"""
import inspect
import bottle

import logging

logger = logging.getLogger(__name__)


# Bottle version >=0.10 required.

class AuthPlugin(object):

    name = 'auth'
    api = 2

    def __init__(self, auth_func=None, keyword="auth", dbkeyword="db"):
        self.auth_func = auth_func
        self.keyword = keyword
        self.dbkeyword = dbkeyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, AuthPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another AuthPlugin with "\
                "conflicting settings (non-unique keyword).")
    
    def apply(self, callback, route):
        pluginconf = route.config
        _auth_func = pluginconf.get("auth_func", self.auth_func)
        _auth_perm = pluginconf.get("auth_perm", None)
        _auth_args = pluginconf.get("auth_args", {})

        argspec = inspect.getargspec(route.callback)
        if self.keyword not in argspec.args or not _auth_func:
            return callback

        def wrapper(*args, **kwargs):
            if self.dbkeyword not in kwargs.keys():
                raise PluginError("[%s] parameter is required, please install the specific plugin first." % self.dbkeyword)
            auth = _auth_func(kwargs[self.dbkeyword], **_auth_args)
            if auth:
                kwargs[self.keyword] = auth
                if not _auth_perm or _auth_perm(**kwargs):
                    return callback(*args, **kwargs)

        return wrapper
