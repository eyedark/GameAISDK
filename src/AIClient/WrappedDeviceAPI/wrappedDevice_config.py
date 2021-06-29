# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/wrappedDevice_config.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 645 bytes
import os
from enum import Enum, unique
SAVE_PIC = False
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, 'log')

@unique
class DeviceType(Enum):
    Android = 'Android'
    IOS = 'IOS'
    Windows = 'Windows'


@unique
class Platform(Enum):
    Local = 'Local'
    WeTest = 'WeTest'
    GAutomator = 'GAutomator'