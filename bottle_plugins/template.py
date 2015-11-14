# -*- coding: utf-8 -*-
"""
    bottle plugin of template
    ~~~~~~~~~~~~~~~~

    template for bottle.

    :copyright: 20150904 by raptor.zh@gmail.com.
"""
import inspect
import bottle

import logging

logger = logging.getLogger(__name__)


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class TemplatePlugin(object):

    name = 'template'
    api = 2

    def __init__(self, template=bottle.template, login_keyword="login"):
        self.template = template
        self.login_keyword = login_keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, TemplatePlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another TemplatePlugin with duplicated keyword.")

    def apply(self, callback, route):
        _template = route.config.get("template", self.template)
        _view = route.config.get("view", "")

        if not _template or not _view:
            return callback

        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if self.login_keyword in kwargs.keys() and isinstance(result, dict):
                result[self.login_keyword] = kwargs[self.login_keyword]
            return _template(_view, result)

        return wrapper
