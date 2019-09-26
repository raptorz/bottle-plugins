# -*- coding: utf-8 -*-
"""
    bottle plugin of template
    ~~~~~~~~~~~~~~~~

    template for bottle.

    :copyright: 20150904 by raptor.zh@gmail.com.
    rev.20190130: add config
"""
from functools import wraps
import logging

import bottle


logger = logging.getLogger(__name__)


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class TemplatePlugin(object):

    name = 'template'
    api = 2

    def __init__(self, template=bottle.template, authkeyword="", configkeyword="config", config=None):
        self.template = template
        self.authkeyword = authkeyword
        self.configkeyword = configkeyword
        self.config = config

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, TemplatePlugin):
                continue
            raise PluginError("Found another TemplatePlugin.")

    def apply(self, callback, route):
        _authkeyword = route.config.get("authkeyword", self.authkeyword)
        _view = route.config.get("view", "")

        if not self.template or not _view:
            return callback

        @wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if _authkeyword and _authkeyword in kwargs.keys() and isinstance(result, dict):
                result[_authkeyword] = kwargs[_authkeyword]
            if self.configkeyword and self.config and isinstance(result, dict):
                result[self.configkeyword] = self.config
            return self.template(_view, result) if isinstance(result, dict) else result

        return wrapper
