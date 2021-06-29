# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/devicePlatform/WrappedPlatform.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 9742 bytes
import re, numpy as np
from ..APIDefine import *
from ..plugin.getPlatformInstance import GetPlatformInstance
from ..plugin.Platform_plugin.PlatformWeTest.demo.common.AdbTool import AdbTool

class ADBClient(object):

    def __init__(self, serial=None):
        self._adb = AdbTool(serial)

    def shell_cmd(self, *args):
        output, err = self._adb.cmd('shell', *args).communicate()
        if output:
            return output.decode('utf-8', 'ignore').strip()

    def input_keys(self, keys, repeat=1):
        if keys.startswith('{') and keys.endswith('}'):
            keyValues = {'{HOME}': 3, '{BACK}': 4, '{MENU}': 82, '{VOLUME_UP}': 24, 
             '{VOLUME_DOWN}': 25, '{POWER}': 26, '{TAB}': 61, 
             '{ENTER}': 66, '{SPACE}': 62, '{DEL}': 67, '{END}': 6, '{SEARCH}': 84, 
             '{MOVE_END}': 123, '{MOVE_HOME}': 122, '{ESCAPE}': 111, 
             '{DOUBLEHOME}': '3 3', '{DOUBLEMENU}': '82 82', '{LONGHOME}': '--longpress 3', '{LONGMENU}': '--longpress 82', 
             '{APP_SWITCH}': 187, '{ESC}': 111}
            if keys in keyValues:
                value = str(keyValues[keys])
                if repeat > 1:
                    value = ' '.join([value for i in range(repeat)])
                cmd = 'input keyevent "' + value + '"'
                self.shell_cmd(cmd)
            else:
                raise ValueError('输入的不是特殊字符，非特殊字符不需要用{}括起来。')
        else:
            mos = re.findall('(\\s*)([^\\s]+)(\\s*)', keys)
            for mo in mos:
                if mo[0]:
                    for _ in range(len(mo[0])):
                        cmd = 'input keyevent SPACE'
                        self.shell_cmd(cmd)

                cmd = "input text '%s'" % mo[1]
                self.shell_cmd(cmd)
                if mo[2]:
                    for _ in range(len(mo[2])):
                        cmd = 'input keyevent SPACE'
                        self.shell_cmd(cmd)


class PlatformWrapper(object):

    def __init__(self, platform):
        self._PlatformWrapper__platform = platform
        self._PlatformWrapper__actionClass = None
        self._PlatformWrapper__platformInstance = None
        self._PlatformWrapper__contactState = []
        self._PlatformWrapper__logger = None
        self._PlatformWrapper__adb_client = None

    def Initialize(self, serial=None, is_portrait=False, long_edge=1280, kwargs=None):
        if serial is None:
            self._PlatformWrapper__logger = logging.getLogger(LOG_DEFAULT)
        else:
            self._PlatformWrapper__logger = logging.getLogger(serial)
        self._PlatformWrapper__logger.info('platform: {}'.format(self._PlatformWrapper__platform))
        self._PlatformWrapper__platformInstance = GetPlatformInstance(serial, self._PlatformWrapper__platform)
        if self._PlatformWrapper__platformInstance is None:
            self._PlatformWrapper__logger.error('get platform class failed')
            return (False, 'get platform class failed')
        self._PlatformWrapper__logger.info('get platform class succeed')
        ret, strError = self._PlatformWrapper__platformInstance.init(serial, True, long_edge, **kwargs)
        if ret is False:
            self._PlatformWrapper__logger.error('platform init failed: {}'.format(strError))
            return (
             False, strError)
        self._PlatformWrapper__logger.info('platform init successful')
        self._PlatformWrapper__contactState = [None] * self.GetMaxContact()
        self._PlatformWrapper__adb_client = ADBClient(serial)
        return (True, str())

    def DeInitialize(self):
        self._PlatformWrapper__platformInstance.deinit()
        return True

    def GetFrame(self):
        PPRET, ScreenImg = self._PlatformWrapper__platformInstance.get_image()
        if PPRET != 0:
            self._PlatformWrapper__logger.error('Get frame failed, error code:{0}'.format(PPRET))
        return (PPRET, ScreenImg)

    def Down(self, px, py, contact=0, pressure=50):
        self._PlatformWrapper__platformInstance.touch_down(px, py, contact, pressure)
        self._PlatformWrapper__contactState[contact] = (
         px, py)

    def Up(self, contact=0):
        self._PlatformWrapper__platformInstance.touch_up(contact)
        self._PlatformWrapper__contactState[contact] = None

    def Move(self, px, py, contact=0, pressure=50):
        self._PlatformWrapper__platformInstance.touch_move(px, py, contact, pressure)
        if self._PlatformWrapper__contactState[contact] is not None:
            self._PlatformWrapper__contactState[contact] = (
             px, py)
        else:
            self._PlatformWrapper__logger.warning('contact {0} not down when move to ({1}, {2})'.format(contact, px, py))

    def SwipeMove(self, px, py, contact=0, durationMS=50, pressure=50):
        if self._PlatformWrapper__contactState[contact] is not None:
            self._AddPoint(self._PlatformWrapper__contactState[contact][0], self._PlatformWrapper__contactState[contact][1], px, py, contact, durationMS, pressure)
        else:
            self._PlatformWrapper__logger.warning('contact {0} not down when swipemove to ({1}, {2})'.format(contact, px, py))

    def Click(self, px, py, contact=0, durationMS=-1, pressure=50):
        if durationMS < 0:
            durationMS = 50
        self.Down(px, py, contact, pressure)
        self.Wait(durationMS)
        self.Up(contact)

    def UpAll(self):
        for contact in range(self.GetMaxContact()):
            self.Up(contact)

    def SwipeDownMoveUp(self, sx, sy, ex, ey, contact=0, durationMS=50, pressure=50):
        self.Up(contact)
        self.Down(sx, sy, contact, pressure)
        self.Wait(WAITTIME_POINT)
        self._AddPoint(sx, sy, ex, ey, contact, durationMS, pressure)
        self.Up(contact)

    def SwipeDownMove(self, sx, sy, ex, ey, contact=0, durationMS=50, pressure=50):
        self.Up(contact)
        self.Down(sx, sy, contact, pressure)
        self.Wait(WAITTIME_POINT)
        self._AddPoint(sx, sy, ex, ey, contact, durationMS, pressure)

    def Wait(self, waitMS):
        self._PlatformWrapper__platformInstance.touch_wait(waitMS)

    def GetScreenResolution(self):
        deviciInfo, strError = self._PlatformWrapper__platformInstance.get_device_info()
        if deviciInfo is None:
            return (-1, -1, strError)
        return (deviciInfo.display_height, deviciInfo.display_width, str())

    def GetMaxContact(self):
        deviciInfo, strError = self._PlatformWrapper__platformInstance.get_device_info()
        if deviciInfo is None:
            raise Exception('get contact number failed')
        return deviciInfo.touch_slot_number

    def Reset(self):
        self._PlatformWrapper__platformInstance.touch_reset()

    def Finish(self):
        self._PlatformWrapper__platformInstance.touch_finish()

    def InstallAPP(self, APKPath):
        raise NotImplementedError

    def LauchAPP(self, PackageName, ActivityName):
        raise NotImplementedError

    def ExitAPP(self, PackageName):
        raise NotImplementedError

    def CurrentApp(self):
        raise NotImplementedError

    def ClearAppData(self, appPackageName):
        raise NotImplementedError

    def Key(self, key):
        self._PlatformWrapper__adb_client.input_keys(key)

    def Text(self, text):
        self._PlatformWrapper__adb_client.input_keys(text)

    def Sleep(self):
        raise NotImplementedError

    def Wake(self):
        raise NotImplementedError

    def WMSize(self):
        raise NotImplementedError

    def TakeScreenshot(self, targetPath):
        raise NotImplementedError
        self._PlatformWrapper__platformInstance.take_screen_shot(targetPath)

    def GetScreenOri(self):
        raise NotImplementedError

    def ADBClick(self, px, py):
        raise NotImplementedError

    def ADBSwipe(self, sx, sy, ex, ey, durationMS=50):
        raise NotImplementedError

    def DeviceParam(self, packageName):
        raise NotImplementedError

    def _AddPoint(self, sx, sy, ex, ey, contact=0, durationMS=50, pressure=50):
        beginPoint = np.array([sx, sy])
        targetPoint = np.array([ex, ey])
        numMovingPoints = int(durationMS / WAITTIME_POINT)
        movingX = np.linspace(beginPoint[0], targetPoint[0], numMovingPoints).astype(int)
        movingY = np.linspace(beginPoint[1], targetPoint[1], numMovingPoints).astype(int)
        for i in range(numMovingPoints - 1):
            self.Move(movingX[(i + 1)], movingY[(i + 1)], contact=contact, pressure=pressure)
            self.Wait(WAITTIME_POINT)