# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making GameAISDK available.

This source code file is licensed under the GNU General Public License Version 3.
For full details, please refer to the file "LICENSE.txt" which is provided as part of this source code package.

Copyright (C) 2020 THL A29 Limited, a Tencent company.  All rights reserved.
"""

import json
import logging
import queue
import threading
import time
from urllib import request
from urllib.error import URLError, HTTPError

LOG = logging.getLogger('IOService')


class HTTPThread(threading.Thread):
    """
    HTTP Thread implement
    """
    def __init__(self, sendQueue, recvQueue, cfg):
        threading.Thread.__init__(self)
        self.__sendQueue = sendQueue
        self.__recvQueue = recvQueue

        self.__port = cfg['port']
        self.__ip = cfg['ip']
        self.__staffName = cfg['STAFFNAME']
        self.__url = 'http://%s:%d/ai_sdk/state_notify' % (self.__ip, self.__port)
        self.__HTTPHeader = {'Content-Type': 'application/json', 'STAFFNAME': self.__staffName}

        LOG.info('ASM HTTP URL [%s]', self.__url)
        LOG.info('ASM HTTP Header [%s]', self.__HTTPHeader)

    def run(self):
        while True:
            if not self.__sendQueue.empty():
                data = self.__sendQueue.get()
                if data is not None:
                    self._Post(data)

            time.sleep(0.001)

    def _Post(self, msgData):
        try:
            ret = self._PostJsonData(msgData)
        except ResourceWarning as e:
            LOG.warning('Send POST to ASM failed err[%s], if you run AI SDK locally, please ignore', e)
            return False
        LOG.info("Res result: {}".format(ret["error"]))
        if int(ret["error"]) < 0:
            LOG.error('POST return err[%s/%s]', ret['error'], ret['errstr'])
            return False
        if 'msg_id' in ret['data']:
            self.__recvQueue.put_nowait(ret['data'])
        return True

    def _PostJsonData(self, data):
        jsonData = json.dumps(data)
        jsonData = bytes(jsonData, 'utf-8')
        result = self._RequestInfo(jsonData)
        return json.loads(result)

    def _RequestInfo(self, data=None):
        req = request.Request(self.__url, data, self.__HTTPHeader)
        try:
            response = request.urlopen(req)
        except URLError as e:
            # do something
            LOG.error('URLError: %s',req.full_url)
            result = '{\"error\":-1, \"errstr\": \"server not found,  if you run AI SDK locally, please ignore\"}'
            return result
        else:
            # do something
            result = response.read().decode('utf-8')
        
        return result


class HTTPClient(object):
    """
    HTTP Client implement for communication with ASM
    """
    def __init__(self):
        self.__sendQueue = queue.Queue()
        self.__recvQueue = queue.Queue()
        self.__HTTPthread = None

    def Initialize(self, cfg):
        """
        Initialize this module, load config from cfg
        :param cfg:
        :return: True or false
        """
        self.__HTTPthread = HTTPThread(self.__sendQueue, self.__recvQueue, cfg)
        self.__HTTPthread.setDaemon(True)
        self.__HTTPthread.start()
        return True

    def Finish(self):
        """
        Finish this module
        :return:
        """
        return True

    def Send(self, msgBuff):
        """
        Send the msgBuff to HTTP Server
        :param msgBuff: the msg buff to be sent
        :return:
        """
        try:
            self.__sendQueue.put_nowait(msgBuff)
        except queue.Full:
            LOG.warning('sendQueue full')

    def Recv(self):
        """
        Receive the msg from HTTP Server
        :return: A list contains the msgs received
        """
        msgBuffList = []
        while not self.__recvQueue.empty():
            try:
                msgBuff = self.__recvQueue.get_nowait()
            except queue.Empty:
                LOG.warning('recvQueue empty')
                break
            msgBuffList.append(msgBuff)

        return msgBuffList
