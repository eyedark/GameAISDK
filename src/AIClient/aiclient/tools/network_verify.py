# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/tools/network_verify.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 2248 bytes
import os, sys, time, logging, threading
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_FILE = os.path.join(WORK_DIR, 'cfg/network_comm_cfg/communication_cfg.ini')
sys.path.append(os.path.dirname(WORK_DIR))
from aiclient.aiclientapi.network_client import NetworkClient
from aiclient.device_remote_interaction.common import network_check
from aiclient.device_remote_interaction.action_threads.action_recv_thread import ActionRecvThread
from aiclient.py_logger import setup_logging
from aiclient.register_obj.state_notify import StateNotify
from aiclient.tools.action_network_verify_thread import ActionNetworkVerifyThread
CHECK_OVER_TIME = 10

class NetWorkVerify(object):

    def __init__(self):
        self.network_logger = logging.getLogger('network_io')
        self.ai_client = NetworkClient(StateNotify())

    def init(self):
        ret = self.ai_client.init()
        self.create_recv_excute_thread()
        return ret

    def create_recv_excute_thread(self):
        ai_client_lock = threading.RLock()
        action_recv_thread = ActionRecvThread(self.ai_client, ai_client_lock)
        action_excute_thread = ActionNetworkVerifyThread()
        action_recv_thread.daemon = True
        action_excute_thread.daemon = True
        action_recv_thread.start()
        action_excute_thread.start()
        self.network_logger.info('has start ActionRecvThread thread and ActionExcuteThread')

    def start_ai(self):
        self.init()
        self.verify_network()

    def verify_network(self):
        self.network_logger.info('send_verify_network info')
        self.ai_client.check_network()
        start_time = time.time()
        while True:
            if network_check.has_recv_rep or time.time() - start_time > 120:
                break
            time.sleep(1)

        if network_check.has_recv_rep:
            self.network_logger.info('this ip and port connected succeesfully')
        else:
            self.network_logger.error('this ip and port is not connected')


if __name__ == '__main__':
    logdir = os.path.join(os.getcwd(), 'log')
    os.makedirs(logdir, exist_ok=True)
    setup_logging()
    ae = NetWorkVerify()
    ae.start_ai()