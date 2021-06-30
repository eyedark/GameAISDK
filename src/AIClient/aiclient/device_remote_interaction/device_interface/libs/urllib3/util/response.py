# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\libs\urllib3\util\response.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 2239 bytes
from __future__ import absolute_import
from ..packages.six.moves import http_client as httplib
from ..exceptions import HeaderParsingError

def is_fp_closed(obj):
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """
    try:
        return obj.closed
    except AttributeError:
        pass

    try:
        return obj.fp is None
    except AttributeError:
        pass

    raise ValueError('Unable to determine whether fp is closed.')


def assert_header_parsing(headers):
    """
    Asserts whether all headers have been successfully parsed.
    Extracts encountered errors from the result of parsing headers.

    Only works on Python 3.

    :param headers: Headers to verify.
    :type headers: `httplib.HTTPMessage`.

    :raises urllib3.exceptions.HeaderParsingError:
        If parsing errors are found.
    """
    if not isinstance(headers, httplib.HTTPMessage):
        raise TypeError('expected httplib.Message, got {0}.'.format(type(headers)))
    else:
        defects = getattr(headers, 'defects', None)
        get_payload = getattr(headers, 'get_payload', None)
        unparsed_data = None
        if get_payload:
            unparsed_data = get_payload()
        if defects or unparsed_data:
            raise HeaderParsingError(defects=defects, unparsed_data=unparsed_data)


def is_response_to_head(response):
    """
    Checks whether the request of a response has been a HEAD-request.
    Handles the quirks of AppEngine.

    :param conn:
    :type conn: :class:`httplib.HTTPResponse`
    """
    method = response._method
    if isinstance(method, int):
        return method == 3
    else:
        return method.upper() == 'HEAD'