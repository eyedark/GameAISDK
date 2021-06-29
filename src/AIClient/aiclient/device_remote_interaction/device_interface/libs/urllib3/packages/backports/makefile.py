# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/device_interface/libs/urllib3/packages/backports/makefile.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 1461 bytes
"""
backports.makefile
~~~~~~~~~~~~~~~~~~

Backports the Python 3 ``socket.makefile`` method for use with anything that
wants to create a "fake" socket object.
"""
import io
from socket import SocketIO

def backport_makefile(self, mode='r', buffering=None, encoding=None, errors=None, newline=None):
    """
    Backport of ``socket.makefile`` from Python 3.5.
    """
    if not set(mode) <= set(['r', 'w', 'b']):
        raise ValueError('invalid mode %r (only r, w, b allowed)' % (mode,))
    writing = 'w' in mode
    reading = 'r' in mode or not writing
    if not reading:
        assert writing
    binary = 'b' in mode
    rawmode = ''
    if reading:
        rawmode += 'r'
    if writing:
        rawmode += 'w'
    raw = SocketIO(self, rawmode)
    self._makefile_refs += 1
    if buffering is None:
        buffering = -1
    if buffering < 0:
        buffering = io.DEFAULT_BUFFER_SIZE
    if buffering == 0:
        if not binary:
            raise ValueError('unbuffered streams must be binary')
        return raw
    if reading and writing:
        buffer = io.BufferedRWPair(raw, raw, buffering)
    else:
        if reading:
            buffer = io.BufferedReader(raw, buffering)
        else:
            assert writing
            buffer = io.BufferedWriter(raw, buffering)
    if binary:
        return buffer
    text = io.TextIOWrapper(buffer, encoding, errors, newline)
    text.mode = mode
    return text