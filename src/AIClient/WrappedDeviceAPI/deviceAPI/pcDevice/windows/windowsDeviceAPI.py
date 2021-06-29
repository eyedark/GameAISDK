# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/windowsDeviceAPI.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 5527 bytes
import time, traceback, logging, win32gui
from ..iPcDeviceAPI import IPcDeviceAPI
from .APIDefine import LOG_DEFAULT
from .win32driver.capture import get_image, roi
from .win32driver.keyboard import Keyboard
from .win32driver.mouse import Mouse, MouseClickType, MouseFlag
from .win32driver.probe import Win32Probe, set_foreground_window
from .win32driver.by import QPath

class WindowsDeviceAPI(IPcDeviceAPI):

    def __init__(self, platform):
        IPcDeviceAPI.__init__(self, platform)
        self._WindowsDeviceAPI__logger = logging.getLogger(LOG_DEFAULT)
        self._is_desktop_window = False
        self._hwnd = None
        self._qpath = None
        self._windows_size = None
        self._kwargs = {}

    def Initialize(self, hwnd=None, query_path=None, window_size=None, **kwargs):
        if not hwnd and query_path is None:
            hwnd = win32gui.GetDesktopWindow()
            self._is_desktop_window = True
        if not hwnd and query_path:
            hwnds = Win32Probe().search_element(QPath(query_path))
            cnt = len(hwnds)
            if cnt > 1:
                raise Exception('found multi windows by qpath(%s)' % query_path)
        else:
            if cnt == 0:
                raise Exception('failed to find window by qpath(%s)' % query_path)
            hwnd = hwnds[0]
        if isinstance(hwnd, str) and hwnd.isdigit():
            hwnd = int(hwnd)
        if not win32gui.IsWindow(hwnd):
            raise ValueError('hwnd(%s) is not valid' % hwnd)
        if window_size:
            l, t, r, b = win32gui.GetWindowRect(hwnd)
            w = r - l
            h = b - t
            if abs(w - window_size[0]) > 50 or abs(h - window_size[1]) > 50:
                raise Exception('window size is not equal, real(%s) != %s' % (str([w, h]), str(window_size)))
        top_hwnd = Win32Probe().get_property(hwnd, 'TOPLEVELWINDOW')
        if top_hwnd:
            set_foreground_window(top_hwnd)
        self._hwnd = hwnd
        self._qpath = query_path
        self._kwargs = kwargs
        self._windows_size = window_size
        return True

    @property
    def window_handle(self):
        return self._hwnd

    def DeInitialize(self):
        return True

    def ScreenCap(self, subrect=None):
        """

        :param subrect:
        :return:
        """
        try:
            img_data = get_image(self._hwnd)
            if img_data is not None and subrect:
                img_data = roi(img_data, subrect)
            return img_data
        except Exception as e:
            self._WindowsDeviceAPI__logger.error('screencap error [{}]'.format(e))
            self._WindowsDeviceAPI__logger.error(traceback.format_exc())
            raise e

    def _to_screen_pos(self, client_pos):
        """ 将相对于窗口的坐标转成屏幕坐标

        :param client_pos:
        :return:
        """
        if self._is_desktop_window:
            return client_pos
        else:
            x, y = client_pos
            rc = win32gui.GetWindowRect(self._hwnd)
            pt = (x + rc[0], y + rc[1])
            return pt

    def PressKey(self, key):
        Keyboard.press_key(key)

    def ReleaseKey(self, key):
        Keyboard.release_key(key)

    def InputKeys(self, keys, long_click_time):
        Keyboard.input_keys(keys)
        if long_click_time > 0:
            time.sleep(long_click_time / 1000)

    def InputStrings(self, key_string):
        Keyboard.input_keys(key_string)

    def MouseMove(self, px, py):
        sx, sy = self._to_screen_pos((px, py))
        Mouse.move(sx, sy)

    def MouseClick(self, px, py, by_post=False):
        if by_post:
            Mouse.post_click(self._hwnd, px, py)
        else:
            sx, sy = self._to_screen_pos((px, py))
            Mouse.click(sx, sy)

    def MouseDoubleClick(self, px, py):
        sx, sy = self._to_screen_pos((px, py))
        Mouse.click(sx, sy, click_type=MouseClickType.DoubleClick)

    def MouseRightClick(self, px, py):
        sx, sy = self._to_screen_pos((px, py))
        Mouse.click(sx, sy, MouseFlag.RightButton)

    def MouseLongClick(self, px, py, long_click_time):
        """

        :param px:
        :param py:
        :param long_click_time: 长按时间，以毫秒为单位
        :return:
        """
        sx, sy = self._to_screen_pos((px, py))
        Mouse.click(sx, sy)
        time.sleep(long_click_time / 1000)

    def MouseDrag(self, from_x, from_y, to_x, to_y):
        """ 从起点(from_x, from_y)拖动到(to_x, to_y)

        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :return:
        """
        sfx, sfy = self._to_screen_pos((from_x, from_y))
        stx, sty = self._to_screen_pos((to_x, to_y))
        Mouse.drag(sfx, sfy, stx, sty)