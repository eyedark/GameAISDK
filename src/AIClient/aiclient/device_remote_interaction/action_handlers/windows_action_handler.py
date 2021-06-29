# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/action_handlers/windows_action_handler.py
# Compiled at: 2021-02-23 15:21:06
# Size of source mod 2**32: 10911 bytes
import threading, time, os, configparser, logging
from ..device_interface.device_api import get_device_api_instance
from ..common.action_check import action_excute_check_inst
from .action_handler_interface import IActionHandler
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
DEVICE_CFG_PATH = os.path.join(WORK_DIR, 'cfg/device_cfg/device.ini')
DEFAULT_DURING_TIME = 100
DEFAULT_WAIT_TIME = 0
OP_NONE = -1
OP_MOUSE_MOVE = 0
OP_MOUSE_LONG_CLICK = 1
OP_MOUSE_DOUBLE_CLICK = 2
OP_MOUSE_RIGHT_CLICK = 3
OP_MOUSE_CLICK = 4
OP_MOUSE_DRAG = 5
OP_KEY_INPUT = 6
OP_KEY_INPUT_STRING = 7
OP_MOUSE_LBUTTON_DOWN = 8
OP_MOUSE_LBUTTON_UP = 9
OP_SIMULATOR_KEY = 10

class SimulatorActionType(object):
    DOWN = 'down'
    UP = 'up'
    CLICK = 'click'
    TEXT = 'text'


class WindowsActionHandler(threading.Thread, IActionHandler):

    def __init__(self):
        IActionHandler.__init__(self)
        threading.Thread.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.DEVICE_DRIVER_LOGGER = logging.getLogger('device_driver')
        self.device_api_inst = None
        self.op_code_funcs = dict()
        self.op_code_funcs[OP_NONE] = self.op_none
        self.op_code_funcs[OP_MOUSE_MOVE] = self.op_mouse_move
        self.op_code_funcs[OP_MOUSE_CLICK] = self.op_mouse_click
        self.op_code_funcs[OP_MOUSE_DOUBLE_CLICK] = self.op_mouse_doubleclick
        self.op_code_funcs[OP_MOUSE_RIGHT_CLICK] = self.op_mouse_rightclick
        self.op_code_funcs[OP_MOUSE_LONG_CLICK] = self.op_mouse_longclick
        self.op_code_funcs[OP_MOUSE_DRAG] = self.op_mouse_drag
        self.op_code_funcs[OP_KEY_INPUT] = self.op_key_input
        self.op_code_funcs[OP_KEY_INPUT_STRING] = self.op_key_inputstring
        self.op_code_funcs[OP_MOUSE_LBUTTON_DOWN] = self.op_mouse_down
        self.op_code_funcs[OP_MOUSE_LBUTTON_UP] = self.op_mouse_up
        self.op_code_funcs[OP_SIMULATOR_KEY] = self.op_simulator_key

    def load_parameter(self, device_cfg_path):
        return (True, '')

    def init(self):
        ret, err = self.load_parameter(DEVICE_CFG_PATH)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('load_parameter error: {}'.format(err))
            return (False, err)
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

    def op_none(self, msg):
        self.DEVICE_DRIVER_LOGGER.debug('op_code=none')

    def op_mouse_down(self, msg):
        px = msg['px']
        py = msg['py']
        try:
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_down')
            self.device_api_inst.do_action(aType='mouse_down', px=px, py=py)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_down exception:{}'.format(err))

    def op_mouse_up(self, msg):
        px = msg['px']
        py = msg['py']
        try:
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_up')
            self.device_api_inst.do_action(aType='mouse_up', px=px, py=py)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_up exception:{}'.format(err))

    def op_mouse_move(self, msg):
        if 'px' in msg and 'py' in msg:
            px = msg['px']
            py = msg['py']
            try:
                start_time = time.time()
                self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_move')
                self.device_api_inst.do_action(aType='mouse_move', px=px, py=py)
                end_time = time.time()
                action_excute_check_inst.add_action(OP_MOUSE_MOVE, end_time - start_time)
            except Exception as err:
                self.DEVICE_DRIVER_LOGGER.error('op mouse_move exception:{}'.format(err))

    def op_mouse_click(self, msg):
        px = msg['px']
        py = msg['py']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_click')
            self.device_api_inst.do_action(aType='mouse_click', px=px, py=py)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOUSE_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_click exception:{}'.format(err))

    def op_mouse_doubleclick(self, msg):
        px = msg['px']
        py = msg['py']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_doubleclick')
            self.device_api_inst.do_action(aType='mouse_doubleclick', px=px, py=py)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOUSE_DOUBLE_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_doubleclick exception:{}'.format(err))

    def op_mouse_longclick(self, msg):
        px = msg['px']
        py = msg['py']
        long_click_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_longclick')
            self.device_api_inst.do_action(aType='mouse_longclick', px=px, py=py, long_click_time=long_click_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOUSE_LONG_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_longclick exception:{}'.format(err))

    def op_mouse_rightclick(self, msg):
        px = msg['px']
        py = msg['py']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_rightclick')
            self.device_api_inst.do_action(aType='mouse_rightclick', px=px, py=py)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOUSE_RIGHT_CLICK, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_rightclick exception:{}'.format(err))

    def op_mouse_drag(self, msg):
        fromX = msg['start_x']
        fromY = msg['start_y']
        toX = msg['end_x']
        toY = msg['end_y']
        during_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=mouse_drag')
            self.device_api_inst.do_action(aType='mouse_drag', fromX=fromX, fromY=fromY, toX=toX, toY=toY, during_time=during_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_MOUSE_DRAG, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_drag exception:{}'.format(err))

    def op_key_input(self, msg):
        keys = msg['keys']
        long_click_time = msg.get('during_time', DEFAULT_DURING_TIME)
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=key_input')
            self.device_api_inst.do_action(aType='key_input', keys=keys, long_click_time=long_click_time)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_KEY_INPUT, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op key_input exception:{}'.format(err))

    def op_key_inputstring(self, msg):
        key_string = msg['key_string']
        try:
            start_time = time.time()
            self.DEVICE_DRIVER_LOGGER.debug('op_code=key_inputstring')
            self.device_api_inst.do_action(aType='key_inputstring', key_string=key_string)
            end_time = time.time()
            action_excute_check_inst.add_action(OP_KEY_INPUT_STRING, end_time - start_time)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op key_inputstring exception:{}'.format(err))

    def op_simulator_key(self, msg):
        try:
            alphabet = msg['alphabet']
            if alphabet is None or alphabet == '':
                self._WindowsActionHandler__op_simulate_mouse(msg)
                return
            action_type = msg['action_type']
            if action_type == SimulatorActionType.CLICK:
                self.DEVICE_DRIVER_LOGGER.debug('op_code=key_input, keys:%s' % alphabet)
                self.device_api_inst.do_action(aType='key_input', keys=alphabet)
            else:
                if action_type == SimulatorActionType.DOWN:
                    self.DEVICE_DRIVER_LOGGER.debug('op_code=key_press, keys:%s' % alphabet)
                    self.device_api_inst.do_action(aType='key_press', keys=alphabet)
                else:
                    if action_type == SimulatorActionType.UP:
                        self.DEVICE_DRIVER_LOGGER.debug('op_code=key_release, keys:%s' % alphabet)
                        self.device_api_inst.do_action(aType='key_release', keys=alphabet)
                    else:
                        if action_type == SimulatorActionType.TEXT:
                            action_text = msg['action_text']
                            self.DEVICE_DRIVER_LOGGER.debug('op_code=key_inputstring')
                            self.device_api_inst.do_action(aType='key_inputstring', key_string=action_text)
                        else:
                            raise ValueError('unknown action type:%s' % action_type)
        except Exception as err:
            self.DEVICE_DRIVER_LOGGER.error('op mouse_click exception:{}'.format(err))

    def __op_simulate_mouse(self, msg):
        action_type = msg['action_type']
        if action_type == SimulatorActionType.CLICK:
            self.op_mouse_click(msg)
        else:
            if action_type == SimulatorActionType.DOWN:
                self.op_mouse_down(msg)
            else:
                if action_type == SimulatorActionType.UP:
                    self.op_mouse_up(msg)
                else:
                    raise ValueError('unknown action type:%s' % action_type)