# -*- coding: utf-8 -*-
"""
    exeptions for botas
    ~~~~~~~~~~~~~~~~

    :copyright: 2010-13 by raptor.zh@gmail.com
"""
import bottle


class WebError(bottle.HTTPError):
    pass


class WebBadrequestError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 400, body or "Bad request!")


class WebUnauthorizedError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 401, body or "Unauthorized!")


class WebForbiddenError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 403, body or "Forbidden!")


class WebNotfoundError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 404, body or "Not found!")


class WebMethodnotallowedError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 405, body or "Method not allowed!")


class WebInternalError(WebError):
    def __init__(self, body=""):
        WebError.__init__(self, 500, body or "Internal server error! Please see log for detail!")
