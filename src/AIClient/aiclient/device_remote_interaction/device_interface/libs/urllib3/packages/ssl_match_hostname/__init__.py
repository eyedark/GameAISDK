# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/device_interface/libs/urllib3/packages/ssl_match_hostname/__init__.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 460 bytes
try:
    from ssl import CertificateError, match_hostname
except ImportError:
    try:
        from backports.ssl_match_hostname import CertificateError, match_hostname
    except ImportError:
        from ._implementation import CertificateError, match_hostname

__all__ = ('CertificateError', 'match_hostname')