# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\network_client.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 14698 bytes
import time, os, telnetlib, json, logging
from .tool_manage import communicate_config as com_config
from .communication import instance_factory as ins_fact
from .tool_manage import parameter_context as para_context
from .performance_profile.speed_check import speed_check_inst
from ..device_remote_interaction.common import define
from .resource_apply.resource_apply import get_resource_apply_instance
from ..device_remote_interaction.common import network_check
MAX_SEND_INTERVAL = 0.05
IMG_NUM_RECORD_INTERVAL = 20
MAX_NONE_FRAME_TIME = 30
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_FILE = os.path.join(WORK_DIR, 'cfg/network_comm_cfg/communication_cfg.ini')
WETESTIP_FILE = os.path.join(WORK_DIR, 'cfg/network_comm_cfg/wetestip_map.json')

class NetworkClient(object):

    def __init__(self, state_notify_inst):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.NETWORK_IO_LOGGER = logging.getLogger('network_io')
        self.img_id = 0
        self.action_id = 0
        self.game_has_start = False
        self.recv_thread = None
        self.pre_send_time = None
        self.max_send_interval_time = MAX_SEND_INTERVAL
        self.max_none_frame_time = MAX_NONE_FRAME_TIME
        self.send_img_type = define.RAW_IMG_SEND_TYPE
        self.para_data = {}
        self.wetest_ip = None
        self.communicate_instance = None
        self.is_test_speed = False
        self.resource_apply_inst = None
        self.game_state = define.GAME_STATE_NONE
        self.state_notify_inst = state_notify_inst
        self.is_heart_beat_ok = True
        self.is_connection_ok = False

    def init(self):
        ret, error_str = self.state_notify_inst.init()
        if not ret:
            self.MAIN_THREAD_LOGGER.error('state_notify init error: {}'.format(error_str))
            return False
        ret, self.para_data, error_str = para_context.para_context_inst.init(CFG_FILE)
        if not ret:
            self.MAIN_THREAD_LOGGER.error(error_str)
            self.state_notify_inst.on_exception(exception_type=(self.state_notify_inst.CONFIG_PARAMS_LOAD_ERROR), description=error_str)
            return False
        if not os.path.exists(WETESTIP_FILE):
            self.MAIN_THREAD_LOGGER.error('wetest_ip loaded error: can not find wetestip_map.json at {}'.format(WETESTIP_FILE))
            return False
        with open(WETESTIP_FILE) as (f):
            self.wetest_ip = json.load(f)
        self.img_id = 0
        self.action_id = 0
        self.game_has_start = False
        self.recv_thread = None
        self.pre_send_time = None
        self.max_send_interval_time = self.para_data.get('max_send_interval', MAX_SEND_INTERVAL)
        self.max_none_frame_time = self.para_data.get('max_none_frame_time', MAX_NONE_FRAME_TIME)
        self.is_test_speed = self.para_data.get('process_speed_test', False)
        self.resource_apply_inst = get_resource_apply_instance()
        ret, error_str = self.resource_apply_inst.init()
        if not ret:
            self.MAIN_THREAD_LOGGER.error(error_str)
            self.state_notify_inst.on_exception(exception_type=(self.state_notify_inst.CONFIG_PARAMS_LOAD_ERROR), description=error_str)
            return False
        ret, error_str = self.resource_apply_inst.args_verify()
        if not ret:
            self.MAIN_THREAD_LOGGER.error(error_str)
            self.state_notify_inst.on_exception(exception_type=(self.state_notify_inst.ARGS_VERIFY_EXCEPTION), description=error_str)
            return False
        else:
            ret, self.communicate_instance = self.create_communication_instance()
            if not ret:
                self.MAIN_THREAD_LOGGER.error('create_communication_instance failed')
                return False
            return True

    def create_communication_instance(self):
        auto_apply_resource = self.para_data.get('auto_apply_resource', 0)
        if auto_apply_resource:
            self.MAIN_THREAD_LOGGER.warning('use auto apply resource pattern')
            service_info, error_str = self.resource_apply_inst.get_service_info()
            if service_info is None:
                self.MAIN_THREAD_LOGGER.error('auto apply resource failed, error: {}'.format(error_str))
                self.state_notify_inst.on_resource_apply_state(com_config.RESOURCE_APPLY_FAILURE, error_str)
                return (False, None)
            try:
                self.para_data['ip'] = service_info['ip']
                self.para_data['port1'] = service_info['port1']
                self.para_data['port2'] = service_info['port2']
                self.para_data['key'] = service_info['key']
                self.para_data['task_id'] = service_info['task_id']
                self.para_data['source_server_id'] = service_info['source_server_id']
                self.para_data['service'] = self.resource_apply_inst.get_service_type()
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('modify attr in auto apply resource:{}'.format(err))
                self.state_notify_inst.on_resource_apply_state(com_config.RESOURCE_APPLY_FAILURE, err)
                return (False, None)

            self.state_notify_inst.on_resource_apply_state(com_config.RESOURCE_APPLY_SUCCESS, 'apply resource success')
        if os.environ.get('PLATFORM_IP'):
            ip = self.para_data['ip']
            if ip in self.wetest_ip:
                self.para_data['ip'] = self.wetest_ip[ip]
            else:
                self.MAIN_THREAD_LOGGER.error('unkown ip {}'.format(ip))
                return (False, None)
        ret, comm_instace, error_str = ins_fact.create_comm_instance(self.para_data)
        if not ret:
            self.MAIN_THREAD_LOGGER.error(error_str)
            self.state_notify_inst.on_exception(self.state_notify_inst.REMOTE_COMMUNICATION_INIT_ERROR, error_str)
        return (
         ret, comm_instace)

    def reconnect(self):
        self.MAIN_THREAD_LOGGER.info('reconnect to tcp:{}, port:{} {}'.format(self.para_data['ip'], self.para_data['port1'], self.para_data['port2']))
        ret, comm_instace, error_str = ins_fact.create_comm_instance(self.para_data)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('reconnect failed: {}' % error_str)
            self.state_notify_inst.on_exception(self.state_notify_inst.REMOTE_COMMUNICATION_INIT_ERROR, error_str)
            return False
        else:
            self.MAIN_THREAD_LOGGER.info('Reconnected...')
            self.communicate_instance = comm_instace
            return True

    def set_heart_beat(self, is_heart_beat_ok):
        self.is_heart_beat_ok = is_heart_beat_ok
        self.MAIN_THREAD_LOGGER.warning('set heart beat state: {}'.format(self.is_heart_beat_ok))

    def heart_beat_ok(self):
        return self.is_heart_beat_ok

    def get_connection_result(self):
        return self.is_connection_ok

    def do_telnet(self, ip, port):
        try:
            tn = telnetlib.Telnet()
            tn.open(ip, port=port, timeout=10)
            self.MAIN_THREAD_LOGGER.debug('ip: {}, port: {} is available'.format(ip, port))
        except Exception as err:
            self.MAIN_THREAD_LOGGER.debug('ip: {}, port: {} is not available, error: {}'.format(ip, port, err))

    def ports_check(self):
        try:
            self.MAIN_THREAD_LOGGER.debug('ports_check......')
            ip = self.para_data['ip']
            port1 = self.para_data['port1']
            port2 = self.para_data['port2']
            self.do_telnet(ip, port1)
            self.do_telnet(ip, port2)
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('ports_check exception: {}'.format(err))

    def build_connection(self):
        self.ports_check()
        self.state_notify_inst.on_resource_apply_state(com_config.NETWORK_CONNECTTING, 'building connection')
        max_connection_time = 300
        start_time = time.time()
        while 1:
            self.check_network()
            self.MAIN_THREAD_LOGGER.debug('send heart beat, wait for response........')
            time.sleep(3)
            current_time = time.time()
            if network_check.has_recv_rep or current_time - start_time > max_connection_time:
                break

        self.ports_check()
        if network_check.has_recv_rep:
            self.MAIN_THREAD_LOGGER.info('build connection succeesfully')
            self.state_notify_inst.on_ai_service_state(com_config.AI_SERVICE_READY)
            self.is_connection_ok = True
            return True
        else:
            self.MAIN_THREAD_LOGGER.error('build connection failed, exit')
            self.state_notify_inst.on_resource_apply_state(com_config.NETWORK_ABNORMAL)
            return False

    def send_img_msg(self, img_data, extend_data=None):
        self.NETWORK_IO_LOGGER.debug('send frame data, frameIndex={}'.format(self.img_id))
        self.communicate_instance.send_img_msg((self.img_id), img_data, extend_info=extend_data)
        if com_config.GAME_STATE != self.game_state:
            self.NETWORK_IO_LOGGER.info('game state changed, {last_state} -> {new_state}'.format(last_state=(self.game_state),
              new_state=(com_config.GAME_STATE)))
            self.game_state = com_config.GAME_STATE
        if self.game_state == define.GAME_STATE_START:
            speed_check_inst.add_img(self.img_id)
        if self.img_id < 200:
            if self.img_id % IMG_NUM_RECORD_INTERVAL == 0:
                self.NETWORK_IO_LOGGER.info('img_id:{}'.format(self.img_id))
        else:
            if self.img_id % (IMG_NUM_RECORD_INTERVAL * 25) == 0:
                self.NETWORK_IO_LOGGER.info('img_id:{}'.format(self.img_id))
        self.img_id += 1

    def check_network(self):
        self.communicate_instance.send_check_network()

    def pause_ai(self):
        self.communicate_instance.send_pause_ai()

    def restore_ai(self):
        self.communicate_instance.send_restore_ai()

    def change_game_state(self, game_state):
        self.MAIN_THREAD_LOGGER.info('game state changed in change_game_state, {last_state} -> {new_state}'.format(last_state=(self.game_state),
          new_state=game_state))
        self.communicate_instance.send_game_state(game_state)

    def start_ai(self):
        service = self.para_data.get('service', define.SERVICE_UI_AI)
        if service == define.SERVICE_AI:
            self.MAIN_THREAD_LOGGER.info('start ai service')
            self.change_game_state(define.GAME_STATE_START)
            com_config.GAME_STATE = define.GAME_STATE_START
            com_config.ui_action_on = False
        elif service == define.SERVICE_UI_AI:
            self.MAIN_THREAD_LOGGER.info('start ui+ai service')
            com_config.ui_action_on = True

    def send_source_info_request(self):
        self.communicate_instance.send_source_info_request()

    def end_ai(self):
        self.communicate_instance.send_end_ai()

    def restart_ai(self):
        self.communicate_instance.send_restart_ai()

    def recv_msg(self):
        msg = self._recv_msg()
        return msg

    def _recv_msg(self):
        while self.communicate_instance is None:
            time.sleep(1)

        msg = self.communicate_instance.recv_msg()
        if msg is not None:
            img_id_recv = msg.get('img_id', define.DEFAULT_IMG_ID)
            if com_config.IS_TEST_SPEED:
                speed_check_inst.caculate_ai_process_time(img_id_recv)
                self.NETWORK_IO_LOGGER.info('recv msg:{}'.format(msg))
            img_id_sent = self.img_id - 1
            if com_config.ui_action_on:
                if not img_id_recv == -1:
                    if not img_id_recv == img_id_sent:
                        self.NETWORK_IO_LOGGER.info('img_id mismatching: sent {}, received {}'.format(img_id_sent, img_id_recv))
                        msg = None
        return msg

    def state_notify_obj_register(self, obj):
        self.state_notify_inst.register_obj(obj, self.para_data.get('task_id'))

    def get_task_id(self):
        if not self.para_data.__contains__('task_id'):
            self.MAIN_THREAD_LOGGER.warning('not task_id to get')
            return
        else:
            task_id = self.para_data.get('task_id')
            self.MAIN_THREAD_LOGGER.info('return task_id:{}'.format(task_id))
            return task_id

    def recycle_resource_by_taskid(self):
        task_id = self.get_task_id()
        if task_id is None:
            self.MAIN_THREAD_LOGGER.warning('task_id is None, can not recycle resource')
            return (True, 'task_id is None, can not recycle resource')
        else:
            ret = self.resource_apply_inst.recycle_resource_by_taskid(task_id)
            if not ret:
                self.MAIN_THREAD_LOGGER.error('recycle_resource_by_taskid')
                return (False, 'recycle_resource_by_taskid, task_id: {}'.format(task_id))
            return (True, '')

    def on_service_over(self):
        self.state_notify_inst.on_service_over()

    def none_frame_exception(self, max_none_fram_time, error_str=''):
        error_str = 'none frame exception, max none frame time should < {} (s), specific reason: {}'.format(max_none_fram_time, error_str)
        self.state_notify_inst.on_exception(self.state_notify_inst.NONE_FRAME_EXCEPTION, error_str)

    def bad_device_exception(self, max_restart_time):
        error_str = 'bad device exception, failed to restart device in {} (s)'.format(max_restart_time)
        self.state_notify_inst.on_exception(self.state_notify_inst.BAD_DEVICE_EXCEPTION, error_str)

    def finish_exception(self, error_str):
        self.state_notify_inst.on_exception(self.state_notify_inst.FINISH_EXCEPTION, error_str)

    def adb_tool_init_exception(self, error_str):
        self.state_notify_inst.on_exception(self.state_notify_inst.ADB_TOOL_INIT_EXCEPTION, error_str)