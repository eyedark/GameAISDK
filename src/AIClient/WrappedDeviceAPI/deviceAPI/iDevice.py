# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/iDevice.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 1769 bytes
from abc import ABCMeta, abstractmethod

class IDevice(object):
    __metaclass__ = ABCMeta
    actions = []

    def __init__(self, platform):
        """
        :param platform:
                    'Local': 在本地运行  (必须实现)
                    'WeTest': 在wetest运行 (不是必须实现)
        :excetption: 错误信息以异常的形式返回
        """
        self.platform = platform

    @abstractmethod
    def initialize(self, log_dir, **kwargs):
        """
        初始化设备
        :param log_dir: str, 指定日志目录（由WrappedDeviceAPI指定）
        :param kwargs: 实现时定义
        :return: True/False
        :excetption: 错误信息以异常的形式返回
        """
        raise NotImplementedError()

    @abstractmethod
    def deInitialize(self):
        """
        回收设备资源
        :return: True/False
        :excetption: 错误信息以异常的形式返回
        """
        raise NotImplementedError()

    @abstractmethod
    def getScreen(self, **kwargs):
        """
        获取当前图像帧
        :return: Mat类型的图像/None
        :excetption: 错误信息以异常的形式返回
        """
        raise NotImplementedError()

    @abstractmethod
    def doAction(self, **kwargs):
        """
        执行动作
        :param kwargs: 实现时定义, 格式{"aType": "xxx", "param1": _, "param2":, _}
        :return: True/False
        :excetption: 错误信息以异常的形式返回
        """
        raise NotImplementedError()