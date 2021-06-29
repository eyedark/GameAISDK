# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/device_interface/libs/urllib3/connection.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 11617 bytes
from __future__ import absolute_import
import datetime, logging, os, sys, socket
from socket import error as SocketError, timeout as SocketTimeout
import warnings
from .packages import six
try:
    from http.client import HTTPConnection as _HTTPConnection
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPConnection as _HTTPConnection
    from httplib import HTTPException

try:
    import ssl
    BaseSSLError = ssl.SSLError
except (ImportError, AttributeError):
    ssl = None

    class BaseSSLError(BaseException):
        pass


try:
    ConnectionError = ConnectionError
except NameError:

    class ConnectionError(Exception):
        pass


from .exceptions import NewConnectionError, ConnectTimeoutError, SubjectAltNameWarning, SystemTimeWarning
from .packages.ssl_match_hostname import match_hostname, CertificateError
from .util.ssl_ import resolve_cert_reqs, resolve_ssl_version, ssl_wrap_socket, assert_fingerprint
from .util import connection
from ._collections import HTTPHeaderDict
log = logging.getLogger(__name__)
port_by_scheme = {'http': 80, 
 'https': 443}
RECENT_DATE = datetime.date(2014, 1, 1)

class DummyConnection(object):
    __doc__ = 'Used to detect a failed ConnectionCls import.'


class HTTPConnection(_HTTPConnection, object):
    __doc__ = "\n    Based on httplib.HTTPConnection but provides an extra constructor\n    backwards-compatibility layer between older and newer Pythons.\n\n    Additional keyword parameters are used to configure attributes of the connection.\n    Accepted parameters include:\n\n      - ``strict``: See the documentation on :class:`urllib3.connectionpool.HTTPConnectionPool`\n      - ``source_address``: Set the source address for the current connection.\n\n        .. note:: This is ignored for Python 2.6. It is only applied for 2.7 and 3.x\n\n      - ``socket_options``: Set specific options on the underlying socket. If not specified, then\n        defaults are loaded from ``HTTPConnection.default_socket_options`` which includes disabling\n        Nagle's algorithm (sets TCP_NODELAY to 1) unless the connection is behind a proxy.\n\n        For example, if you wish to enable TCP Keep Alive in addition to the defaults,\n        you might pass::\n\n            HTTPConnection.default_socket_options + [\n                (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),\n            ]\n\n        Or you may want to disable the defaults by passing an empty list (e.g., ``[]``).\n    "
    default_port = port_by_scheme['http']
    default_socket_options = [
     (
      socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
    is_verified = False

    def __init__(self, *args, **kw):
        if six.PY3:
            kw.pop('strict', None)
        self.source_address = kw.get('source_address')
        if sys.version_info < (2, 7):
            kw.pop('source_address', None)
        self.socket_options = kw.pop('socket_options', self.default_socket_options)
        _HTTPConnection.__init__(self, *args, **kw)

    def _new_conn(self):
        """ Establish a socket connection and set nodelay settings on it.

        :return: New socket connection.
        """
        extra_kw = {}
        if self.source_address:
            extra_kw['source_address'] = self.source_address
        if self.socket_options:
            extra_kw['socket_options'] = self.socket_options
        try:
            conn = connection.create_connection((
             self.host, self.port), self.timeout, **extra_kw)
        except SocketTimeout as e:
            raise ConnectTimeoutError(self, 'Connection to %s timed out. (connect timeout=%s)' % (
             self.host, self.timeout))
        except SocketError as e:
            raise NewConnectionError(self, 'Failed to establish a new connection: %s' % e)

        return conn

    def _prepare_conn(self, conn):
        self.sock = conn
        if getattr(self, '_tunnel_host', None):
            self._tunnel()
            self.auto_open = 0

    def connect(self):
        conn = self._new_conn()
        self._prepare_conn(conn)

    def request_chunked(self, method, url, body=None, headers=None):
        """
        Alternative to the common request method, which sends the
        body with chunked encoding and not as one block
        """
        headers = HTTPHeaderDict(headers if headers is not None else {})
        skip_accept_encoding = 'accept-encoding' in headers
        self.putrequest(method, url, skip_accept_encoding=skip_accept_encoding)
        for header, value in headers.items():
            self.putheader(header, value)

        if 'transfer-encoding' not in headers:
            self.putheader('Transfer-Encoding', 'chunked')
        self.endheaders()
        if body is not None:
            stringish_types = six.string_types + (six.binary_type,)
            if isinstance(body, stringish_types):
                body = (
                 body,)
            for chunk in body:
                if not chunk:
                    pass
                else:
                    if not isinstance(chunk, six.binary_type):
                        chunk = chunk.encode('utf8')
                    len_str = hex(len(chunk))[2:]
                    self.send(len_str.encode('utf-8'))
                    self.send('\r\n')
                    self.send(chunk)
                    self.send('\r\n')

        self.send('0\r\n\r\n')


class HTTPSConnection(HTTPConnection):
    default_port = port_by_scheme['https']

    def __init__(self, host, port=None, key_file=None, cert_file=None, strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, **kw):
        HTTPConnection.__init__(self, host, port, strict=strict, timeout=timeout, **kw)
        self.key_file = key_file
        self.cert_file = cert_file
        self._protocol = 'https'

    def connect(self):
        conn = self._new_conn()
        self._prepare_conn(conn)
        self.sock = ssl.wrap_socket(conn, self.key_file, self.cert_file)


class VerifiedHTTPSConnection(HTTPSConnection):
    __doc__ = '\n    Based on httplib.HTTPSConnection but wraps the socket with\n    SSL certification.\n    '
    cert_reqs = None
    ca_certs = None
    ca_cert_dir = None
    ssl_version = None
    assert_fingerprint = None

    def set_cert(self, key_file=None, cert_file=None, cert_reqs=None, ca_certs=None, assert_hostname=None, assert_fingerprint=None, ca_cert_dir=None):
        if (ca_certs or ca_cert_dir) and cert_reqs is None:
            cert_reqs = 'CERT_REQUIRED'
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.assert_hostname = assert_hostname
        self.assert_fingerprint = assert_fingerprint
        self.ca_certs = ca_certs and os.path.expanduser(ca_certs)
        self.ca_cert_dir = ca_cert_dir and os.path.expanduser(ca_cert_dir)

    def connect(self):
        conn = self._new_conn()
        resolved_cert_reqs = resolve_cert_reqs(self.cert_reqs)
        resolved_ssl_version = resolve_ssl_version(self.ssl_version)
        hostname = self.host
        if getattr(self, '_tunnel_host', None):
            self.sock = conn
            self._tunnel()
            self.auto_open = 0
            hostname = self._tunnel_host
        is_time_off = datetime.date.today() < RECENT_DATE
        if is_time_off:
            warnings.warn('System time is way off (before {0}). This will probably lead to SSL verification errors'.format(RECENT_DATE), SystemTimeWarning)
        self.sock = ssl_wrap_socket(conn, self.key_file, self.cert_file, cert_reqs=resolved_cert_reqs, ca_certs=self.ca_certs, ca_cert_dir=self.ca_cert_dir, server_hostname=hostname, ssl_version=resolved_ssl_version)
        if self.assert_fingerprint:
            assert_fingerprint(self.sock.getpeercert(binary_form=True), self.assert_fingerprint)
        elif resolved_cert_reqs != ssl.CERT_NONE and self.assert_hostname is not False:
            cert = self.sock.getpeercert()
            if not cert.get('subjectAltName', ()):
                warnings.warn('Certificate for {0} has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/shazow/urllib3/issues/497 for details.)'.format(hostname), SubjectAltNameWarning)
            _match_hostname(cert, self.assert_hostname or hostname)
        self.is_verified = resolved_cert_reqs == ssl.CERT_REQUIRED or self.assert_fingerprint is not None


def _match_hostname(cert, asserted_hostname):
    try:
        match_hostname(cert, asserted_hostname)
    except CertificateError as e:
        log.error('Certificate did not match expected hostname: %s. Certificate: %s', asserted_hostname, cert)
        e._peer_cert = cert
        raise


if ssl:
    UnverifiedHTTPSConnection = HTTPSConnection
    HTTPSConnection = VerifiedHTTPSConnection
else:
    HTTPSConnection = DummyConnection