# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAdapter.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 3714 bytes
import os, sys, cv2
from datetime import datetime
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
from .wrappedDevice_config import Platform, DeviceType, LOG_DIR, SAVE_PIC

class DeviceAdapter(object):

    def __init__(self, device_type, platform=Platform.Local.value):
        """
        :param device_type: 'Android'|'IOS'|'Windows'
        :param platform: 'Local'|'WeTest'
        """
        self.device_type = device_type
        self.platform = platform
        self.log_dir = None
        self.picDir = None
        self._DeviceAdapter__device = None
        try:
            if self.device_type == DeviceType.Android.value:
                from .deviceAPI.mobileDevice.android.androidDevice import AndroidDevice
                self._DeviceAdapter__device = AndroidDevice(platform)
            else:
                if self.device_type == DeviceType.IOS.value:
                    from .deviceAPI.mobileDevice.ios.iOSDevice import IOSDevice
                    self._DeviceAdapter__device = IOSDevice(platform)
                else:
                    if self.device_type == DeviceType.Windows.value:
                        from .deviceAPI.pcDevice.windows.windowsDevice import WindowsDevice
                        self._DeviceAdapter__device = WindowsDevice(platform)
                    else:
                        raise Exception('Unknown device type: {}'.format(self.device_type))
        except Exception as err:
            raise Exception(err)

    def initialize(self, log_dir=LOG_DIR, **kwargs):
        """
        初始化设备
        :param log_dir: str, 日志保存路径
        :param kwargs: self.__device.initialize查看对应实现
        :return: True/False
        """
        self.log_dir = os.path.join(log_dir, self.device_type)
        self.picDir = os.path.join(self.log_dir, 'pic')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if not os.path.exists(self.picDir):
            os.makedirs(self.picDir)
        try:
            return self._DeviceAdapter__device.initialize(self.log_dir, **kwargs)
        except Exception as err:
            raise Exception(err)

    def deInitialize(self):
        """
        回收设备资源
        :return: True/False
        """
        try:
            return self._DeviceAdapter__device.deInitialize()
        except Exception as err:
            raise Exception(err)

    def getScreen(self, **kwargs):
        """
        获取当前图像帧
        :return: Mat类型的图像/None
        """
        try:
            return self._DeviceAdapter__device.getScreen(**kwargs)
        except Exception as err:
            raise Exception(err)

    def doAction(self, **kwargs):
        """
        操作设备
        :param kwargs: 格式{"aType": "xxx", "param1": _, "param2":, _}, self.__device.doAction查看对应实现;
        :return: True/False
        """
        if 'aType' not in kwargs:
            raise Exception('got an action without aType: {}'.format(kwargs))
        else:
            try:
                filename = datetime.now().strftime('%m-%d_%H-%M-%S_%f.jpg')
                filepath = os.path.join(self.picDir, filename)
                if SAVE_PIC:
                    while True:
                        try:
                            img_data = self.getScreen()
                            if img_data is not None:
                                pass
                            cv2.imwrite(filepath, img_data)
                            break
                        except Exception as err:
                            continue

                return self._DeviceAdapter__device.doAction(**kwargs)
            except Exception as err:
                raise Exception(err)