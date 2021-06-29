# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/devicePlatform/IPlatformProxy.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 3840 bytes
from abc import ABCMeta, abstractmethod
PP_RET_OK = 0
PP_RET_ERR = -1
PP_RET_ERR_SOCKET_EXCEPTION = -2

class DeviceInfo(object):

    def __init__(self):
        self.display_width = None
        self.display_height = None
        self.touch_width = None
        self.touch_height = None
        self.touch_slot_number = None


class IPlatformProxy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def init(self, serial=None, is_portrait=True, long_edge=720, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def deinit(self):
        pass

    @abstractmethod
    def touch_up(self, contact=0):
        raise NotImplementedError()

    @abstractmethod
    def touch_down(self, px, py, contact=0, pressure=50):
        raise NotImplementedError()

    @abstractmethod
    def touch_move(self, px, py, contact=0, pressure=50):
        raise NotImplementedError()

    @abstractmethod
    def touch_wait(self, milliseconds):
        raise NotImplementedError()

    @abstractmethod
    def touch_reset(self):
        raise NotImplementedError()

    @abstractmethod
    def touch_finish(self):
        raise NotImplementedError()

    @abstractmethod
    def get_image(self):
        raise NotImplementedError()

    @abstractmethod
    def get_device_info(self):
        raise NotImplementedError()

    @abstractmethod
    def get_rotation(self):
        raise NotImplementedError()

    def install_app(self, apk_path):
        pass

    def launch_app(self, package_name, activity_name):
        pass

    def exit_app(self, package_name):
        pass

    def current_app(self):
        pass

    def clear_app_data(self, app_package_name):
        pass

    def key(self, key):
        pass

    def text(self, text):
        pass

    def sleep(self):
        pass

    def wake(self):
        pass

    def vm_size(self):
        pass

    def take_screen_shot(self, target_path):
        pass

    def get_screen_ori(self):
        pass

    def adb_click(self, px, py):
        pass

    def adb_swipe(self, sx, sy, ex, ey, duration_ms=50):
        pass

    def device_param(self, packageName):
        pass