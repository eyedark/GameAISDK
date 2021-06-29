# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/start_service.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 12402 bytes
import configparser, logging, os, threading, time, traceback, cv2, json
from .aiclientapi.network_client import NetworkClient
from .aiclientapi.tool_manage import communicate_config as com_config
from .device_remote_interaction.action_threads.action_execute_thread import ActionExecuteThread
from .device_remote_interaction.action_threads.action_recv_thread import ActionRecvThread
from .device_remote_interaction.common import network_check
from .device_remote_interaction.device_interface.device_api import get_device_api_instance
from .register_obj.state_notify import StateNotify
from .device_remote_interaction.device_interface.config import IniConfigParser
CHECK_OVER_TIME = 10
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(__dir__))
_device_cfg_path = os.path.join(__dir__, 'cfg/device_cfg/device.ini')

class ActionExecute(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.state_notify_inst = StateNotify()
        self.ai_client = NetworkClient(self.state_notify_inst)
        self.need_stop = False
        self.device_api_inst = None
        self.ai_client_lock = threading.RLock()
        self.action_recv_thread = None
        self.action_execute_thread = None
        self.heart_beat_thread = None

    def init(self):
        success = self.ai_client.init()
        if success is not True:
            return False
        return self.create_action_recv_thread()

    def finish(self):
        self.MAIN_THREAD_LOGGER.info('main thread terminating......')
        com_config.terminate = True
        error_str, adb_ret = ('', False)
        recycle_ret = True
        try:
            if self.device_api_inst is not None:
                adb_ret = self.device_api_inst.finish()
                if not adb_ret:
                    error_str += '-' + 'finish adb tool error'
            else:
                adb_ret = True
        except Exception as err:
            error_str += '-' + str(err)
            self.MAIN_THREAD_LOGGER.error('finish adb tool error: {}'.format(err))

        if not adb_ret or not recycle_ret:
            self.MAIN_THREAD_LOGGER.error(error_str)
            self.ai_client.finish_exception(error_str)
            self.MAIN_THREAD_LOGGER.info('finish over, failed')
            return False
        self.ai_client.on_service_over()
        self.MAIN_THREAD_LOGGER.info('finish over, success')
        self.MAIN_THREAD_LOGGER.info('It needs few seconds to quit, please wait.')
        return True

    def create_recv_execute_thread(self):
        try:
            self.action_execute_thread = ActionExecuteThread(self.state_notify_inst)
            self.action_execute_thread.init()
            self.action_execute_thread.daemon = True
            self.action_execute_thread.start()
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('start action execute thread error: {}'.format(err))
            return False

        self.MAIN_THREAD_LOGGER.info('has start ActionRecvThread thread and ActionExecuteThread')
        return True

    def create_action_recv_thread(self):
        try:
            self.action_recv_thread = ActionRecvThread(self.ai_client, self.ai_client_lock)
            self.action_recv_thread.daemon = True
            self.action_recv_thread.start()
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('start action recv thread error: {}'.format(err))
            return False

        return True

    def save_device_config(self, source_info):
        """ 根据获取的配置信息，保存到aiclient/cfg/device_cfg/device.ini

        :param source_info:
        :return:
        """
        global _device_cfg_path
        if not source_info:
            self.MAIN_THREAD_LOGGER.warning('empty source info')
            return False
        if not os.path.exists(_device_cfg_path):
            self.MAIN_THREAD_LOGGER.warning('file(%s) is not found' % _device_cfg_path)
            return False
        try:
            cfg_parser = IniConfigParser(_device_cfg_path)
            if 'device_type' in source_info:
                cfg_parser.set('device', 'device_type', source_info['device_type'])
            if 'platform' in source_info:
                cfg_parser.set('device', 'platform', source_info['platform'])
            if 'long_edge' in source_info:
                cfg_parser.set('device', 'long_edge', str(source_info['long_edge']))
            if 'window_size' in source_info:
                cfg_parser.set('pc_device', 'window_size', source_info['window_size'])
            if 'query_path' in source_info:
                cfg_parser.set('pc_device', 'query_path', source_info['query_path'])
            cfg_parser.save()
            return True
        except:
            exp = traceback.format_exc()
            self.MAIN_THREAD_LOGGER.error(exp)
            return False

    def run(self):
        is_connected = self.ai_client.build_connection()
        if not is_connected:
            self.MAIN_THREAD_LOGGER.error('network connection failed, main thread will exist')
            return
        self.MAIN_THREAD_LOGGER.info('begin to get source info')
        message = self.get_source_info()
        self.MAIN_THREAD_LOGGER.info('get the resource is {}'.format(message))
        success = self.save_device_config(message)
        if success is not True:
            self.MAIN_THREAD_LOGGER.error('change device config failed, main thread will exist')
            return
        success = self.start_device()
        if success is not True:
            self.MAIN_THREAD_LOGGER.error('start the device failed, main thread will exist')
            return
        success = self.create_recv_execute_thread()
        if success is not True:
            self.MAIN_THREAD_LOGGER.error('start the execute thread  failed, main thread will exist')
            return
        self.start_game()
        none_frame_start_time = None
        restart_time = None
        while not com_config.terminate:
            if self.need_stop or not com_config.is_ai_service_state_ok or not self.ai_client.heart_beat_ok():
                self.MAIN_THREAD_LOGGER.error('main thread exit, need_stop: {}, is_ai_service_state_ok: {}, heart_beat_ok: {}'.format(self.need_stop, com_config.is_ai_service_state_ok, self.ai_client.heart_beat_ok()))
                break
            if com_config.ui_action_on and not com_config.send_frame:
                time.sleep(0.002)
                continue
            else:
                send_start_time = time.time()
                try:
                    img, extend_data, error_str = self.device_api_inst.GetFrame()
                except Exception as err:
                    img = None
                    extend_data = None
                    error_str = 'get screen exception: {}'.format(err)

                if img is None:
                    get_img_interval = 5 if error_str else 0.002
                    if self.device_api_inst.ready:
                        if none_frame_start_time is None:
                            none_frame_start_time = time.time()
            if time.time() - none_frame_start_time > self.ai_client.max_none_frame_time:
                if self.device_api_inst.max_restart_time == 0:
                    self.ai_client.none_frame_exception(self.ai_client.max_none_frame_time, error_str)
                    break
                else:
                    self.MAIN_THREAD_LOGGER.warning('failed to get frame in {} seconds: {}'.format(self.ai_client.max_none_frame_time, error_str))
                    restart_flag = False
                    if restart_time is None:
                        restart_time = time.time()
                    while time.time() - restart_time <= self.device_api_inst.max_restart_time:
                        self.MAIN_THREAD_LOGGER.info('try to restart device. {} seconds left'.format(self.device_api_inst.max_restart_time - time.time() + restart_time))
                        restart_flag = self.device_api_inst.restart()
                        if restart_flag:
                            none_frame_start_time = None
                            break
                        time.sleep(5)

                if not restart_flag:
                    self.ai_client.bad_device_exception(self.device_api_inst.max_restart_time)
                    break
                time.sleep(get_img_interval)
                continue
            else:
                restart_time = None
                none_frame_start_time = None
                with self.ai_client_lock:
                    self.ai_client.send_img_msg(img, extend_data)
                if com_config.ui_action_on:
                    com_config.send_frame = False
                send_end_time = time.time()
                if self.ai_client.max_send_interval_time > send_end_time - send_start_time:
                    time.sleep(self.ai_client.max_send_interval_time - (send_end_time - send_start_time))
                else:
                    self.MAIN_THREAD_LOGGER.warning('send img time has exceed fixed time, actually time:{expend_time}'.format(expend_time=send_end_time - send_start_time))

        self.MAIN_THREAD_LOGGER.info('Stop sending frames...')

    def register_object(self, obj):
        self.ai_client.state_notify_obj_register(obj)

    def get_taskid(self):
        return self.ai_client.get_task_id()

    def recycle_resource(self):
        return self.ai_client.recycle_resource_by_taskid()

    def start_game(self):
        self.ai_client.start_ai()

    def get_source_info(self):
        st = time.time()
        while 1:
            ct = time.time()
            if ct - st > 30:
                break
            self.ai_client.send_source_info_request()
            if network_check.source_info is None or len(network_check.source_info) == 0:
                time.sleep(0.1)
            continue
        return network_check.source_info

    def start_device(self):
        try:
            self.device_api_inst = get_device_api_instance()
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('get device instance failed')
            self.ai_client.adb_tool_init_exception(err)
            return False

        return True

    def restart_ai(self):
        self.ai_client.restart_ai()

    def pause_ai(self):
        self.ai_client.pause_ai()

    def restore_ai(self):
        self.ai_client.restore_ai()

    def stop_ai(self):
        self.need_stop = True
        self.finish()


if __name__ == '__main__':
    cv2.imread('')
    ae = ActionExecute()
    ret = ae.init()
    if not ret:
        exit()
    ae.run()