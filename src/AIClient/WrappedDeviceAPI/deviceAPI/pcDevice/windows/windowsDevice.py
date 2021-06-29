# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/windowsDevice.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 7545 bytes
import os, sys, logging, traceback
from logging.handlers import RotatingFileHandler
from .windowsDeviceAPI import WindowsDeviceAPI
from .APIDefine import KEYBOARD_CMD_LIST, MOUSE_CMD_LIST, KEY_INPUT, KEY_INPUTSTRING, MOUSE_MOVE, MOUSE_CLICK, MOUSE_DOUBLECLICK, MOUSE_RIGHTCLICK, MOUSE_LONGCLICK, MOUSE_DRAG, LOG_DEFAULT, LOG_FORMAT, KEY_PRESS, KEY_RELEASE
from ...iDevice import IDevice
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)

class WindowsDevice(IDevice):

    def __init__(self, platform):
        IDevice.__init__(self, platform)
        self._WindowsDevice__deviceApi = WindowsDeviceAPI(platform)

    def initialize(self, log_dir, level=logging.DEBUG, hwnd=None, query_path=None, window_size=None, **kwargs):
        if not self._LogInit(log_dir, level):
            raise RuntimeError('init log failed')
        self._WindowsDevice__deviceApi.Initialize(hwnd=hwnd, query_path=query_path, window_size=window_size, **kwargs)
        hwnd = self._WindowsDevice__deviceApi.window_handle
        if hwnd:
            self._WindowsDevice__logger.info('find window:%x' % hwnd)
        self._WindowsDevice__logger.info('logging start')
        return True

    def deInitialize(self):
        return self._WindowsDevice__deviceApi.DeInitialize()

    def getScreen(self, **kwargs):
        img = self._WindowsDevice__deviceApi.ScreenCap(**kwargs)
        return img

    def doAction(self, **kwargs):
        aType = kwargs['aType']
        if aType in KEYBOARD_CMD_LIST:
            return self.keyboardCMD(**kwargs)
        if aType in MOUSE_CMD_LIST:
            return self.mouseCMD(**kwargs)
        raise Exception('unknown action type: {}, {}'.format(aType, kwargs))

    def keyboardCMD(self, **kwargs):
        try:
            aType = kwargs['aType']
            if aType == KEY_INPUT:
                keys = self._GetValuesInkwargs('keys', True, None, kwargs)
                long_click_time = self._GetValuesInkwargs('long_click_time', False, 0, kwargs)
                self._WindowsDevice__logger.info('key input, keys: {0}'.format(keys))
                self._WindowsDevice__deviceApi.InputKeys(keys, long_click_time)
            else:
                if aType == KEY_INPUTSTRING:
                    key_string = kwargs['key_string']
                    self._WindowsDevice__logger.info('key input string, key_string: {0}'.format(key_string))
                    self._WindowsDevice__deviceApi.InputStrings(key_string)
                else:
                    if aType == KEY_PRESS:
                        keys = kwargs['keys']
                        self._WindowsDevice__logger.info('key_press: {0}'.format(keys))
                        self._WindowsDevice__deviceApi.PressKey(keys)
                    elif aType == KEY_RELEASE:
                        keys = kwargs['keys']
                        self._WindowsDevice__logger.info('key_release: {0}'.format(keys))
                        self._WindowsDevice__deviceApi.ReleaseKey(keys)
        except Exception as e:
            self._WindowsDevice__logger.error('keyboardCMD error [{}]'.format(e))
            self._WindowsDevice__logger.error(traceback.format_exc())
            raise e

    def mouseCMD(self, **kwargs):
        try:
            aType = kwargs['aType']
            if aType == MOUSE_MOVE:
                px = self._GetValuesInkwargs('px', True, None, kwargs)
                py = self._GetValuesInkwargs('py', True, None, kwargs)
                self._WindowsDevice__logger.info('mouse move, px: {0}, py: {1}'.format(px, py))
                self._WindowsDevice__deviceApi.MouseMove(px, py)
            else:
                if aType == MOUSE_CLICK:
                    px = self._GetValuesInkwargs('px', True, None, kwargs)
                    py = self._GetValuesInkwargs('py', True, None, kwargs)
                    by_post = kwargs.get('by_post', False)
                    self._WindowsDevice__logger.info('mouse click, px: {0}, py: {1}'.format(px, py))
                    self._WindowsDevice__deviceApi.MouseClick(px, py, by_post)
                else:
                    if aType == MOUSE_DOUBLECLICK:
                        px = self._GetValuesInkwargs('px', True, None, kwargs)
                        py = self._GetValuesInkwargs('py', True, None, kwargs)
                        self._WindowsDevice__logger.info('mouse double click, px: {0}, py: {1}'.format(px, py))
                        self._WindowsDevice__deviceApi.MouseDoubleClick(px, py)
                    else:
                        if aType == MOUSE_RIGHTCLICK:
                            px = self._GetValuesInkwargs('px', True, None, kwargs)
                            py = self._GetValuesInkwargs('py', True, None, kwargs)
                            self._WindowsDevice__logger.info('mouse right click, px: {0}, py: {1}'.format(px, py))
                            self._WindowsDevice__deviceApi.MouseRightClick(px, py)
                        else:
                            if aType == MOUSE_LONGCLICK:
                                px = self._GetValuesInkwargs('px', True, None, kwargs)
                                py = self._GetValuesInkwargs('py', True, None, kwargs)
                                long_click_time = self._GetValuesInkwargs('long_click_time', True, None, kwargs)
                                self._WindowsDevice__logger.info('mouse long click, px: {0}, py: {1}, long_click_time: {2}'.format(px, py, long_click_time))
                                self._WindowsDevice__deviceApi.MouseLongClick(px, py, long_click_time)
                            elif aType == MOUSE_DRAG:
                                fromX = self._GetValuesInkwargs('fromX', True, None, kwargs)
                                fromY = self._GetValuesInkwargs('fromY', True, None, kwargs)
                                toX = self._GetValuesInkwargs('toX', True, None, kwargs)
                                toY = self._GetValuesInkwargs('toY', True, None, kwargs)
                                self._WindowsDevice__logger.info('mouse drag, fromX: {0}, fromY: {1}, toX: {2}, toY: {3}'.format(fromX, fromY, toX, toY))
                                self._WindowsDevice__deviceApi.MouseDrag(fromX, fromY, toX, toY)
        except Exception as e:
            self._WindowsDevice__logger.error('mouseCMD error [{}]'.format(e))
            self._WindowsDevice__logger.error(traceback.format_exc())
            raise e

    def _LogInit(self, log_dir, level):
        try:
            if not isinstance(log_dir, str):
                logging.ERROR('wrong log_dir when init LOG, log_dir:{0}'.format(log_dir))
                return False
            else:
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                self._WindowsDevice__logger = logging.getLogger(LOG_DEFAULT)
                if not self._WindowsDevice__logger.handlers:
                    console = logging.StreamHandler()
                    formatter = logging.Formatter(LOG_FORMAT)
                    console.setFormatter(formatter)
                    fileHandler = RotatingFileHandler(filename=os.path.join(log_dir, 'DeviceAPI.log'), maxBytes=2048000, backupCount=10)
                    fileHandler.setFormatter(formatter)
                    self._WindowsDevice__logger.addHandler(fileHandler)
                    self._WindowsDevice__logger.addHandler(console)
                    self._WindowsDevice__logger.setLevel(level)
                return True
        except Exception as e:
            logging.error(e)
            return False

    def _GetValuesInkwargs(self, key, isNessesary, defaultValue, kwargs):
        try:
            if not isNessesary:
                if key not in kwargs:
                    return defaultValue
                else:
                    return kwargs[key]
            else:
                return kwargs[key]
        except Exception as e:
            self._WindowsDevice__logger.error(e)
            raise e