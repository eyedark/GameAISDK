# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/aiclientapi/communication/zmq_client_communication.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 7129 bytes
import os, zmq, cv2, numpy as np, json, logging
from .client_communication import ClientCommunication
from ...device_remote_interaction.common import define
from ..tool_manage import communicate_config as com_config

class ZmqClientCommunication(ClientCommunication):

    def __init__(self):
        ClientCommunication.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.NETWORK_IO_LOGGER = logging.getLogger('network_io')
        self.sock_send = None
        self.sock_recv = None
        self.para_data = None
        self.frame_decode_type = 2
        self.key = ''
        self.test_id = '0'
        self.game_id = 0
        self.game_version = '0'

    def init(self, para_data):
        self.para_data = para_data
        self.MAIN_THREAD_LOGGER.info('para_data in zmq:{}'.format(para_data))
        ip, port1, port2 = self.get_ip_port()
        send_pattern = self.para_data['send_pattern']
        recv_pattern = self.para_data['recv_pattern']
        context_send = zmq.Context()
        self.sock_send = context_send.socket(send_pattern)
        self.sock_send.setsockopt(zmq.CONFLATE, 1)
        self.sock_send.connect('tcp://%s:%d' % (ip, port1))
        context_recv = zmq.Context()
        self.sock_recv = context_recv.socket(recv_pattern)
        save_last_action = self.para_data.get('save_last_action')
        if save_last_action == 1:
            self.sock_recv.setsockopt(zmq.CONFLATE, 1)
        self.sock_recv.connect('tcp://%s:%d' % (ip, port2))
        ret = self.set_parameter()
        return ret

    def set_parameter(self):
        self.frame_decode_type = self.para_data.get('frame_decode_type')
        if self.frame_decode_type not in define.FRAME_DECODE_TYPES:
            self.MAIN_THREAD_LOGGER.error('frame decode type error:{}'.format(self.frame_decode_type))
            return False
        self.key = self.para_data.get('key', '')
        if self.key == '':
            self.MAIN_THREAD_LOGGER.error('key error, key:{}'.format(self.key))
            return False
        return True

    def get_ip_port(self):
        ip = self.para_data['ip']
        port1 = self.para_data['port1']
        port2 = self.para_data['port2']
        use_env_variable = self.para_data.get('use_env_variable', False)
        self.test_id = com_config.test_id
        self.game_id = com_config.game_id
        self.game_version = com_config.game_version
        self.MAIN_THREAD_LOGGER.info('use test_id: {}'.format(self.test_id))
        if use_env_variable:
            self.MAIN_THREAD_LOGGER.info('use_env_variable ip and port')
            ip = os.environ.get('CLIENT_IP')
            port1 = int(os.environ.get('CLIENT_PORT1'))
            port2 = int(os.environ.get('CLIENT_PORT2'))
            key = os.environ.get('GAME_KEY')
            self.para_data['key'] = key
            if ip is None or port1 is None or port2 is None:
                self.MAIN_THREAD_LOGGER.error('env_variable is None, env_ip:{a}, env_port1:{b}, env_port2:{c}'.format(a=ip, b=port1, c=port2))
            self.MAIN_THREAD_LOGGER.info('env_ip:{a}, env_port1:{b}, env_port2:{c}'.format(a=ip, b=port1, c=port2))
        return (ip, port1, port2)

    def recv_msg(self):
        try:
            msg_data = self.sock_recv.recv(flags=zmq.NOBLOCK)
        except Exception as err:
            return

        if msg_data is None:
            self.NETWORK_IO_LOGGER.warning('recv data is None in zmq')
            return msg_data
        msg_data = self.unpack_msg(msg_data)
        return msg_data

    def send_check_network(self):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CLIENT_REQ
        msg_data['key'] = self.key
        msg_data['test_id'] = self.test_id
        msg_data['game_id'] = self.game_id
        msg_data['game_version'] = self.game_version
        self.send_compress_data(msg_data)

    def send_pause_ai(self):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CLIENT_PAUSE
        msg_data['key'] = self.key
        self.send_compress_data(msg_data)

    def send_restore_ai(self):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CLIENT_RESTORE
        msg_data['key'] = self.key
        self.send_compress_data(msg_data)

    def send_game_state(self, game_state):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CLIENT_CHANGE_GAME_STATE
        msg_data['game_state'] = game_state
        msg_data['key'] = self.key
        self.send_compress_data(msg_data)

    def send_source_info_request(self):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_SOURCE_REQ
        self.send_compress_data(msg_data)

    def send_start_ai(self):
        pass

    def send_end_ai(self):
        pass

    def send_restart_ai(self):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CLIENT_RESTART
        msg_data['key'] = self.key
        self.send_compress_data(msg_data)

    def send_img_msg(self, img_id, img_data, extend_info=None):
        msg_data = dict()
        msg_data['msg_id'] = define.MSG_CMD_CLIENT_DATA
        msg_data['key'] = self.key
        msg_data['frame_seq'] = img_id
        msg_data['frame_decode_type'] = self.frame_decode_type
        ret, img_data = self.convert_img_data(img_id, img_data, self.frame_decode_type)
        if not ret:
            self.NETWORK_IO_LOGGER.error('convert img data error, return')
            return
        msg_data['frame'] = img_data
        if extend_info is not None:
            if type(extend_info) != dict:
                self.NETWORK_IO_LOGGER.error('extend_info type not dict, actually type: {}'.format(type(extend_info)))
                return
            try:
                msg_data['extend'] = json.dumps(extend_info)
            except Exception as err:
                self.NETWORK_IO_LOGGER.error('dums extend_info error: {}, extend_info: {}'.format(err, extend_info))
                return

        self.send_compress_data(msg_data)

    def send_compress_data(self, msg_data):
        msg_data = self.pack_msg(msg_data)
        self.sock_send.send(msg_data)

    def convert_digital_data(self, frame_data, frame_decode_type):
        return (
         True, frame_data)

    def convert_img_data(self, img_id, img_data, send_type):
        if send_type == define.RAW_IMG_SEND_TYPE:
            return (True, img_data)
        if send_type == define.BINARY_IMG_SEND_TYPE:
            if bytes != type(img_data):
                self.NETWORK_IO_LOGGER.error('send img type error:{} in BINARY_IMG_SEND_TYPE'.format(send_type))
                return (False, '')
        else:
            if send_type == define.CV2_EN_DECODE_IMG_SEND_TYPE:
                img_encode = cv2.imencode('.jpg', img_data)[1]
                data_encode = np.array(img_encode)
                img_data = data_encode.tostring()
            else:
                self.NETWORK_IO_LOGGER.error('img send type error, type:{}'.format(send_type))
                return (False, '')
        return (
         True, img_data)