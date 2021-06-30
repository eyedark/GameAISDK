# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\config.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 2083 bytes
import os, configparser
from enum import Enum, unique

@unique
class DeviceType(Enum):
    Android = 'Android'
    IOS = 'IOS'
    Windows = 'Windows'


@unique
class Platform(Enum):
    Local = 'Local'
    WeTest = 'WeTest'
    GAutomator = 'GAutomator'


class Account(object):
    QQNAME = ''
    QQPWD = ''
    WECHATNAME = ''
    WECHATPWD = ''


class TestInfo(object):
    PACKAGE = 'com.tencent.wetest.demo_ftest'


Unity = 'unity'
UE4 = 'ue4'

class Engine(object):
    Unity = 'unity'
    UE4 = 'ue4'


EngineType = Engine.Unity

class IniConfigParser(object):
    __doc__ = ' ini配置文件的读写类\n\n    '

    def __init__(self, cfg_path):
        if not os.path.exists(cfg_path):
            raise ValueError('file(%s) is not found!' % cfg_path)
        self._IniConfigParser__cfg_path = cfg_path
        self._IniConfigParser__parser = None

    @property
    def parser(self):
        if self._IniConfigParser__parser is None:
            self._IniConfigParser__parser = configparser.ConfigParser()
            self._IniConfigParser__parser.read((self._IniConfigParser__cfg_path), encoding='UTF-8')
        return self._IniConfigParser__parser

    def get(self, section, key):
        """ 获取配置项

        :param section:
        :param key:
        :return:
        """
        if self.parser:
            if section in self.parser:
                if key in self.parser[section]:
                    return self.parser.get(section, key)

    def set(self, section, key, value):
        """ 修改配置项

        :param section:
        :param key:
        :param value:
        :return:
        """
        if self.parser:
            self.parser.set(section, key, value)

    def save(self):
        """ 保存

        :return:
        """
        with open((self._IniConfigParser__cfg_path), 'w', encoding='UTF-8') as (fd):
            self.parser.write(fd)