# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\resource_apply\resource_apply.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 12211 bytes
import os, configparser, json, argparse, logging, uuid
from .communication.request_service import RequestService
from ..tool_manage import communicate_config as com_config
from ..args_helps import Args
__dir__ = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__dir__)))
resource_cfg_path = os.path.join(os.path.dirname(os.path.dirname(__dir__)), 'cfg/resource_apply_cfg/game.ini')
pre_apply_result_path = os.path.join(WORK_DIR, 'tools', 'resource_result.json')

class ResourceApply(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')
        self.resource_apply_url = ''
        self.game_data = {}
        self.user = ''
        self.max_post_timeout = None
        self.pre_apply = False
        self.request_service_inst = RequestService()

    def init(self):
        ret, config, error_str = self._load_parameter(resource_cfg_path)
        if not ret:
            return (ret, error_str)
        else:
            if config.__contains__('communication'):
                if config['communication'].__contains__('resource_apply_root_url'):
                    self.resource_apply_url = config['communication']['resource_apply_root_url']
            else:
                self.MAIN_THREAD_LOGGER.error('no resource_apply_root_url in config file')
                return (False, 'no resource_apply_root_url in config file')
                if config.__contains__('apply_condition'):
                    if config['apply_condition'].__contains__('pre_apply'):
                        self.pre_apply = config.getboolean('apply_condition', 'pre_apply')
                else:
                    return (False, 'no pre_apply[apply_condition] in config file')
                ret, error_str = self.load_game_info(config)
                if not ret:
                    return (
                     ret, error_str)
            self.request_service_inst.init(self.resource_apply_url, self.user, self.max_post_timeout)
            return (ret, '')

    def load_game_info(self, config):
        if os.environ.get('GAME_USE_ENV_VARIABLE'):
            use_env_variable = int(os.environ.get('GAME_USE_ENV_VARIABLE'))
        elif config.__contains__('resource'):
            if config['resource'].__contains__('use_env_variable'):
                use_env_variable = config.getboolean('resource', 'use_env_variable')
        else:
            self.MAIN_THREAD_LOGGER.error('game.ini config file not contain use_env_variable')
            return (False, 'game.ini config file not contain use_env_variable')
        if use_env_variable:
            try:
                self.MAIN_THREAD_LOGGER.info('use env variable to load game info')
                user = os.environ.get('USER')
                game_id = os.environ.get('GAME_ID')
                scene_id = os.environ.get('SCENE_ID')
                resolution = os.environ.get('RESOLUTION')
                service = int(os.environ.get('SERVICE', 1))
                use_time = float(os.environ.get('USE_TIME', 3.0))
                max_post_timeout = int(os.environ.get('MAX_POST_TIMEOUT', 300))
                image_name = os.environ.get('IMAGE_NAME', '')
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('use env variable to load game info error, error: {}'.format(err))
                return (False, 'use env variable to load game info error, error: {}'.format(err))

        else:
            self.MAIN_THREAD_LOGGER.info('use config file to load game info')
            if not config.__contains__('resource'):
                self.MAIN_THREAD_LOGGER.error('game.ini config file do not contain resource section')
                return (False, 'game.ini config file do not contain resource section')
            else:
                try:
                    user = config.get('resource', 'user')
                    game_id = config.get('resource', 'game_id')
                    scene_id = config.get('resource', 'scene_id')
                    resolution = config.getint('resource', 'resolution_type')
                    service = config.getint('resource', 'service')
                    use_time = config.getfloat('resource', 'use_time')
                    max_post_timeout = config.getint('resource', 'max_post_timeout')
                    image_name = config.get('resource', 'image_name')
                except Exception as err:
                    self.MAIN_THREAD_LOGGER.error('use config to load game info error: {}'.format(err))
                    return (False, 'use config to load game info error: {}'.format(err))

                ret, error_str = self.check_game_info(user, game_id, scene_id, resolution, service, use_time, max_post_timeout, image_name)
                return (ret, error_str)

    def check_game_info(self, user, game_id, scene_id, resolution, service, use_time, max_post_timeout, image_name):
        if user is None:
            self.MAIN_THREAD_LOGGER.error('user is None')
            return (False, 'user is None')
        else:
            if game_id is None:
                self.MAIN_THREAD_LOGGER.error('game_id is None')
                return (False, 'game_id is None')
            elif scene_id is None:
                self.MAIN_THREAD_LOGGER.error('scene_id is None')
                return (False, 'scene_id is None')
            else:
                if resolution is None:
                    self.MAIN_THREAD_LOGGER.error('resolution is None')
                    return (False, 'resolution is None')
                else:
                    if service is None:
                        self.MAIN_THREAD_LOGGER.error('service is None')
                        return (False, 'service is None')
                    if use_time is None:
                        self.MAIN_THREAD_LOGGER.error('use_time is None')
                        return (False, 'use_time is None')
                    if max_post_timeout is None:
                        self.MAIN_THREAD_LOGGER.error('max_post_timeout is None')
                        return (False, 'max_post_timeout is None')
                app_id = str(uuid.uuid4())
                self.game_data = {'game_id':game_id,  'scene_id':scene_id,  'app_id':app_id,  'resolution':resolution,  'service':service, 
                 'use_time':use_time}
                if image_name != '':
                    if image_name is not None:
                        self.game_data['image'] = image_name
            self.user = user
            self.max_post_timeout = max_post_timeout
            self.MAIN_THREAD_LOGGER.info('game_data:{}'.format(self.game_data))
            self.MAIN_THREAD_LOGGER.info('user: {}'.format(self.user))
            return (True, '')

    def _load_parameter(self, cfg_file):
        if not os.path.exists(cfg_file):
            self.MAIN_THREAD_LOGGER.error('cfg_file not exist:{}'.format(cfg_file))
            return (
             False, None, 'game.ini config file not exist:{}'.format(cfg_file))
        else:
            try:
                config = configparser.ConfigParser(strict=False)
                config.read(cfg_file)
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('read game.ini config file error: {}'.format(err))
                return (False, None, 'read game.ini config file error: {}'.format(err))

            return (True, config, '')

    def load_pre_apply_result(self):
        if not os.path.exists(pre_apply_result_path):
            self.MAIN_THREAD_LOGGER.error('pre_apply_result_path not exist, path: {}'.format(pre_apply_result_path))
            return (
             False, 'pre_apply_result_path not exist, path: {}'.format(pre_apply_result_path))
        else:
            try:
                data = json.load(open(pre_apply_result_path))
            except Exception as err:
                self.MAIN_THREAD_LOGGER.error('load pre_apply_result error: {}, path: {}'.format(err, pre_apply_result_path))
                return (False, 'load pre_apply_result error: {}, path: {}'.format(err, pre_apply_result_path))

            if not data.__contains__('ip') or not data.__contains__('port1') or not data.__contains__('port2') or not data.__contains__('key') or not data.__contains__('source_server_id') or not data.__contains__('task_id'):
                self.MAIN_THREAD_LOGGER.error('data not contain ip, port1, port2, key, source_server_id or task_id, data: {}'.format(data))
                return (
                 False, 'data not contain ip, port1, port2, key, source_server_id or task_id, data: {}'.format(data))
            return (
             True, data)

    def get_service_info(self):
        if self.pre_apply:
            ret, result = self.load_pre_apply_result()
            if ret:
                self.MAIN_THREAD_LOGGER.debug('load pre_apply_result successfully, data: {}'.format(result))
                return (
                 result, '')
        self.MAIN_THREAD_LOGGER.warning('no pre_apply_result, will apply resource first')
        return self.apply_resource()

    def apply_resource(self):
        ret, result = self.request_service_inst.create_ai_service(self.game_data)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('create service error:{}'.format(result))
            return (
             None, result)
        else:
            return (
             result, '')

    def recycle_resource_by_taskid(self, task_id):
        ret, result = self.request_service_inst.recycle_resource_by_taskid(task_id)
        if not ret:
            self.MAIN_THREAD_LOGGER.error('recycle_resource_by_taskid error:{}'.format(result))
            return False
        else:
            return True

    def get_service_type(self):
        return self.game_data.get('service')

    def parse_testid_and_verify(self):
        if os.environ.get('NO_ARGPARSE'):
            args = Args('0', 0, '0', 0)
        else:
            parse = argparse.ArgumentParser()
            parse.add_argument('-t', '--test_id', default='0', type=str)
            parse.add_argument('-g', '--game_id', default='0', type=int)
            parse.add_argument('-gv', '--game_version', default='0', type=str)
            parse.add_argument('-rts', '--runtimes', default='0', type=int)
            args, _ = parse.parse_known_args()
        try:
            if com_config.test_id == args.test_id:
                if com_config.game_id == args.game_id:
                    if com_config.game_version == args.game_version:
                        com_config.runtimes = args.runtimes
                        self.MAIN_THREAD_LOGGER.warning('use default test_id: {}, game_id: {}, game_version: {}, runtimes: {} (0 for unlimited)'.format(com_config.test_id, com_config.game_id, com_config.game_version, com_config.runtimes))
                        return (True, '')
        except Exception as err:
            self.MAIN_THREAD_LOGGER.error('parse_test_id error: {}'.format(err))
            return (False, 'parse test_id error: {}'.format(err))

        com_config.test_id = args.test_id
        com_config.game_id = args.game_id
        com_config.game_version = args.game_version
        com_config.runtimes = args.runtimes
        self.MAIN_THREAD_LOGGER.debug('input test_id: {}, game_id: {}, game_version: {}, runtimes: {} (0 for unlimited)'.format(com_config.test_id, com_config.game_id, com_config.game_version, com_config.runtimes))
        ret, error_str = self.request_service_inst.ai_version_verify(com_config.test_id, com_config.game_id, com_config.game_version)
        if not ret:
            return (False, error_str)
        else:
            return (True, '')

    def args_verify(self):
        return self.parse_testid_and_verify()


resource_apply_inst = None

def get_resource_apply_instance():
    global resource_apply_inst
    if resource_apply_inst is None:
        resource_apply_inst = ResourceApply()
    return resource_apply_inst


if __name__ == '__main__':
    resource_apply_inst = ResourceApply()
    ret = resource_apply_inst.init()
    if not ret:
        exit()
    resource_apply_inst.get_service_info()