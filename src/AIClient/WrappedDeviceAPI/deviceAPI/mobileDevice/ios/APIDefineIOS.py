# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/ios/APIDefineIOS.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 1732 bytes
import os, platform, logging.config, queue
from logging.handlers import RotatingFileHandler
LOG_DEFAULT = 'default_device'
exceptionQueue = queue.Queue()
__dir__ = os.path.dirname(os.path.abspath(__file__))
LOG_FORMAT = '[%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] : %(message)s'
UI_SCREEN_ORI_LANDSCAPE = 0
UI_SCREEN_ORI_PORTRAIT = 1
WAITTIME_MS = 1
WAITTIME_POINT = 4
TOUCH_KEY = [
 'aType',
 'sx',
 'sy',
 'ex',
 'ey',
 'contact',
 'durationMS',
 'wait_time',
 'needUp']
LOG_DEBUG = logging.DEBUG
LOG_INFO = logging.INFO
LOG_WARNING = logging.WARNING
LOG_ERROR = logging.ERROR
LOG_CRITICAL = logging.CRITICAL
LOG_LIST = [
 LOG_DEBUG,
 LOG_INFO,
 LOG_WARNING,
 LOG_ERROR,
 LOG_CRITICAL]
TOUCH_CLICK = 'touch_click'
TOUCH_SWIPE = 'touch_swipe'
TOUCH_RESET = 'touch_reset'
TOUCH_CMD_LIST = [
 TOUCH_CLICK,
 TOUCH_SWIPE,
 TOUCH_RESET]
DEVICE_INSTALL = 'device_install'
DEVICE_START = 'device_start'
DEVICE_EXIT = 'device_exit'
DEVICE_CURAPP = 'device_current'
DEVICE_WAKE = 'device_wake'
DEVICE_SLEEP = 'device_sleep'
DEVICE_WMSIZE = 'device_wmsize'
DEVICE_KEY = 'device_key'
DEVICE_MAXCONTACT = 'device_maxcontact'
DEVICE_CMD_LIST = [
 DEVICE_INSTALL,
 DEVICE_START,
 DEVICE_EXIT,
 DEVICE_CURAPP,
 DEVICE_WAKE,
 DEVICE_SLEEP,
 DEVICE_WMSIZE,
 DEVICE_KEY,
 DEVICE_MAXCONTACT]
PORTRAIT_UP = 0
LANDSCAPE_RIGHT = 1
PORTRAIT_DOWN = 2
LANDSCAPE_LEFT = 3
ROTATION_LIST = [
 PORTRAIT_UP,
 LANDSCAPE_RIGHT,
 PORTRAIT_DOWN,
 LANDSCAPE_LEFT]