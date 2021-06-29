# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/ios/iOSDeviceAPI.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 2572 bytes
from ..iMobileDeviceAPI import IMobileDeviceAPI
from .plugin.PlatformIOS.PlatformIOS import PlatformIOS
from .APIDefineIOS import *

class IOSDeviceAPI(IMobileDeviceAPI):

    def __init__(self, platform):
        IMobileDeviceAPI.__init__(self, platform)
        self._IOSDeviceAPI__platformIOS = PlatformIOS()
        self._IOSDeviceAPI__logger = None

    def Initialize(self, device_serial, is_portrait, long_edge):
        if device_serial is None:
            self._IOSDeviceAPI__logger = logging.getLogger(LOG_DEFAULT)
        else:
            self._IOSDeviceAPI__logger = logging.getLogger(device_serial)
        return self._IOSDeviceAPI__platformIOS.init(device_serial, is_portrait, long_edge)

    def DeInitialize(self):
        return self._IOSDeviceAPI__platformIOS.deinit()

    def GetFrame(self):
        quality = 0.5
        return self._IOSDeviceAPI__platformIOS.get_image(quality)

    def InstallAPP(self, path):
        return self._IOSDeviceAPI__platformIOS.install_app(path)

    def LaunchAPP(self, PackageName, ActivityName):
        self._IOSDeviceAPI__platformIOS.launch_app(PackageName, ActivityName)

    def ExitAPP(self, PackageName):
        self._IOSDeviceAPI__platformIOS.exit_app(PackageName)

    def current_app(self):
        return self._IOSDeviceAPI__platformIOS.current_app()

    def Click(self, px, py, durationMS=-1, wait_time=0):
        if durationMS < 0:
            self._IOSDeviceAPI__platformIOS.click(px, py)
        else:
            self._IOSDeviceAPI__platformIOS.long_tap(px, py, durationMS)

    def Swipe(self, sx, sy, ex, ey, contact=0, durationMS=1000, needUp=True, wait_time=0):
        if needUp:
            self._IOSDeviceAPI__platformIOS.swipe(sx, sy, ex, ey, durationMS)
        else:
            self._IOSDeviceAPI__platformIOS.swipe_hold(sx, sy, ex, ey, durationMS)

    def Reset(self, wait_time=0):
        self._IOSDeviceAPI__platformIOS.touch_reset()

    def Finish(self):
        self._IOSDeviceAPI__logger.info('touch finish')

    def Key(self, key):
        self._IOSDeviceAPI__logger.info('key')

    def Down(self, px, py, contact=0, wait_time=0):
        self._IOSDeviceAPI__logger.info('touch down')

    def Up(self, contact=0, wait_time=0):
        self._IOSDeviceAPI__logger.info('touch up')

    def Move(self, px, py, contact=0, wait_time=0):
        self._IOSDeviceAPI__logger.info('touch move')

    def SwipeMove(self, px, py, contact=0, durationMS=50, wait_time=0):
        self._IOSDeviceAPI__logger.info('swipe move')

    def Wake(self):
        self._IOSDeviceAPI__platformIOS.wake()

    def Sleep(self):
        self._IOSDeviceAPI__platformIOS.sleep()

    def WMSize(self):
        self._IOSDeviceAPI__platformIOS.vm_size()

    def GetMaxContact(self):
        return 0

    def GetScreenResolution(self):
        width, height = self._IOSDeviceAPI__platformIOS.vm_size()
        return (height, width, str())