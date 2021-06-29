# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/APIDefine.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 3272 bytes
import os, platform, logging.config, queue
from logging.handlers import RotatingFileHandler
TOUCH_IP = '127.0.0.1'
TOUCH_PORT = 1112
LOG_DEFAULT = 'default_device'
exceptionQueue = queue.Queue()
__dir__ = os.path.dirname(os.path.abspath(__file__))
WINDOWS_ADB = __dir__ + '/platformdefult/adb/Windows/adb'
LINUX_ADB = __dir__ + '/platformdefult/adb/Linux/adb'
ADB_CMD = LINUX_ADB
if platform.system() == 'Linux':
    os.system('chmod +x ' + LINUX_ADB)
elif platform.system() == 'Windows':
    ADB_CMD = WINDOWS_ADB
if 'ANDROID_HOME' in os.environ:
    filename = 'adb'
    adb_dir = os.path.join(os.environ['ANDROID_HOME'], 'platform-tools')
    adb_cmd = os.path.join(adb_dir, filename)
    if os.path.exists(adb_cmd):
        ADB_CMD = adb_cmd
else:
    import distutils
    if 'spawn' not in dir(distutils):
        import distutils.spawn
    adb_cmd = distutils.spawn.find_executable('adb')
if adb_cmd:
    ADB_CMD = os.path.realpath(adb_cmd)
LOG_FORMAT = '[%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] : %(message)s'
UI_SCREEN_ORI_LANDSCAPE = 0
UI_SCREEN_ORI_PORTRAIT = 1
WAITTIME_MS = 1
WAITTIME_POINT = 4
PLUGIN_TOUCH_DIR = '/Platform_plugin/'
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
TOUCH_DOWN = 'touch_down'
TOUCH_UP = 'touch_up'
TOUCH_SWIPE = 'touch_swipe'
TOUCH_MOVE = 'touch_move'
TOUCH_RESET = 'touch_reset'
TOUCH_SWIPEMOVE = 'touch_swipemove'
TOUCH_CMD_LIST = [
 TOUCH_CLICK,
 TOUCH_DOWN,
 TOUCH_UP,
 TOUCH_SWIPE,
 TOUCH_MOVE,
 TOUCH_SWIPEMOVE,
 TOUCH_RESET]
DEVICE_INSTALL = 'device_install'
DEVICE_START = 'device_start'
DEVICE_EXIT = 'device_exit'
DEVICE_CURAPP = 'device_current'
DEVICE_CLEARAPP = 'device_clear'
DEVICE_WAKE = 'device_wake'
DEVICE_SLEEP = 'device_sleep'
DEVICE_WMSIZE = 'device_wmsize'
DEVICE_BINDRO = 'device_bindrotation'
DEVICE_SCREENSHOT = 'device_screenshot'
DEVICE_SCREENORI = 'device_screenori'
DEVICE_KEY = 'device_key'
DEVICE_TEXT = 'device_text'
DEVICE_MAXCONTACT = 'device_maxcontact'
DEVICE_CLICK = 'device_click'
DEVICE_SWIPE = 'device_swip'
DEVICE_PARAM = 'device_param'
DEVICE_CMD_LIST = [
 DEVICE_INSTALL,
 DEVICE_START,
 DEVICE_EXIT,
 DEVICE_CURAPP,
 DEVICE_CLEARAPP,
 DEVICE_WAKE,
 DEVICE_SLEEP,
 DEVICE_WMSIZE,
 DEVICE_BINDRO,
 DEVICE_SCREENSHOT,
 DEVICE_SCREENORI,
 DEVICE_KEY,
 DEVICE_TEXT,
 DEVICE_MAXCONTACT,
 DEVICE_CLICK,
 DEVICE_SWIPE,
 DEVICE_PARAM]

class DEVICE_KEYS(object):
    HOME = '{HOME}'
    MENU = '{MENU}'
    BACK = '{BACK}'


PORTRAIT_UP = 0
LANDSCAPE_RIGHT = 1
PORTRAIT_DOWN = 2
LANDSCAPE_LEFT = 3
ROTATION_LIST = [
 PORTRAIT_UP,
 LANDSCAPE_RIGHT,
 PORTRAIT_DOWN,
 LANDSCAPE_LEFT]