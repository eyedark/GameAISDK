# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/APIDefine.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 1189 bytes
from logging.handlers import RotatingFileHandler
LOG_FORMAT = '[%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] : %(message)s'
LOG_DEFAULT = 'default_device'
KEY_INPUT = 'key_input'
KEY_INPUTSTRING = 'key_inputstring'
KEY_LONGPRESS = 'key_longpress'
KEY_PRESS = 'key_press'
KEY_RELEASE = 'key_release'
KEYBOARD_CMD_LIST = [
 KEY_INPUT,
 KEY_INPUTSTRING,
 KEY_LONGPRESS,
 KEY_PRESS,
 KEY_RELEASE]
MOUSE_MOVE = 'mouse_move'
MOUSE_PRESS = 'mouse_press'
MOUSE_RELEASE = 'mouse_release'
MOUSE_CLICK = 'mouse_click'
MOUSE_RIGHTCLICK = 'mouse_rightclick'
MOUSE_DOUBLECLICK = 'mouse_doubleclick'
MOUSE_LONGCLICK = 'mouse_longclick'
MOUSE_DRAG = 'mouse_drag'
MOUSE_CMD_LIST = [
 MOUSE_MOVE,
 MOUSE_PRESS,
 MOUSE_RELEASE,
 MOUSE_CLICK,
 MOUSE_RIGHTCLICK,
 MOUSE_DOUBLECLICK,
 MOUSE_LONGCLICK,
 MOUSE_DRAG]