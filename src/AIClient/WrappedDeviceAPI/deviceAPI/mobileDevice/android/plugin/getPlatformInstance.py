# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/getPlatformInstance.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 1027 bytes
import sys, importlib, traceback
from ..APIDefine import *
from wrappedDevice_config import Platform
parentdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parentdir + PLUGIN_TOUCH_DIR)

def GetPlatformInstance(serial=None, platform=None):
    if serial is None:
        logger = logging.getLogger(LOG_DEFAULT)
    else:
        logger = logging.getLogger(serial)
    try:
        if platform == Platform.Local.value:
            module = importlib.import_module('PlatformWeTest')
        else:
            if platform == Platform.WeTest.value:
                module = importlib.import_module('PlatformWeTest')
            else:
                logger.error('unknown platform: {}'.format(platform))
                return
        getInstance = getattr(module, 'GetInstance')
        return getInstance()
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        return