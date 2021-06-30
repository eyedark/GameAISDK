# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\action_handlers\android_action_handler.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 14792 bytes
import threading, time, os, configparser, logging
from ...device_remote_interaction.device_interface.device_api import get_device_api_instance
from ...device_remote_interaction.common.action_check import action_excute_check_inst
from .action_handler_interface import IActionHandler
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
DEVICE_CFG_PATH = os.path.join(WORK_DIR, 'cfg/device_cfg/device.ini')
DEFAULT_DURING_TIME = -1
DEFAULT_WAIT_TIME = 0
OP_NONE = -1
OP_RESET = 0
OP_DOWN = 1
OP_UP = 2
OP_MOVE = 3
OP_CLICK = 4
OP_SWIPE = 5
OP_SWIPE_DOWN = 6
OP_SWIPE_MOVE = 7
OP_INPUT_TEXT = 8
OP_INPUT_KEY = 9
OP_CODM_ACTION_ID = 100

class AndroidActionHandler(threading.Thread, IActionHandler):

    def __init__(self):
        IActionHandler.__init__(self)
        threading.Thread.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.DEVICE_DRIVER_LOGGER = logging.getLogger('device_driver')
        self.login_api = None
        self.use_env_variable = 0
        self.device_serial = None
        self.use_login_function = 0
        self.auto_launch_app = 0
        self.app_package_name = ''
        self.game_account = ''
        self.game_pwd = ''
        self.device_api_inst = None
        self.op_code_funcs = dict()
        self.op_code_funcs[OP_NONE] = self.op_none_process
        self.op_code_funcs[OP_RESET] = self.op_reset_process
        self.op_code_funcs[OP_DOWN] = self.op_press_down_process
        self.op_code_funcs[OP_UP] = self.op_press_up_process
        self.op_code_funcs[OP_MOVE] = self.op_move_process
        self.op_code_funcs[OP_CLICK] = self.op_click_process
        self.op_code_funcs[OP_SWIPE] = self.op_swipe_process
        self.op_code_funcs[OP_SWIPE_DOWN] = self.op_swipe_down_process
        self.op_code_funcs[OP_SWIPE_MOVE] = self.op_swipe_move_process
        self.op_code_funcs[OP_INPUT_TEXT] = self.op_input_text_process
        self.op_code_funcs[OP_INPUT_KEY] = self.op_input_key_process
        self.op_code_funcs[OP_CODM_ACTION_ID] = self.codm_action

    def load_parameter(self, device_cfg_path):
        if not os.path.exists(device_cfg_path):
            return (False, 'device_cfg_path not exist:{}'.format(device_cfg_path))
        else:
            config = configparser.ConfigParser()
            config.read(device_cfg_path, encoding='UTF-8')
            if 'device' not in config:
                return (False, 'device.ini config file not contain device section')
            if 'android_action_handler' not in config:
                return (False, 'device.ini config file not contain android_action_handler section')
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
                if 'use_login_function' in config['android_action_handler']:
                    self.use_login_function = int(config['android_action_handler']['use_login_function'])
                else:
                    return (False, 'device.ini config file cannot contain use_login_function')
                    if 'auto_launch_app' in config['android_action_handler']:
                        self.auto_launch_app = int(config['android_action_handler']['auto_launch_app'])
                    else:
                        return (False, 'device.ini config file cannot contain auto_launch_app')
                        if 'app_package_name' in config['android_action_handler']:
                            self.app_package_name = config['android_action_handler']['app_package_name']
                        else:
                            return (False, 'device.ini config file cannot contain app_package_name')
                    if 'game_account' in config['android_action_handler']:
                        self.game_account = config['android_action_handler']['game_account']
                    else:
                        return (False, 'device.ini config file cannot contain game_account')
                if 'game_pwd' in config['android_action_handler']:
                    self.game_pwd = config['android_action_handler']['game_pwd']
                else:
                    return (False, 'device.ini config file cannot contain game_pwd')
            if self.use_env_variable:
                self.MAIN_THREAD_LOGGER.info('use_env_variable resolution')
                try:
                    self.game_account = os.environ.get('GAME_ACCOUNT', '')
                    self.game_pwd = os.environ.get('GAME_PWD', '')
                except Exception as err:
                    return (
                     False, 'get game_account or game_pwd from env error: {}'.format(err))

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

            if self.use_login_function == 1 or self.auto_launch_app == 1:
                from ...device_remote_interaction.device_interface.ui_device import UIDevice
                self.login_api = UIDevice()
                ret, error_str = self.login_api.init(serial=(self.device_serial))
                if not ret:
                    self.MAIN_THREAD_LOGGER.error('login_function init failed: {}'.format(error_str))
                    return (False, error_str)
                if self.auto_launch_app == 1:
                    self.login_api.launch_app(self.app_package_name)
            return (True, '')

    def launch_app(self, package_name):
        if self.use_login_function == 0:
            self.DEVICE_DRIVER_LOGGER.warning('no set use login function, bug call the launch_app api')
            return True
        else:
            return self.login_api.launch_app(package_name)

    def login_qq(self, msg_data):
        if self.use_login_function == 0:
            self.DEVICE_DRIVER_LOGGER.warning('no set use login function, bug call the login_qq api')
            return True
        else:
            if self.game_account is None or self.game_account == '' or self.game_pwd is None or self.game_pwd == '':
                self.DEVICE_DRIVER_LOGGER.error('game_account or game_pwd error, game_account: {}, game_pwd: {}'.format(self.game_account, self.game_pwd))
                return False
            return self.login_api.login_qq(msg_data=msg_data, account=(self.game_account), pwd=(self.game_pwd))

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

    def op_reset_process(self, msg):
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=reset')
            self.device_api_inst.do_action(aType='touch_reset')
            end_time = time.time()
            action_excute_check_inst.add_action(OP_RESET, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process reset op exception:{}'.format(err))

    def op_press_down_process(self, msg):
        px = msg['px']
        py = msg['py']
        contact = msg['contact']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=down')
            self.device_api_inst.do_action(aType='touch_down', sx=px, sy=py, contact=contact)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_DOWN, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process press_down op exception:{}'.format(err))

    def op_press_up_process(self, msg):
        contact = msg['contact']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=up')
            self.device_api_inst.do_action(aType='touch_up', contact=contact)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_UP, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process press_up op exception:{}'.format(err))

    def op_move_process(self, msg):
        px = msg['px']
        py = msg['py']
        contact = msg['contact']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=move')
            self.device_api_inst.do_action(aType='touch_move', sx=px, sy=py, contact=contact)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOVE, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process move op exception:{}'.format(err))

    def op_click_process(self, msg):
        px = msg['px']
        py = msg['py']
        contact = msg['contact']
        during_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=click, during_time={during_time}'.format(during_time=during_time))
            self.device_api_inst.do_action(aType='touch_click', sx=px, sy=py, contact=contact, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process click op exception:{}'.format(err))

    def op_swipe_process(self, msg):
        start_x = msg['start_x']
        start_y = msg['start_y']
        end_x = msg['end_x']
        end_y = msg['end_y']
        contact = msg['contact']
        during_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=swipe, during_time={during_time}'.format(during_time=during_time))
            self.device_api_inst.do_action(aType='touch_swipe', needUp=True, sx=start_x, sy=start_y, ex=end_x, ey=end_y, contact=contact, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_SWIPE, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process swipe op exception:{}'.format(err))

    def op_swipe_down_process(self, msg):
        start_x = msg['start_x']
        start_y = msg['start_y']
        end_x = msg['end_x']
        end_y = msg['end_y']
        contact = msg['contact']
        during_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=swipe_down, during_time={during_time}'.format(during_time=during_time))
            self.device_api_inst.do_action(aType='touch_swipe', needUp=False, sx=start_x, sy=start_y, ex=end_x, ey=end_y, contact=contact, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_SWIPE_DOWN, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process swipe_down op exception:{}'.format(err))

    def op_swipe_move_process(self, msg):
        px = msg['px']
        py = msg['py']
        contact = msg['contact']
        during_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=swipe_move, during_time={during_time}'.format(during_time=during_time))
            self.device_api_inst.do_action(aType='touch_swipemove', sx=px, sy=py, contact=contact, durationMS=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_SWIPE_MOVE, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process swipe_down op exception:{}'.format(err))

    def op_input_text_process(self, msg):
        text = msg.get('text', '')
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=input_text')
            self.device_api_inst.do_action(aType='device_text', text=text)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_INPUT_TEXT, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process input_text op exception:{}'.format(err))

    def op_input_key_process(self, msg):
        key = msg.get('key', '')
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=input_key')
            self.device_api_inst.do_action(aType='device_key', key=key)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_INPUT_TEXT, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('process input_text op exception:{}'.format(err))

    def codm_action(self, msg):
        self.device_api_inst.do_action(msg)

    def call_ui_login(self, msg):
        try:
            start_time = time.time()
            ret = self.login_qq(msg)
            self.DEVICE_DRIVER_LOGGER.debug('call login_qq api time: %3.3f' % (time.time() - start_time))
            if not ret:
                self.DEVICE_DRIVER_LOGGER.error('login_qq error: {}'.format(msg))
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('call login_qq exception: {}'.format(err))