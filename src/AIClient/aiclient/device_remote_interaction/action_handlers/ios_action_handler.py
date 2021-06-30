# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\action_handlers\ios_action_handler.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 5861 bytes
import threading, time, os, configparser, logging
from aiclient.device_remote_interaction.device_interface.device_api import get_device_api_instance
from aiclient.device_remote_interaction.common.action_check import action_excute_check_inst
from .action_handler_interface import IActionHandler
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
DEVICE_CFG_PATH = os.path.join(WORK_DIR, 'cfg/device_cfg/device.ini')
DEFAULT_WAIT_TIME = 0
DEFAULT_CLICK_DURING_TIME = 100
DEFAULT_SWIPE_DURING_TIME = 200
OP_NONE = -1
OP_CLICK = 4
OP_SWIPE = 5
OP_SWIPE_DOWN = 6

class IOSActionHandler(threading.Thread, IActionHandler):

    def __init__(self):
        IActionHandler.__init__(self)
        threading.Thread.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.DEVICE_DRIVER_LOGGER = logging.getLogger('device_driver')
        self.use_env_variable = 0
        self.device_serial = None
        self.device_api_inst = None
        self.op_code_funcs = dict()
        self.op_code_funcs[OP_NONE] = self.op_none_process
        self.op_code_funcs[OP_CLICK] = self.op_click_process
        self.op_code_funcs[OP_SWIPE] = self.op_swipe_process
        self.op_code_funcs[OP_SWIPE_DOWN] = self.op_swipe_down_process

    def load_parameter(self, device_cfg_path):
        if not os.path.exists(device_cfg_path):
            return (False, 'device_cfg_path not exist:{}'.format(device_cfg_path))
        else:
            config = configparser.ConfigParser()
            config.read(device_cfg_path)
            if 'device' not in config:
                return (False, 'device.ini config file not contain device section')
            if 'ios_action_handler' not in config:
                return (False, 'device.ini config file not contain ios_action_handler section')
            if 'use_env_variable' in config['device']:
                self.use_env_variable = int(config['device']['use_env_variable'])
            else:
                return (False, 'device.ini config file cannot contain use_env_variable')
                if 'device_serial' in config['mobile_device']:
                    self.device_serial = config.get('mobile_device', 'device_serial')
                    if self.device_serial == '':
                        self.device_serial = None
                else:
                    return (False, 'device.ini config file not contain device_serial')
            return (True, '')

    def init(self):
        ret, err = self.load_parameter(DEVICE_CFG_PATH)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('load_parameter error: {}'.format(err))
            return (
             False, err)
        else:
            try:
                self.device_api_inst = get_device_api_instance()
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('get device instance failed')
                return (False, err)

            return (True, '')

    def do_action(self, msg):
        op_code = msg.get('action_id')
        wait_time = msg.get('wait_time', DEFAULT_WAIT_TIME)
        if self.op_code_funcs.__contains__(op_code):
            func = self.op_code_funcs[op_code]
            func(msg)
            time.sleep(wait_time / 1000)
        else:
            self.DEVICE_DRIVER_LOGGER.error('unknown action id {}'.format(op_code))

    def op_none_process(self, msg):
        self.DEVICE_DRIVER_LOGGER.debug('op_code=none')

    def op_click_process(self, msg):
        px = msg['px']
        py = msg['py']
        during_time = msg.get('during_time', DEFAULT_CLICK_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=click, during_time={}'.format(during_time))
            self.device_api_inst.do_action(aType='touch_click', sx=px, sy=py, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process click op exception:{}'.format(err))

    def op_swipe_process(self, msg):
        start_x = msg['start_x']
        start_y = msg['start_y']
        end_x = msg['end_x']
        end_y = msg['end_y']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=swipe')
            self.device_api_inst.do_action(aType='touch_swipe', needUp=True, sx=start_x, sy=start_y, ex=end_x, ey=end_y)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_SWIPE, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process swipe op exception:{}'.format(err))

    def op_swipe_down_process(self, msg):
        start_x = msg['start_x']
        start_y = msg['start_y']
        end_x = msg['end_x']
        end_y = msg['end_y']
        during_time = msg.get('during_time', DEFAULT_SWIPE_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=swipe_down')
            self.device_api_inst.do_action(aType='touch_swipe', needUp=False, sx=start_x, sy=start_y, ex=end_x, ey=end_y, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_SWIPE, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process swipe op exception:{}'.format(err))