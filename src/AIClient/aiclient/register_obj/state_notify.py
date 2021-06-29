# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/register_obj/state_notify.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 9046 bytes
import os, sys, configparser, logging
from aiclient.aiclientapi.tool_manage import communicate_config as com_config
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_NOTIFY_CFG_FILE = os.path.join(WORK_DIR, 'cfg/plugin/state_notify.ini')

class StateNotify(object):
    CONFIG_PARAMS_LOAD_ERROR = 1
    EXECUTE_ACTION_THREAD_START_ERROR = 2
    REMOTE_COMMUNICATION_INIT_ERROR = 3
    NONE_FRAME_EXCEPTION = 4
    FINISH_EXCEPTION = 5
    ADB_TOOL_INIT_EXCEPTION = 6
    ARGS_VERIFY_EXCEPTION = 7
    AI_SDK_ERROR = 8
    BAD_DEVICE_EXCEPTION = 9

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.obj_inst = None
        self.task_id = None
        self.use_state_plugin = False
        self.state_package = None
        self.state_module = None
        self.state_class = None

    def init(self):
        ret, config, error_str = self.load_parameter(STATE_NOTIFY_CFG_FILE)
        if not ret:
            return (False, error_str)
        ret, error_str = self.load_plugin_parameter(config)
        if not ret:
            return (False, error_str)
        ret, error_str = self.create_state_notify_obj()
        if not ret:
            return (False, error_str)
        return (True, '')

    def load_parameter(self, cfg_file):
        if not os.path.exists(cfg_file):
            self.MAIN_THREAD_LOGGER.error('cfg_file not exist:{}'.format(cfg_file))
            return (False, None, 'cfg_file not exist:{}'.format(cfg_file))
        else:
            try:
                config = configparser.ConfigParser(strict=False)
                config.read(cfg_file)
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('read state_notify config file error: {}'.format(err))
                return (False, None, 'read state_notify config file error: {}'.format(err))

            return (True, config, '')

    def load_plugin_parameter(self, config):
        try:
            self.use_state_plugin = config.getint('state', 'use_plugin')
            self.state_package = config.get('state', 'package')
            self.state_module = config.get('state', 'module')
            self.state_class = config.get('state', 'class')
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('load plugin parameter error: {}'.format(err))
            return (False, 'load plugin parameter error: {}'.format(err))

        return (True, '')

    def create_state_notify_obj(self):
        if not self.use_state_plugin:
            self.MAIN_THREAD_LOGGER.warning('do not use plugin for state notify, transfer to using register obj')
        try:
            plugin_path = os.path.join(WORK_DIR, 'plugin')
            sys.path.append(plugin_path)
            module_path = '{}.{}'.format(self.state_package, self.state_module)
            package = __import__(module_path)
            module_name = getattr(package, self.state_module)
            class_name = getattr(module_name, self.state_class)
            self.MAIN_THREAD_LOGGER.info('state plugin, module_path:{}, package:{}, module_name:{}, class_name:{}'.format(module_path, package, module_name, class_name))
            self.obj_inst = class_name()
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('load state_notify instance error: {}'.format(err))
            return (False, 'load state_notify instance error: {}'.format(err))

        return (True, '')

    def register_obj(self, obj):
        self.obj_inst = obj

    def set_taskid(self, task_id):
        self.task_id = task_id

    def obj_is_none(self):
        if self.obj_inst is None:
            self.MAIN_THREAD_LOGGER.error('obj has no loaded')
            return True
        else:
            return False

    def on_start(self):
        """this function will be called when game enter scene and detect begin"""
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_start(task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.debug('call on_start successfully')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_start error:{}'.format(err))

    def on_restore(self):
        """this function will be called when restore actions execution"""
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_resume(task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.debug('call on_restore successfully')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_restore error:{}'.format(err))

    def on_pause(self):
        """this function will be called when stop actions execution"""
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_pause(task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.debug('call on_pause successfully')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_pause error:{}'.format(err))

    def on_stop(self):
        """this function will be called when current round detect game over"""
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_stop(task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.debug('call on_stop successfully')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_stop error:{}'.format(err))

    def on_service_over(self):
        """this function will be called when all the service over"""
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_service_over(task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.debug('call on_service_over successfully')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_service_over error:{}'.format(err))

    def on_ai_service_state(self, state):
        """notify ai-sdk service state, -1 ai-sdk service is abnormal, 0 ai-sdk service is ok"""
        if self.obj_is_none():
            return
            try:
                if state == com_config.AI_SERVICE_ABNORMAL:
                    self.MAIN_THREAD_LOGGER.error('call on_ai_service_state error, state:{}'.format(state))
                else:
                    if state == com_config.AI_SERVICE_READY:
                        self.MAIN_THREAD_LOGGER.debug('call on_ai_service_state successfully, state:{}'.format(state))
                    else:
                        self.MAIN_THREAD_LOGGER.error('call on_ai_service_state error, no define state:{}'.format(state))
                self.obj_inst.on_ai_service_state(state=state, task_id=self.task_id)
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_ai_service_state error:{}, state:{}'.format(err, state))

    def on_resource_apply_state(self, state, description=''):
        """notify resource apply state, -2 resource apply failed, -1 network abnormal,
            0 network connecting, 1 success
        """
        if self.obj_is_none():
            return
            try:
                if state == com_config.RESOURCE_APPLY_FAILURE:
                    self.MAIN_THREAD_LOGGER.error('call on_resource_apply_state error, resource apply failure, state:{}'.format(state))
                else:
                    if state == com_config.NETWORK_ABNORMAL:
                        self.MAIN_THREAD_LOGGER.error('call on_resource_apply_state error, network abnormal, state:{}'.format(state))
                    else:
                        if state == com_config.NETWORK_CONNECTTING:
                            self.MAIN_THREAD_LOGGER.debug('call on_resource_apply_state, connecting network, state:{}'.format(state))
                        else:
                            if state == com_config.RESOURCE_APPLY_SUCCESS:
                                self.MAIN_THREAD_LOGGER.debug('call on_resource_apply_state, resource apply successful, state:{}'.format(state))
                            else:
                                self.MAIN_THREAD_LOGGER.error('call on_resource_apply_state error, no define state:{}'.format(state))
                self.obj_inst.on_resource_apply_state(state=state, description='', task_id=self.task_id)
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call resource_apply_state error:{}, state:{}'.format(err, state))

    def on_exception(self, exception_type, description):
        if self.obj_is_none():
            return
            try:
                self.obj_inst.on_exception(exception_type=exception_type, description=description, task_id=self.task_id)
                self.MAIN_THREAD_LOGGER.error('call on_exception notify error, exception_type:{}, description: {}'.format(exception_type, description))
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('call on_exception error:{}, exception_type:{}, description: {}'.format(err, exception_type, description))