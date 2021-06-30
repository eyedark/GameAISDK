# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\libs\imap_utf7.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 3444 bytes
from __future__ import unicode_literals
from libs.six import binary_type, text_type, byte2int, iterbytes, unichr
PRINTABLE = set(range(32, 38)) | set(range(39, 127))

def encode(s):
    """Encode a folder name using IMAP modified UTF-7 encoding.

    Input is unicode; output is bytes (Python 3) or str (Python 2). If
    non-unicode input is provided, the input is returned unchanged.
    """
    if not isinstance(s, text_type):
        return s
    else:
        r = []
        _in = []

        def extend_result_if_chars_buffered():
            if _in:
                r.extend(['&', modified_utf7(''.join(_in)), '-'])
                del _in[:]

        for c in s:
            if ord(c) in PRINTABLE:
                extend_result_if_chars_buffered()
                r.append(c.encode('latin-1'))
            else:
                if c == '&':
                    extend_result_if_chars_buffered()
                    r.append('&-')
                else:
                    _in.append(c)

        extend_result_if_chars_buffered()
        return ''.join(r)


AMPERSAND_ORD = byte2int('&')
DASH_ORD = byte2int('-')

def decode(s):
    """Decode a folder name from IMAP modified UTF-7 encoding to unicode.

    Input is bytes (Python 3) or str (Python 2); output is always
    unicode. If non-bytes/str input is provided, the input is returned
    unchanged.
    """
    if not isinstance(s, binary_type):
        return s
    else:
        r = []
        _in = bytearray()
        for c in iterbytes(s):
            if c == AMPERSAND_ORD and not _in:
                _in.append(c)
            elif c == DASH_ORD and _in:
                if len(_in) == 1:
                    r.append('&')
                else:
                    r.append(modified_deutf7(_in[1:]))
                _in = bytearray()
            else:
                if _in:
                    _in.append(c)
                else:
                    r.append(unichr(c))

        if _in:
            r.append(modified_deutf7(_in[1:]))
        return ''.join(r)


def modified_utf7(s):
    s_utf7 = s.encode('utf-7')
    return s_utf7[1:-1].replace('/', ',')


def modified_deutf7(s):
    s_utf7 = '+' + s.replace(',', '/') + '-'
    return s_utf7.decode('utf-7')