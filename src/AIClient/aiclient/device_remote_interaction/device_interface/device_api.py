# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\device_interface\device_api.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 12768 bytes
import sys, json, logging, os, traceback
from .config import Platform, DeviceType, IniConfigParser
from WrappedDeviceAPI.deviceAdapter import DeviceAdapter
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
DEVICE_CFG_PATH = os.path.join(WORK_DIR, 'cfg/device_cfg/device.ini')
DO_ACTION_TYPE = 'dact_minitouch'
DEFAULT_HEIGHT = 720
DEFAULT_WIDTH = 1280
GAUTOMATOR_PACKAGE = 'GAutomatorAndroid'
GAUTOMATOR_MODULE = 'platformCODM'
GAUTOMATOR_CLASS = 'PlatformCODM'

class DeviceAPI(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.device_api = None
        self.ready = False
        self.use_env_variable = 0
        self.device_type = None
        self.platform = None
        self.long_edge = None
        self.max_restart_time = None
        self.log_dir = None
        self.log_level = None
        self.device_serial = None
        self.is_portrait = 0
        self.show_screen = 0
        self.foregroundwin_only = 1
        self.win_names = None
        self._windows_size = None
        self._query_path = None

    def load_parameter(self, device_cfg_path):
        if not os.path.exists(device_cfg_path):
            return (False, 'device_cfg_path not exist:{}'.format(device_cfg_path))
        else:
            config = IniConfigParser(device_cfg_path).parser
            if 'device' not in config:
                return (False, 'device.ini config file not contain device section')
            if 'log' not in config:
                return (False, 'device.ini config file not contain log section')
            if 'mobile_device' not in config:
                return (False, 'device.ini config file not contain mobile_device section')
            if 'pc_device' not in config:
                return (False, 'device.ini config file not contain pc_device section')
            if 'use_env_variable' in config['device']:
                self.use_env_variable = int(config['device']['use_env_variable'])
            else:
                return (False, 'device.ini config file cannot contain use_env_variable')
            if 'device_type' in config['device']:
                self.device_type = config['device']['device_type']
            else:
                return (False, 'source info not contain device_type')
            if self.device_type not in DeviceType.__members__.keys():
                err_info = 'source info Unknown device_type {}, should be one of {}'.format(self.device_type, DeviceType.__members__.keys())
                return (False, err_info)
            if 'platform' in config['device']:
                self.platform = config['device']['platform']
            else:
                return (False, 'source info not contain platform')
            if self.platform not in Platform.__members__.keys():
                err_info = 'source info Unknown platform {}, shouled be one of {}'.format(self.platform, Platform.__members__.keys())
                return (False, err_info)
            if 'long_edge' in config['device']:
                self.long_edge = int(config['device']['long_edge'])
            else:
                return (False, 'source info cannot contain long_edge')
            if 'max_restart_time' in config['device']:
                self.max_restart_time = config.getint('device', 'max_restart_time')
            else:
                return (False, 'device.ini config file cannot contain max_restart_time')
            if 'log_dir' in config['log']:
                self.log_dir = config.get('log', 'log_dir')
            else:
                return (False, 'device.ini config file cannot contain log_dir')
            if 'level' in config['log']:
                self.log_level = self.log_level_parse(config.get('log', 'level'))
            else:
                return (False, 'device.ini config file cannot contain log level')
            if 'device_serial' in config['mobile_device']:
                self.device_serial = config.get('mobile_device', 'device_serial')
                if self.device_serial == '':
                    self.device_serial = None
            else:
                return (False, 'device.ini config file not contain device_serial')
            if 'is_portrait' in config['mobile_device']:
                self.is_portrait = config.getint('mobile_device', 'is_portrait')
            else:
                return (False, 'device.ini config file cannot contain is_portrait')
            if 'show_raw_screen' in config['mobile_device']:
                self.show_screen = config.getboolean('mobile_device', 'show_raw_screen')
            else:
                return (False, 'device.ini config file cannot contain show_raw_screen')
            if 'foregroundwin_only' in config['pc_device']:
                self.foregroundwin_only = config.getboolean('pc_device', 'foregroundwin_only')
            else:
                return (False, 'device.ini config file cannot contain foregroundwin_only')
            if 'win_names' in config['pc_device']:
                self.win_names = config.get('pc_device', 'win_names')
                self.win_names = self.win_names.split('|')
            else:
                return (False, 'device.ini config file cannot contain win_names')
            if 'window_size' in config['pc_device']:
                window_size = config.get('pc_device', 'window_size')
                if window_size:
                    self._windows_size = json.loads(window_size)
            if 'query_path' in config['pc_device']:
                self._query_path = config.get('pc_device', 'query_path')
            if self.use_env_variable:
                self.MAIN_THREAD_LOGGER.info('use_env_variable resolution')
                try:
                    self.long_edge = int(os.environ.get('IMG_LONG_EDGE'))
                    self.is_portrait = int(os.environ.get('IS_PORTRAIT'))
                    self.is_portrait = True if self.is_portrait == 1 else False
                except Exception as err:
                    return (
                     False, 'get long_edge or is_portrait from env error: {}'.format(err))

            return (True, '')

    def init(self):
        ret, err = self.load_parameter(DEVICE_CFG_PATH)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('load_parameter error:{}'.format(err))
            return (False, err)
        self.MAIN_THREAD_LOGGER.info('device_type: {}, platform: {}'.format(self.device_type, self.platform))
        try:
            if self.platform == Platform.GAutomator.value:
                self.device_api = self.get_gautomator_instance()
            else:
                self.device_api = DeviceAdapter(self.device_type, self.platform)
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('device api long_edge failed')
            return (False, err)

        try:
            self.MAIN_THREAD_LOGGER.info("Try detect device type...")
            if self.device_type == DeviceType.Android.value:
                if self.platform == Platform.GAutomator.value:
                    ret = self.device_api.init()
                else:
                    self.device_api.initialize(log_dir=(self.log_dir), level=(self.log_level),
                      long_edge=(self.long_edge),
                      device_serial=(self.device_serial),
                      show_raw_screen=(self.show_screen))
                self.ready = True
            else:
                if self.device_type == DeviceType.IOS.value:
                    self.device_api.initialize(log_dir=(self.log_dir), level=(self.log_level),
                      long_edge=(self.long_edge),
                      device_serial=(self.device_serial),
                      show_raw_screen=(self.show_screen))
                elif self.device_type == DeviceType.Windows.value:
                    self.device_api.initialize(log_dir=(self.log_dir), level=(self.log_level),
                      hwnd=(self.device_serial),
                      window_size=(self._windows_size),
                      query_path=(self._query_path))
                self.ready = True
        except:
            exp = traceback.format_exc()
            self.MAIN_THREAD_LOGGER.error('device api initializes failed: {}'.format(exp))
            self.device_api = None
            self.ready = False
            return (False, err)
        else:
            return (True, '')

    def finish(self):
        if self.device_api is not None:
            try:
                try:
                    if self.device_type == DeviceType.Android.value:
                        if self.platform == Platform.GAutomator.value:
                            return self.device_api.DeInitialize()
                    return self.device_api.deInitialize()
                except Exception as err:
                    self.MAIN_THREAD_LOGGER.error('finish failed: {}'.format(err))

            finally:
                self.ready = False
                self.device_api = None

        return True

    def restart(self):
        self.MAIN_THREAD_LOGGER.info('restart device...')
        try:
            self.finish()
            self.MAIN_THREAD_LOGGER.info('  device finished..')
            flag, _ = self.init()
            if not flag:
                self.MAIN_THREAD_LOGGER.info('  device restart failed..')
                self.finish()
                return False
            self.MAIN_THREAD_LOGGER.info('  device restarted..')
            return True
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('device restart failed: {}'.format(err))
            return False

    def get_gautomator_instance(self):
        PLUGIN_PATH = os.path.join(WORK_DIR, 'plugin')
        sys.path.append(PLUGIN_PATH)
        module_path = '{}.{}'.format(GAUTOMATOR_PACKAGE, GAUTOMATOR_MODULE)
        package = __import__(module_path)
        module_name = getattr(package, GAUTOMATOR_MODULE)
        class_name = getattr(module_name, GAUTOMATOR_CLASS)
        self.MAIN_THREAD_LOGGER.info('gautomator plugin, module_path:{}, package:{}, module_name:{}, class_name:{}'.format(module_path, package, module_name, class_name))
        return class_name()

    def log_level_parse(self, log_level_str):
        if log_level_str == 'LOG_DEBUG':
            return logging.DEBUG
        else:
            if log_level_str == 'LOG_INFO':
                return logging.INFO
            else:
                if log_level_str == 'LOG_WARNING':
                    return logging.WARN
                if log_level_str == 'LOG_ERROR':
                    return logging.ERROR
                if log_level_str == 'LOG_CRITICAL':
                    return logging.CRITICAL
            self.MAIN_THREAD_LOGGER.warning('log level is not correct, using info level')
            return logging.INFO

    def GetFrame(self):
        if not self.ready:
            self.MAIN_THREAD_LOGGER.warning('device_api is not ready')
            return (None, None, 'device_api not ready')
        else:
            if self.device_type == DeviceType.Android.value:
                if self.platform == Platform.GAutomator.value:
                    img, extend_data = self.device_api.GetFrame()
                    return (
                     img, extend_data, '')
            img = self.device_api.getScreen()
            return (img, None, '')

    def do_action(self, **kwargs):
        if not self.ready:
            self.MAIN_THREAD_LOGGER.warning('device_api is not ready')
        else:
            if self.platform == Platform.GAutomator.value:
                (self.device_api.DoAction)(**kwargs)
            else:
                (self.device_api.doAction)(**kwargs)


device_api_inst = None

def get_device_api_instance():
    global device_api_inst
    if device_api_inst is None:
        device_api_inst = DeviceAPI()
        ret, err = device_api_inst.init()
        if not ret:
            raise Exception(err)
    return device_api_inst