# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\tool_manage\parameter_context.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 6817 bytes
import os, configparser, logging

class ParameterContext(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.para_data = {}

    def init(self, cfg_file):
        return self.load_parameter(cfg_file)

    def load_parameter(self, cfg_file):
        if not os.path.exists(cfg_file):
            self.MAIN_THREAD_LOGGER.error('cfg_file not exist:{}'.format(cfg_file))
            return (
             False, None, 'cfg_file not exist:{}'.format(cfg_file))
        else:
            config = configparser.ConfigParser(strict=False)
            config.read(cfg_file)
            ret, error_str = self.load_ip(config)
            if not ret:
                return (
                 ret, None, error_str)
            ret, error_str = self.load_monitor(config)
            if not ret:
                return (
                 ret, None, error_str)
            ret, error_str = self.load_resource_apply(config)
            if not ret:
                return (ret, None, error_str)
            return (
             True, self.para_data.copy(), '')

    def load_ip(self, config):
        if not config.__contains__('IP'):
            self.MAIN_THREAD_LOGGER.error('config file not contain IP section, please check config file first')
            return (False, 'config file not contain IP section')
        else:
            if not config['IP'].__contains__('ip'):
                self.MAIN_THREAD_LOGGER.error('config file not contain ip')
                return (False, 'config file not contain ip')
            else:
                self.para_data['ip'] = config.get('IP', 'ip')
                if not config['IP'].__contains__('port1'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain port1')
                    return (False, 'config file not contain port1')
                self.para_data['port1'] = config.getint('IP', 'port1')
                if not config['IP'].__contains__('port2'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain port2')
                    return (False, 'config file not contain port2')
                self.para_data['port2'] = config.getint('IP', 'port2')
                if not config['IP'].__contains__('send_pattern'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain send_pattern')
                    return (False, 'config file not contain send_pattern')
                self.para_data['send_pattern'] = config.getint('IP', 'send_pattern')
                if not config['IP'].__contains__('recv_pattern'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain recv_pattern')
                    return (False, 'config file not contain recv_pattern')
                self.para_data['recv_pattern'] = config.getint('IP', 'recv_pattern')
                if not config['IP'].__contains__('save_last_action'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain save_last_action')
                    return (False, 'config file not contain save_last_action')
                self.para_data['save_last_action'] = config.getint('IP', 'save_last_action')
                if not config['IP'].__contains__('key'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain key')
                    return (False, 'config file not contain key')
                else:
                    self.para_data['key'] = config.get('IP', 'key')
                    if not config['IP'].__contains__('comm_type'):
                        self.MAIN_THREAD_LOGGER.error('config file not contain comm_type')
                        return (False, 'config file not contain comm_type')
                    self.para_data['comm_type'] = config.getint('IP', 'comm_type')
                    if not config['IP'].__contains__('use_env_variable'):
                        self.MAIN_THREAD_LOGGER.error('config file not contain use_env_variable')
                        return (False, 'config file not contain use_env_variable')
                    self.para_data['use_env_variable'] = config.getint('IP', 'use_env_variable')
            return (True, '')

    def load_monitor(self, config):
        if not config.__contains__('MONITOR'):
            self.MAIN_THREAD_LOGGER.error('config file not contain MONITOR section, please check config file first')
            return (False, 'config file not contain MONITOR section')
        else:
            if not config['MONITOR'].__contains__('process_speed_test'):
                self.MAIN_THREAD_LOGGER.error('config file not contain process_speed_test')
                return (False, 'config file not contain process_speed_test')
            else:
                self.para_data['process_speed_test'] = config.getint('MONITOR', 'process_speed_test')
                if not config['MONITOR'].__contains__('frame_decode_type'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain frame_decode_type')
                    return False
                self.para_data['frame_decode_type'] = config.getint('MONITOR', 'frame_decode_type')
                if not config['MONITOR'].__contains__('max_send_interval'):
                    self.MAIN_THREAD_LOGGER.error('config file not contain max_send_interval')
                    return (False, 'config file not contain max_send_interval')
                else:
                    self.para_data['max_send_interval'] = config.getfloat('MONITOR', 'max_send_interval')
                    if not config['MONITOR'].__contains__('max_none_frame_time'):
                        self.MAIN_THREAD_LOGGER.error('config file not contain max_none_frame_time')
                        return (False, 'config file not contain max_none_frame_time')
                    self.para_data['max_none_frame_time'] = config.getfloat('MONITOR', 'max_none_frame_time')

                    if not config['MONITOR'].__contains__('max_none_action_time'):
                        self.MAIN_THREAD_LOGGER.error('config file not contain max_none_action_time')
                        return (False, 'config file not contain max_none_action_time')
                    self.para_data['max_none_action_time'] = config.getfloat('MONITOR', 'max_none_action_time')
            return (True, '')

    def load_resource_apply(self, config):
        if not config.__contains__('resource_apply'):
            self.MAIN_THREAD_LOGGER.error('config file not contain resource_apply section, please check config file first')
            return (False, 'config file not contain resource_apply section')
        else:
            if os.environ.get('AUTO_APPLY_RESOURCE'):
                self.para_data['auto_apply_resource'] = int(os.environ.get('AUTO_APPLY_RESOURCE'))
            else:
                if config['resource_apply'].__contains__('auto_apply_resource'):
                    self.para_data['auto_apply_resource'] = config.getint('resource_apply', 'auto_apply_resource')
                else:
                    self.MAIN_THREAD_LOGGER.error('config file not contain auto_apply_resource')
                    return (False, 'config file not contain auto_apply_resource')
            if not config['resource_apply'].__contains__('service'):
                self.MAIN_THREAD_LOGGER.error('config file not contain service type')
                return (False, 'config file not contain service type')
            self.para_data['service'] = config.getint('resource_apply', 'service')
            return (True, '')


para_context_inst = ParameterContext()