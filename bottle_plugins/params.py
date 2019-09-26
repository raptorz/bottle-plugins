# -*- coding: utf-8 -*-
"""
    bottle plugin of request parameters
    ~~~~~~~~~~~~~~~~

    request parameters plugins for bottle.

    :copyright: 20150426 by raptor.zh@gmail.com.
    2015-09-02 for python3
"""
from functools import wraps
import sys
import inspect
import logging

import bottle


logger = logging.getLogger(__name__)

PY3 = sys.version > "3"


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class ParamsPlugin(object):

    name = 'params'
    api = 2

    def __init__(self, json_params=False, encoding='utf-8'):
        self.json_params = json_params
        self.encoding = encoding

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, ParamsPlugin):
                continue
            raise bottle.PluginError("Found another ParamsPlugin be installed.")

    def apply(self, callback, route):
        pluginconf = route.config
        _json_params = pluginconf.get("json_params", self.json_params)

        argspec = inspect.signature(route.callback) if PY3 else inspect.getargspec(route.callback)

        @wraps(callback)
        def wrapper(*args, **kwargs):
            try:
                if _json_params:
                    kw = bottle.request.json
                else:
                    if route.method == "POST" or route.method == "PUT":
                        kw = bottle.request.forms
                    else:
                        kw = bottle.request.query
            except:
                kw = None
            if kw:
                keywords = [p for p in argspec.parameters.values()
                            if p.kind == inspect.Parameter.VAR_KEYWORD] if PY3 else argspec.keywords
                argkeys = [p.name for p in argspec.parameters.values()
                           if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD] if PY3 else argspec.args
                keys = set(kw.keys()) - set(kwargs.keys())
                if not keywords:
                    keys = keys & set(argkeys[len(args):])
                fn = (lambda d, k: d.__getitem__(k)) if _json_params or PY3 and bottle.request.content_type.find(
                        "multipart/form-data") >= 0 else (lambda d, k: d.__getattr__(k))
                [kwargs.__setitem__(k, fn(kw, k)) for k in keys]
            return callback(*args, **kwargs)

        return wrapper
