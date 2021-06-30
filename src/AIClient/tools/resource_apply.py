# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\tools\resource_apply.py
# Compiled at: 2021-02-23 16:10:42
# Size of source mod 2**32: 2784 bytes
import os, sys, json, telnetlib, logging
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from aiclient.aiclientapi.resource_apply.resource_apply import get_resource_apply_instance
SAVE_PATH = os.path.join(ROOT_DIR, 'tools/resource_result.json')

class ResourceApply(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.resource_apply_inst = get_resource_apply_instance()

    def init(self):
        ret, error_str = self.resource_apply_inst.init()
        return (ret, error_str)

    def save_data(self, json_data):
        if not os.path.exists(os.path.dirname(SAVE_PATH)):
            os.makedirs(os.path.dirname(SAVE_PATH))
        try:
            json.dump(json_data, open(SAVE_PATH, 'w'))
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('save resource apply result error: {}'.format(err))

    def do_telnet(self, ip, port):
        try:
            tn = telnetlib.Telnet()
            tn.open(ip, port=port, timeout=10)
            self.MAIN_THREAD_LOGGER.debug('ip: {}, port: {} is available'.format(ip, port))
        except Exception as err:
            self.MAIN_THREAD_LOGGER.debug('ip: {}, port: {} is not available, error: {}'.format(ip, port, err))

    def ports_check(self, service_info):
        if type(service_info) != dict or not service_info.__contains__('ip') or not service_info.__contains__('port1') or not service_info.__contains__('port2'):
            self.MAIN_THREAD_LOGGER.error('pre_apply_resource failed, can not telnet ip:port, service_info: {}'.format(service_info))
            return
        ip = service_info.get('ip')
        port1 = service_info.get('port1')
        port2 = service_info.get('port2')
        self.do_telnet(ip, port1)
        self.do_telnet(ip, port2)

    def run(self):
        service_info, error_str = self.resource_apply_inst.apply_resource()
        if service_info is None:
            self.MAIN_THREAD_LOGGER.error('create service error: service_info -> {}'.format(service_info))
            return
        self.MAIN_THREAD_LOGGER.info('create_service result: service_info -> {}'.format(service_info))
        self.save_data(service_info)
        self.ports_check(service_info)


if __name__ == '__main__':
    resource_apply_main_inst = ResourceApply()
    ret, error_str = resource_apply_main_inst.init()
    if not ret:
        exit()
    resource_apply_main_inst.run()