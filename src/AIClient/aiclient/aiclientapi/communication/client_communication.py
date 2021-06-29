# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/aiclientapi/communication/client_communication.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 3017 bytes
import os, socket, configparser, msgpack, msgpack_numpy as mn, struct, logging
from ..tool_manage import communicate_config as com_conf

class ClientCommunication(object):

    def __init__(self):
        pass

    def init(self, cfg_file):
        pass

    def recv_msg(self):
        pass

    def send_msg(self, img_id, img_data, status, extend_info=None):
        pass

    def unpack_msg(self, msg):
        msg_data = msgpack.unpackb(msg)
        return msg_data

    def pack_msg(self, msg):
        return msgpack.packb(msg, default=mn.encode, use_bin_type=True)


class SocketClientCommunication(ClientCommunication):

    def __init__(self, cfg_file):
        ClientCommunication.__init__(self)
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.NETWORK_IO_LOGGER = logging.getLogger('network_io')
        self.sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.MAIN_THREAD_LOGGER.info('cfg_file:{}'.format(cfg_file))
        self._init(cfg_file)

    def _load_parameter(self, cfg_file):
        if not os.path.exists(cfg_file):
            self.MAIN_THREAD_LOGGER.error('cfg_file not exist:{}'.format(cfg_file))
        config = configparser.ConfigParser(strict=False)
        config.read(cfg_file)
        return config['IP']

    def _init(self, cfg_file):
        ip_args = self._load_parameter(cfg_file)
        self.sock_conn.connect((ip_args['ip'], int(ip_args['port1'])))
        self.sock_conn2.connect((ip_args['ip'], int(ip_args['port2'])))

    def _recv_msg_size(self, msg_size):
        size = 0
        data = []
        while size < msg_size:
            buff = self.sock_conn2.recv(msg_size - size)
            if buff == '':
                return
            size += len(buff)
            data.append(buff)

        return ''.join(data)

    def recv_msg(self):
        msg_data = None
        try:
            size_buff = self._recv_msg_size(com_conf.INTEGER_LENGTH)
            data_size = struct.unpack('I', size_buff)[0]
            msg_data = self._recv_msg_size(data_size)
            msg_data = self.unpack_msg(msg_data)
        except Exception as err:
            self.NETWORK_IO_LOGGER.error('recv msg data excetion:{}'.format(err))

        return msg_data

    def send_msg(self, img_id, img_data, status, extend_info=None):
        msg_data = dict()
        msg_data['img_id'] = img_id
        msg_data['img_data'] = img_data
        msg_data['status'] = status
        if extend_info is not None:
            msg_data = dict(msg_data, **extend_info)
        msg_data = self.pack_msg(msg_data)
        size = len(msg_data)
        size_buff = struct.pack('I', size)
        try:
            self.sock_conn.sendall(size_buff)
            self.sock_conn.sendall(msg_data)
        except Exception as err:
            self.NETWORK_IO_LOGGER.error('send data exception:{}'.format(err))