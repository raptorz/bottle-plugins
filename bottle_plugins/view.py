# -*- coding: utf-8 -*-
"""
    bottle plugin of template
    ~~~~~~~~~~~~~~~~

    template for bottle.

    :copyright: 20150904 by raptor.zh@gmail.com.
"""
import sys
PY3=sys.version>"3"

import inspect
import bottle

import logging

logger = logging.getLogger(__name__)


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class ViewPlugin(object):

    name = 'view'
    api = 2

    def __init__(self, template=bottle.template):
        self.template = template

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, ViewPlugin):
                continue

    def apply(self, callback, route):
        _template = route.config.get("template", self.template)
        _view = route.config.get("view", "")

        argspec = inspect.getargspec(route.callback)

        if not _template or not _view:
            return callback

        def wrapper(*args, **kwargs):
            return _template(_view, callback(*args, **kwargs))

        return wrapper
