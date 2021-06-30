# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\libs\urllib3\util\url.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 6096 bytes
from __future__ import absolute_import
from collections import namedtuple
from ..exceptions import LocationParseError
url_attrs = [
 'scheme', 'auth', 'host', 'port', 'path', 'query', 'fragment']

class Url(namedtuple('Url', url_attrs)):
    __doc__ = '\n    Datastructure for representing an HTTP URL. Used as a return value for\n    :func:`parse_url`.\n    '
    slots = ()

    def __new__(cls, scheme=None, auth=None, host=None, port=None, path=None, query=None, fragment=None):
        if path:
            if not path.startswith('/'):
                path = '/' + path
        return super(Url, cls).__new__(cls, scheme, auth, host, port, path, query, fragment)

    @property
    def hostname(self):
        """For backwards-compatibility with urlparse. We're nice like that."""
        return self.host

    @property
    def request_uri(self):
        """Absolute path including the query string."""
        uri = self.path or '/'
        if self.query is not None:
            uri += '?' + self.query
        return uri

    @property
    def netloc(self):
        """Network location including host and port"""
        if self.port:
            return '%s:%d' % (self.host, self.port)
        else:
            return self.host

    @property
    def url(self):
        """
        Convert self into a url

        This function should more or less round-trip with :func:`.parse_url`. The
        returned url may not be exactly the same as the url inputted to
        :func:`.parse_url`, but it should be equivalent by the RFC (e.g., urls
        with a blank port will have : removed).

        Example: ::

            >>> U = parse_url('http://google.com/mail/')
            >>> U.url
            'http://google.com/mail/'
            >>> Url('http', 'username:password', 'host.com', 80,
            ... '/path', 'query', 'fragment').url
            'http://username:password@host.com:80/path?query#fragment'
        """
        scheme, auth, host, port, path, query, fragment = self
        url = ''
        if scheme is not None:
            url += scheme + '://'
        if auth is not None:
            url += auth + '@'
        if host is not None:
            url += host
        if port is not None:
            url += ':' + str(port)
        if path is not None:
            url += path
        if query is not None:
            url += '?' + query
        if fragment is not None:
            url += '#' + fragment
        return url

    def __str__(self):
        return self.url


def split_first(s, delims):
    """
    Given a string and an iterable of delimiters, split on the first found
    delimiter. Return two split parts and the matched delimiter.

    If not found, then the first part is the full input string.

    Example::

        >>> split_first('foo/bar?baz', '?/=')
        ('foo', 'bar?baz', '/')
        >>> split_first('foo/bar?baz', '123')
        ('foo/bar?baz', '', None)

    Scales linearly with number of delims. Not ideal for large number of delims.
    """
    min_idx = None
    min_delim = None
    for d in delims:
        idx = s.find(d)
        if idx < 0:
            continue
        if min_idx is None or idx < min_idx:
            min_idx = idx
            min_delim = d

    if min_idx is None or min_idx < 0:
        return (s, '', None)
    else:
        return (
         s[:min_idx], s[min_idx + 1:], min_delim)


def parse_url(url):
    """
    Given a url, return a parsed :class:`.Url` namedtuple. Best-effort is
    performed to parse incomplete urls. Fields not provided will be None.

    Partly backwards-compatible with :mod:`urlparse`.

    Example::

        >>> parse_url('http://google.com/mail/')
        Url(scheme='http', host='google.com', port=None, path='/mail/', ...)
        >>> parse_url('google.com:80')
        Url(scheme=None, host='google.com', port=80, path=None, ...)
        >>> parse_url('/foo?bar')
        Url(scheme=None, host=None, port=None, path='/foo', query='bar', ...)
    """
    if not url:
        return Url()
    else:
        scheme = None
        auth = None
        host = None
        port = None
        path = None
        fragment = None
        query = None
        if '://' in url:
            scheme, url = url.split('://', 1)
        url, path_, delim = split_first(url, ['/', '?', '#'])
        if delim:
            path = delim + path_
        if '@' in url:
            auth, url = url.rsplit('@', 1)
        if url:
            if url[0] == '[':
                host, url = url.split(']', 1)
                host += ']'
        if ':' in url:
            _host, port = url.split(':', 1)
            if not host:
                host = _host
            if port:
                if not port.isdigit():
                    raise LocationParseError(url)
                port = int(port)
            else:
                port = None
        else:
            if not host:
                if url:
                    host = url
        if not path:
            return Url(scheme, auth, host, port, path, query, fragment)
        if '#' in path:
            path, fragment = path.split('#', 1)
        if '?' in path:
            path, query = path.split('?', 1)
        return Url(scheme, auth, host, port, path, query, fragment)


def get_host(url):
    """
    Deprecated. Use :func:`.parse_url` instead.
    """
    p = parse_url(url)
    return (p.scheme or 'http', p.hostname, p.port)