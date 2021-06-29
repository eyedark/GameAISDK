# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/iPcDeviceAPI.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 612 bytes
from abc import ABCMeta, abstractmethod

class IPcDeviceAPI(object):
    __metaclass__ = ABCMeta

    def __init__(self, platform):
        """
        :param platform:
                    'local': 在本地运行  (必须实现)
                    'wetest': 在wetest运行 (不是必须实现)
        :excetption: 错误信息以异常的形式返回
        """
        self.platform = platform

    @abstractmethod
    def Initialize(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def DeInitialize(self):
        raise NotImplementedError()