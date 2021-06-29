# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/devicePlatform/IPlatformProxy.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 1587 bytes
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

    def __repr__(self):
        return ' display_width:{}, display_height={}, touch_width={}, touch_height={}, touch_slot_number={} ]'.format(self.display_width, self.display_height, self.touch_width, self.touch_height, self.touch_slot_number)


class IPlatformProxy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def init(self, serial=None, is_portrait=True, height=1280, showscreen=True, **kwargs):
        pass

    @abstractmethod
    def deinit(self):
        pass

    @abstractmethod
    def touch_up(self, contact=0):
        pass

    @abstractmethod
    def touch_down(self, px, py, contact=0, pressure=50):
        pass

    @abstractmethod
    def touch_move(self, px, py, contact=0, pressure=50):
        pass

    @abstractmethod
    def touch_wait(self, milliseconds):
        pass

    @abstractmethod
    def touch_reset(self):
        pass

    @abstractmethod
    def touch_finish(self):
        pass

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def get_device_info(self):
        pass

    @abstractmethod
    def get_rotation(self):
        pass