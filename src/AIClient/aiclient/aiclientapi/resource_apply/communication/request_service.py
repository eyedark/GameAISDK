# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\resource_apply\communication\request_service.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 3729 bytes
import requests, json, os, time, logging
resource_apply_url = 'application/create_service'
recycle_resource_url = 'other/recycle_by_taskid'
test_id_verify_url = 'other/ai_version_verify'

class RequestService(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.root_url = ''
        self.headers = {}
        self.max_post_timeout = None

    def init(self, root_url, user, max_post_timeout):
        self.root_url = root_url
        self.headers = {'content-type':'application/json',  'STAFFNAME':user}
        self.max_post_timeout = max_post_timeout
        self.MAIN_THREAD_LOGGER.debug('max_post_timeout: {}'.format(self.max_post_timeout))
        return (True, '')

    def http_post(self, url, data):
        start_post_time = time.time()
        resp = requests.post(url, data=(json.dumps(data)), timeout=(self.max_post_timeout), headers=(self.headers), verify=False)
        end_post_time = time.time()
        self.MAIN_THREAD_LOGGER.debug('post spent time: %3.2f' % (end_post_time - start_post_time))
        if resp.status_code == 200:
            self.MAIN_THREAD_LOGGER.debug('post {} success data: {}'.format(url, data))
            return (
             True, json.loads(resp.text))
        else:
            self.MAIN_THREAD_LOGGER.error('post {} failed data:{} text:{}'.format(url, data, resp.text))
            return (False, resp.text)

    def create_ai_service(self, data):
        url = '%s/%s' % (self.root_url, resource_apply_url)
        ret, result = self.http_post(url, data)
        if ret:
            if result.get('error') == 0:
                result = self.parse_ai_service(result['data'])
                if result is not None:
                    self.MAIN_THREAD_LOGGER.info('ai service result:{}'.format(result))
                    return (
                     True, result)
        self.MAIN_THREAD_LOGGER.error('create ai-service request error:{}'.format(result))
        return (False, result)

    def parse_ai_service(self, data):
        if data is None or type(data) != dict:
            self.MAIN_THREAD_LOGGER.error('create ai-service return obj type error:{}'.format(data))
            return
        if data.get('code') == 200:
            return {'ip':data.get('tgw_ip'), 
             'port1':data.get('ports')[0],  'port2':data.get('ports')[1],  'key':data.get('source_server_id'), 
             'source_server_id':data.get('source_server_id'), 
             'task_id':data.get('task_id')}

    def recycle_resource_by_taskid(self, task_id):
        url = '%s/%s' % (self.root_url, recycle_resource_url)
        data = {'task_id': task_id}
        ret, result = self.http_post(url, data)
        if ret:
            if result.get('error') == 0:
                return (
                 True, result.get('data'))
        self.MAIN_THREAD_LOGGER.error('recycle resource request error:{}'.format(result))
        return (False, result)

    def ai_version_verify(self, test_id, game_id, game_version):
        url = '%s/%s' % (self.root_url, test_id_verify_url)
        data = {'test_id':test_id,  'game_id':game_id,  'game_version':game_version}
        ret, result = self.http_post(url, data)
        if ret and type(result) == dict:
            self.MAIN_THREAD_LOGGER.debug('ai_version_verify result: {}'.format(result))
            return (
             result.get('data'), result.get('errstr'))
        else:
            self.MAIN_THREAD_LOGGER.error('test_id verify error:{}'.format(result))
            return (False, 'ai_version_verify request failed: {}'.format(result))