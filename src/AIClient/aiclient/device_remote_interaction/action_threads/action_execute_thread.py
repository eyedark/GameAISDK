# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\action_threads\action_execute_thread.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 12355 bytes
import threading, time, os, configparser, traceback, logging
from ...aiclientapi.performance_profile.speed_check import speed_check_inst
from ...aiclientapi.tool_manage import communicate_config as com_config
from ...aiclientapi.tool_manage import parameter_context as para_context
from ...device_remote_interaction.common.action_queue import action_result_queue_inst
from ...device_remote_interaction.common import define, network_check
from ..device_interface.config import DeviceType
S_MS_DECIMAL = 1000.0
DEFAULT_DURING_TIME = -1
DEFAULT_WAIT_TIME = -1
MAX_NONE_ACTION_TIME = 20
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
CFG_FILE = os.path.join(WORK_DIR, 'cfg/network_comm_cfg/communication_cfg.ini')

class ActionExecuteThread(threading.Thread):

    def __init__(self, state_notify_inst):
        threading.Thread.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.DEVICE_DRIVER_LOGGER = logging.getLogger('device_driver')
        self.state_notify_inst = state_notify_inst
        self.action_handler = None
        self.cur_runtimes_by_game_state = 1
        self.cur_runtimes_by_agent_state = 1
        self.device_type = None
        self.para_data = {}
        self.max_none_action_time = MAX_NONE_ACTION_TIME
        self.service = None

    def load_parameter(self):
        source_info = network_check.source_info
        if source_info['device_type'] is not None:
            self.device_type = source_info['device_type']
        else:
            return (False, 'get media type failed')
        self.MAIN_THREAD_LOGGER.info('the media type is {}'.format(self.device_type))
        if self.device_type not in DeviceType.__members__.keys():
            err_info = 'Unknown device_type {}, should be one of {}'.format(self.device_type, DeviceType)
            return (
             False, err_info)
        else:
            ret, self.para_data, error_str = para_context.para_context_inst.init(CFG_FILE)
            if not ret:
                self.state_notify_inst.on_exception(exception_type=(self.state_notify_inst.CONFIG_PARAMS_LOAD_ERROR), description=error_str)
                return (False, error_str)
            self.max_none_action_time = self.para_data.get('max_none_action_time', MAX_NONE_ACTION_TIME)
            self.service = self.para_data.get('service')
            return (True, '')

    def init(self):
        ret, err = self.load_parameter()
        if not ret:
            self.MAIN_THREAD_LOGGER.error('load_parameter error: {}'.format(err))
            return False
        try:
            if self.device_type == DeviceType.Android.value:
                from ..action_handlers.android_action_handler import AndroidActionHandler
                self.action_handler = AndroidActionHandler()
                if not self.action_handler.init():
                    self.MAIN_THREAD_LOGGER.error('android action handler init failed')
                    return False
            else:
                if self.device_type == DeviceType.IOS.value:
                    from ..action_handlers.ios_action_handler import IOSActionHandler
                    self.action_handler = IOSActionHandler()
                    if not self.action_handler.init():
                        self.MAIN_THREAD_LOGGER.error('android action handler init failed')
                        return False
                else:
                    if self.device_type == DeviceType.Windows.value:
                        from ..action_handlers.windows_action_handler import WindowsActionHandler
                        self.action_handler = WindowsActionHandler()
                        if not self.action_handler.init():
                            self.MAIN_THREAD_LOGGER.error('windows action handler init failed')
                            return False
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('{} action handler created failed: {}'.format(self.device_type, err))
            self.MAIN_THREAD_LOGGER.error(traceback.format_exc())
            return False

    def run(self):
        none_action_start_time = None
        while not com_config.terminate:
            msg = action_result_queue_inst.get_action_item()
            if msg is None:
                if com_config.ui_action_on:
                    if none_action_start_time is None:
                        none_action_start_time = time.time()
                    elif time.time() - none_action_start_time > self.max_none_action_time:
                        self.DEVICE_DRIVER_LOGGER.info('have not received any action in the last {} seconds.'.format(self.max_none_action_time))
                        com_config.send_frame = True
                        none_action_start_time = None
                time.sleep(0.002)
                continue
            if com_config.ui_action_on:
                if none_action_start_time is not None:
                    if time.time() - none_action_start_time > self.max_none_action_time:
                        self.DEVICE_DRIVER_LOGGER.info('have not received any action in the last {} seconds.'.format(self.max_none_action_time))
                        com_config.send_frame = True
                        none_action_start_time = None
            self.DEVICE_DRIVER_LOGGER.info('get action item: {}'.format(msg))
            msg_id = msg.get('msg_id', -1)
            if msg_id == -1:
                self.DEVICE_DRIVER_LOGGER.error('msg_id error:{}'.format(msg))
            else:
                if msg_id == define.MSG_AI_ACTION:
                    try:
                        self.action_handler.do_action(msg)
                    except Exception as err:
                        self.DEVICE_DRIVER_LOGGER.error('do AI action exception: {}'.format(err))

                    speed_check_inst.caculate_ai_process_time(msg_id)
                else:
                    if msg_id == define.MSG_UI_ACTION:
                        none_action_start_time = None
                        if 'actions' in msg:
                            actions = msg['actions']
                        else:
                            if 'action_id' in msg:
                                actions = [
                                 msg]
                            else:
                                actions = []
                                self.DEVICE_DRIVER_LOGGER.error('MSG_UI_ACTION should have label: actions or action_id')
                        for action_msg in actions:
                            if action_msg:
                                try:
                                    self.action_handler.do_action(action_msg)
                                except Exception as err:
                                    self.DEVICE_DRIVER_LOGGER.error('do UI action exception: {}'.format(err))

                        com_config.send_frame = True
                    else:
                        if msg_id == define.MSG_GAME_STATE:
                            game_state = msg.get('game_state', define.GAME_STATE_NONE)
                            if game_state != define.GAME_STATE_NONE:
                                if game_state != com_config.GAME_STATE:
                                    self.MAIN_THREAD_LOGGER.info('game_state changed, from {a} to {b}'.format(a=(com_config.GAME_STATE), b=game_state))
                                    com_config.GAME_STATE = game_state
                            if game_state == define.GAME_STATE_START:
                                self.DEVICE_DRIVER_LOGGER.info('Use AI action')
                                com_config.ui_action_on = False
                            else:
                                if game_state == define.GAME_STATE_UI:
                                    self.DEVICE_DRIVER_LOGGER.info('Using UI action')
                                    com_config.ui_action_on = True
                                else:
                                    if game_state == define.GAME_STATE_OVER or game_state == define.GAME_STATE_MATCH_WIN:
                                        self.MAIN_THREAD_LOGGER.info('Round {} done. Counted by GAME_STATE'.format(self.cur_runtimes_by_game_state))
                                        if self.cur_runtimes_by_game_state == com_config.runtimes:
                                            if self.service == 2:
                                                self.MAIN_THREAD_LOGGER.info('UI agent: reached maximum runtimes: {}'.format(com_config.runtimes))
                                                com_config.terminate = True
                                        else:
                                            self.cur_runtimes_by_game_state += 1
                        else:
                            if msg_id == define.MSG_AGENT_STATE:
                                self.state_notify(msg)
                            else:
                                if msg_id == define.MSG_RESTART_RESULT:
                                    self.restart_process(msg)
                                else:
                                    if msg_id == define.MSG_AI_SERVICE_STATE:
                                        self.ai_service_state_detect(msg)
                                    else:
                                        self.DEVICE_DRIVER_LOGGER.error('msg_id error:{}'.format(msg))
                if self.device_type == DeviceType.Android.value:
                    self.action_handler.call_ui_login(msg)
                time.sleep(0.001)

        self.MAIN_THREAD_LOGGER.info('action_execute_thread terminated...')

    def restart_process(self, msg):
        restart_result = msg.get('restart_result')
        if restart_result == define.RESTART_RESULT_SUCCESS:
            self.state_notify_inst.on_ai_service_state(com_config.AI_SERVICE_READY)
            self.MAIN_THREAD_LOGGER.debug('restart success:{}'.format(msg))
        else:
            if restart_result == define.RESTART_RESULT_FAILURE:
                self.state_notify_inst.on_ai_service_state(com_config.AI_SERVICE_ABNORMAL)
                self.MAIN_THREAD_LOGGER.debug('restart failed:{}'.format(msg))
            else:
                self.MAIN_THREAD_LOGGER.error('restart_result error:{}'.format(msg))

    def state_notify(self, msg):
        agent_state_id = msg.get('agent_state_id')
        if agent_state_id == define.AGENT_STATE_WAITING:
            self.MAIN_THREAD_LOGGER.debug('AGENT_STATE_WAITING: {}'.format(msg))
        else:
            if agent_state_id == define.AGENT_STATE_PLAYING:
                self.MAIN_THREAD_LOGGER.debug('AGENT_STATE_PLAYING: {}'.format(msg))
                self.state_notify_inst.on_start()
            else:
                if agent_state_id == define.AGENT_STATE_PAUSE:
                    self.MAIN_THREAD_LOGGER.debug('AGENT_STATE_PAUSE: {}'.format(msg))
                    self.state_notify_inst.on_pause()
                else:
                    if agent_state_id == define.AGENT_STATE_RESTORE_PLAYING:
                        self.MAIN_THREAD_LOGGER.debug('AGENT_STATE_RESTORE_PLAYING: {}'.format(msg))
                        self.state_notify_inst.on_restore()
                    else:
                        if agent_state_id == define.AGENT_STATE_OVER:
                            self.MAIN_THREAD_LOGGER.debug('AGENT_STATE_OVER: {}'.format(msg))
                            self.state_notify_inst.on_stop()
                            self.MAIN_THREAD_LOGGER.info('Round {} done. Counted by AGENT_STATE'.format(self.cur_runtimes_by_agent_state))
                            if self.cur_runtimes_by_agent_state == com_config.runtimes and self.service == 1:
                                self.MAIN_THREAD_LOGGER.info('AI agent: reached maximum runtimes: {}'.format(com_config.runtimes))
                                com_config.terminate = True
                            else:
                                self.cur_runtimes_by_agent_state += 1
                        else:
                            self.MAIN_THREAD_LOGGER.error('agent_state_id error:{}'.format(agent_state_id))

    def ai_service_state_detect(self, msg):
        ai_service_state = msg.get('ai_service_state', define.AI_SERVICE_STATE_NORMAL)
        if ai_service_state == define.AI_SERVICE_STATE_NORMAL:
            return
        error_str = com_config.msg_ai_service_state_desc.get(int(ai_service_state), 'ai service exception')
        self.state_notify_inst.on_exception(self.state_notify_inst.AI_SDK_ERROR, error_str)
        com_config.is_ai_service_state_ok = False