# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/tools/action_network_verify_thread.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 1840 bytes
import threading, time, logging
from aiclient.aiclientapi.tool_manage import communicate_config as com_config
from aiclient.device_remote_interaction.common.action_queue import action_result_queue_inst
from aiclient.device_remote_interaction.common import define, network_check
S_MS_DECIMAL = 1000.0
DEFAULT_DURING_TIME = -1
DEFAULT_WAIT_TIME = -1

class ActionNetworkVerifyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.network_logger = logging.getLogger('network_io')
        self.adb_funcs = None
        self.op_code_funcs = {}

    def run(self):
        while 1:
            msg = action_result_queue_inst.get_action_item()
            if msg is None:
                time.sleep(0.01)
                continue
                msg_id = msg.get('msg_id', -1)
                if msg_id == -1:
                    self.network_logger.error('msg_id error:{}'.format(msg))
                    continue
                    if msg_id == define.MSG_AI_ACTION:
                        self.network_logger.warning('AI action process function in AI part, msg:{}'.format(msg))
                    else:
                        if msg_id == define.MSG_UI_ACTION:
                            self.network_logger.warning('no op_code process function in UI part, msg:{}'.format(msg))
                        else:
                            if msg_id == define.MSG_GAME_STATE:
                                game_state = msg.get('game_state', define.GAME_STATE_NONE)
                                self.network_logger.warning('game_state changed, from {a} to {b}'.format(a=com_config.GAME_STATE, b=game_state))
                                com_config.GAME_STATE = game_state
                            else:
                                if msg_id == define.MSG_CLIENT_REP:
                                    self.network_logger.info('get IO response:{}'.format(msg))
                                    network_check.has_recv_rep = True
                                else:
                                    self.network_logger.error('msg_id error:{}'.format(msg))