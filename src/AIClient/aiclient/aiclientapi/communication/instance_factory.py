# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/aiclientapi/communication/instance_factory.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 644 bytes
import logging
from .zmq_client_communication import ZmqClientCommunication
ZMQ_COMM_TYPE = 1

def create_comm_instance(para_data):
    MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
    comm_type = para_data.get('comm_type', ZMQ_COMM_TYPE)
    if comm_type == ZMQ_COMM_TYPE:
        instance = ZmqClientCommunication()
        ret = instance.init(para_data)
        if not ret:
            return (ret, instance, 'zmq_client_communication init error')
        return (ret, instance, '')
    else:
        MAIN_THREAD_LOGGER.error('comm type error:{}'.format(comm_type))
        return (False, None, 'comm type error:{}'.format(comm_type))