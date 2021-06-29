# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/androidDeviceAPI.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 4173 bytes
import sys, logging, logging.config
from .APIDefine import *
from .devicePlatform.WrappedPlatform import PlatformWrapper
from ..iMobileDeviceAPI import IMobileDeviceAPI
WINDOW_DUMP_PATH = 'window_dump.xml'

class AndroidDeviceAPI(IMobileDeviceAPI):

    def __init__(self, platform):
        IMobileDeviceAPI.__init__(self, platform)
        self._AndroidDeviceAPI__platformWrapper = PlatformWrapper(self.platform)

    def Initialize(self, device_serial, is_portrait, long_edge, kwargs):
        return self._AndroidDeviceAPI__platformWrapper.Initialize(device_serial, is_portrait, long_edge, kwargs)

    def DeInitialize(self):
        return self._AndroidDeviceAPI__platformWrapper.DeInitialize()

    def GetFrame(self):
        return self._AndroidDeviceAPI__platformWrapper.GetFrame()

    def InstallAPP(self, APKPath):
        return self._AndroidDeviceAPI__platformWrapper.InstallAPP(APKPath)

    def LaunchAPP(self, PackageName, ActivityName):
        self._AndroidDeviceAPI__platformWrapper.LauchAPP(PackageName, ActivityName)

    def ExitAPP(self, PackageName):
        self._AndroidDeviceAPI__platformWrapper.ExitAPP(PackageName)

    def Click(self, px, py, contact=0, durationMS=-1, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.Click(px, py, contact=contact, durationMS=durationMS)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def Down(self, px, py, contact=0, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.Down(px, py, contact=contact)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def Up(self, contact=0, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.Up(contact=contact)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def SwipeMove(self, px, py, contact=0, durationMS=50, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.SwipeMove(px, py, contact=contact, durationMS=durationMS)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def Swipe(self, sx, sy, ex, ey, contact=0, durationMS=50, needUp=True, wait_time=0):
        if needUp:
            self._AndroidDeviceAPI__platformWrapper.SwipeDownMoveUp(sx, sy, ex, ey, contact=contact, durationMS=durationMS)
        else:
            self._AndroidDeviceAPI__platformWrapper.SwipeDownMove(sx, sy, ex, ey, contact=contact, durationMS=durationMS)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def Move(self, px, py, contact=0, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.Move(px, py, contact)
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def Reset(self, wait_time=0):
        self._AndroidDeviceAPI__platformWrapper.Reset()
        self._AndroidDeviceAPI__platformWrapper.Wait(wait_time * WAITTIME_MS)

    def ADBClick(self, px, py):
        self._AndroidDeviceAPI__platformWrapper.ADBClick(px, py)

    def ADBSwipe(self, sx, sy, ex, ey, durationMS=50):
        self._AndroidDeviceAPI__platformWrapper.ADBSwipe(sx, sy, ex, ey, durationMS)

    def Key(self, key):
        self._AndroidDeviceAPI__platformWrapper.Key(key)

    def Text(self, text):
        self._AndroidDeviceAPI__platformWrapper.Text(text)

    def Wake(self):
        self._AndroidDeviceAPI__platformWrapper.Wake()

    def Sleep(self):
        self._AndroidDeviceAPI__platformWrapper.Sleep()

    def WMSize(self):
        return self._AndroidDeviceAPI__platformWrapper.WMSize()

    def GetScreenResolution(self):
        return self._AndroidDeviceAPI__platformWrapper.GetScreenResolution()

    def CurrentApp(self):
        return self._AndroidDeviceAPI__platformWrapper.CurrentApp()

    def ClearAppData(self, appPackageName):
        self._AndroidDeviceAPI__platformWrapper.ClearAppData(appPackageName)

    def TakeScreenshot(self, targetPath):
        self._AndroidDeviceAPI__platformWrapper.TakeScreenshot(targetPath)

    def GetScreenOri(self):
        return self._AndroidDeviceAPI__platformWrapper.GetScreenOri()

    def GetMaxContact(self):
        return self._AndroidDeviceAPI__platformWrapper.GetMaxContact()

    def GetDeviceParame(self, packageName):
        return self._AndroidDeviceAPI__platformWrapper.DeviceParam(packageName)