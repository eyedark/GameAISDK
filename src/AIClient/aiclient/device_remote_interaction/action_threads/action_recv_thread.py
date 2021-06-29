# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/action_threads/action_recv_thread.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 4639 bytes
import threading, time, logging
from ...aiclientapi.tool_manage import communicate_config as com_config
from ..common.action_queue import action_result_queue_inst
from ..common import define, network_check
RECORD_RECV_ACTION_INTERVAL = 20
MAX_NO_ACTION_DURING_TIME = 20
MAX_RECV_REP_TIME = 120
MAX_AVAILABLE_RECONNECT_TIME = 3

class ActionRecvThread(threading.Thread):

    def __init__(self, ai_client_api, ai_client_lock):
        threading.Thread.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.NETWORK_IO_LOGGER = logging.getLogger('network_io')
        self.ai_client_lock = ai_client_lock
        self.ai_client_api = ai_client_api
        self.recv_action_num = 0
        self.no_rep_start_time = 0
        self.no_rep_start_time_reconnect = 0
        self.cur_heart_beat_try_num = 1
        self.available_reconnect_time = MAX_AVAILABLE_RECONNECT_TIME

    def run(self):
        self.reset_heart_beat()
        while not com_config.terminate:
            msg = self.ai_client_api.recv_msg()
            if msg is None:
                self.check_heart_beat()
                time.sleep(0.002)
                continue
            else:
                self.reset_heart_beat()
                self._solve_message(msg)

        self.MAIN_THREAD_LOGGER.info('action_recv_thread terminated...')

    def _solve_message(self, msg):
        msg_id = msg.get('msg_id')
        if msg_id == define.MSG_CLIENT_REP:
            self._solve_heat_beat_message(msg)
        else:
            if msg_id == define.MSG_SOURCE_RES:
                self._solve_source_message(msg)
            else:
                self._solve_other_message(msg)

    def _solve_heat_beat_message(self, msg):
        self.MAIN_THREAD_LOGGER.info('get connection response:{}'.format(msg))
        if msg.get('code') != define.SUCCESS_CODE:
            self.MAIN_THREAD_LOGGER.warning('ai service connection exception: {}'.format(msg))
        else:
            network_check.has_recv_rep = True

    def _solve_source_message(self, msg):
        self.MAIN_THREAD_LOGGER.info('get source response:{}'.format(msg))
        network_check.source_info = msg

    def _solve_other_message(self, msg):
        img_id = msg.get('img_id', -1)
        msg_id = msg.get('msg_id')
        if msg_id == define.MSG_AI_ACTION:
            self.NETWORK_IO_LOGGER.debug('recv frame data, frameIndex={}'.format(img_id))
        action_result_queue_inst.add_action_item(msg=msg)
        self.recv_action_num += 1
        if self.recv_action_num % RECORD_RECV_ACTION_INTERVAL == 0:
            self.NETWORK_IO_LOGGER.info('recv action in recv thread:{}'.format(self.recv_action_num))
            self.NETWORK_IO_LOGGER.info('left action num to excute:{}'.format(action_result_queue_inst.get_queque_size()))
        time.sleep(0.001)

    def check_heart_beat(self):
        if not self.ai_client_api.get_connection_result():
            return
        current_time = time.time()
        if current_time - self.no_rep_start_time_reconnect > MAX_RECV_REP_TIME:
            with self.ai_client_lock:
                while 1:
                    if self.available_reconnect_time <= 0:
                        self.MAIN_THREAD_LOGGER.error('Stop reconnect. Exit...')
                        self.ai_client_api.set_heart_beat(False)
                        exit()
                    self.MAIN_THREAD_LOGGER.info('received no msg in {}s. Try to reconnect... [{}/{}]'.format(current_time - self.no_rep_start_time_reconnect, MAX_AVAILABLE_RECONNECT_TIME - self.available_reconnect_time + 1, MAX_AVAILABLE_RECONNECT_TIME))
                    self.available_reconnect_time -= 1
                    if self.ai_client_api.reconnect():
                        self.no_rep_start_time_reconnect = time.time()
                        break

        if current_time - self.no_rep_start_time > MAX_NO_ACTION_DURING_TIME * self.cur_heart_beat_try_num:
            self.send_heart_beat()
            self.NETWORK_IO_LOGGER.warning('no recv action, try send heart beat num: {}, elapsed_time: {}'.format(self.cur_heart_beat_try_num, current_time - self.no_rep_start_time))
            self.cur_heart_beat_try_num += 1

    def reset_heart_beat(self):
        self.no_rep_start_time = time.time()
        self.no_rep_start_time_reconnect = time.time()
        self.cur_heart_beat_try_num = 1
        self.available_reconnect_time = MAX_AVAILABLE_RECONNECT_TIME

    def send_heart_beat(self):
        self.ai_client_api.check_network()