# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\libs\urllib3\util\request.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 2200 bytes
from __future__ import absolute_import
from base64 import b64encode
from ..packages.six import b
ACCEPT_ENCODING = 'gzip,deflate'

def make_headers(keep_alive=None, accept_encoding=None, user_agent=None, basic_auth=None, proxy_basic_auth=None, disable_cache=None):
    """
    Shortcuts for generating request headers.

    :param keep_alive:
        If ``True``, adds 'connection: keep-alive' header.

    :param accept_encoding:
        Can be a boolean, list, or string.
        ``True`` translates to 'gzip,deflate'.
        List will get joined by comma.
        String will be used as provided.

    :param user_agent:
        String representing the user-agent you want, such as
        "python-urllib3/0.6"

    :param basic_auth:
        Colon-separated username:password string for 'authorization: basic ...'
        auth header.

    :param proxy_basic_auth:
        Colon-separated username:password string for 'proxy-authorization: basic ...'
        auth header.

    :param disable_cache:
        If ``True``, adds 'cache-control: no-cache' header.

    Example::

        >>> make_headers(keep_alive=True, user_agent="Batman/1.0")
        {'connection': 'keep-alive', 'user-agent': 'Batman/1.0'}
        >>> make_headers(accept_encoding=True)
        {'accept-encoding': 'gzip,deflate'}
    """
    headers = {}
    if accept_encoding:
        if isinstance(accept_encoding, str):
            pass
        else:
            if isinstance(accept_encoding, list):
                accept_encoding = ','.join(accept_encoding)
            else:
                accept_encoding = ACCEPT_ENCODING
            headers['accept-encoding'] = accept_encoding
    if user_agent:
        headers['user-agent'] = user_agent
    if keep_alive:
        headers['connection'] = 'keep-alive'
    if basic_auth:
        headers['authorization'] = 'Basic ' + b64encode(b(basic_auth)).decode('utf-8')
    if proxy_basic_auth:
        headers['proxy-authorization'] = 'Basic ' + b64encode(b(proxy_basic_auth)).decode('utf-8')
    if disable_cache:
        headers['cache-control'] = 'no-cache'
    return headers