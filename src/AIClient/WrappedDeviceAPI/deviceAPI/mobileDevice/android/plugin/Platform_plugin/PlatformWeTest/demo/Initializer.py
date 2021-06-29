# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/Initializer.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 7754 bytes
import time, logging, pathlib
from .common.AdbTool import AdbTool
from concurrent.futures import ThreadPoolExecutor, wait
logger = logging.getLogger(__name__)

class Initializer:
    TOUCH_SEVER_PORT = 1111
    CLOUD_SCREEN_PORT = 1113
    INPUT_SERVER_PORT = 1115

    def __init__(self, resource_dir, serial=None):
        self._Initializer__adb = AdbTool(serial)
        self._Initializer__resource_dir = resource_dir
        self._Initializer__thread_pool = ThreadPoolExecutor(max_workers=3)
        self._Initializer__touch_future = None
        self._Initializer__input_future = None
        self._Initializer__cloudscreen_future = None
        self._Initializer__running = False
        self.abi = None
        self.sdk = None
        self.abi, self.sdk = self._Initializer__get_abi_sdk()

    def __get_abi_sdk(self):
        if self.abi is None:
            self.abi = self._Initializer__adb.cmd('shell', 'getprop', 'ro.product.cpu.abi').communicate()[0].decode('utf-8', 'ignore').strip()
        if self.sdk is None:
            self.sdk = int(self._Initializer__adb.cmd('shell', 'getprop', 'ro.build.version.sdk').communicate()[0].decode('utf-8', 'ignore').strip())
        logger.info('adi={}, sdk={}'.format(self.abi, self.sdk))
        return (self.abi, self.sdk)

    def __install_touch_server(self):
        try:
            logger.info('Install touch server...')
            abi, _ = self._Initializer__get_abi_sdk()
            file_path = '{}/touchserver/binary/{}/touchserver'.format(self._Initializer__resource_dir, abi)
            if not pathlib.Path(file_path).is_file():
                raise Exception('touchserver is not exsit')
            logger.info('Push touch server to device')
            self._Initializer__adb.cmd_wait('push', file_path, '/data/local/tmp/wetest')
            self._Initializer__adb.cmd_wait('shell', 'chmod', '0755', '/data/local/tmp/wetest/touchserver')
            logger.info('Install touch server complete')
        except Exception as e:
            logger.error('error: %s', e)
            raise e

    def __install_cloudscreen_server(self):
        try:
            logger.info('Install cloud screen...')
            abi, sdk = self._Initializer__get_abi_sdk()
            so_path = '{}/cloudscreen/libs/android-{}/{}/cloudscreen.so'.format(self._Initializer__resource_dir, sdk, abi)
            if not pathlib.Path(so_path).is_file():
                raise Exception('cloudscreen.so is not exsit')
            self._Initializer__adb.cmd_wait('push', so_path, '/data/local/tmp/wetest')
            binary_path = '{}/cloudscreen/binary/{}/cloudscreen'.format(self._Initializer__resource_dir, abi)
            if not pathlib.Path(binary_path).is_file():
                raise Exception('cloudscreen.so is not exsit')
            logger.info('Push cloudscreen to device')
            self._Initializer__adb.cmd_wait('push', binary_path, '/data/local/tmp/wetest/')
            self._Initializer__adb.cmd_wait('shell', 'chmod', '0755', '/data/local/tmp/wetest/cloudscreen')
            logger.info('Install cloud screen complete')
        except Exception as e:
            logger.error('error: %s', e)
            raise e

    def __install_input_server(self):
        try:
            logger.info('Install input server...')
            file_path = '{}/input/inputserver'.format(self._Initializer__resource_dir)
            if not pathlib.Path(file_path).is_file():
                raise Exception('inputserver is not exsit')
            self._Initializer__adb.cmd_wait('push', file_path, '/data/local/tmp/wetest')
            self._Initializer__adb.cmd_wait('shell', 'chmod', '0755', '/data/local/tmp/wetest/inputserver')
            file_path = '{}/input/inputserver.jar'.format(self._Initializer__resource_dir)
            if not pathlib.Path(file_path).is_file():
                raise Exception('inputserver.jar is not exsit')
            self._Initializer__adb.cmd_wait('push', file_path, '/data/local/tmp/wetest')
            logger.info('Install input server complete')
        except Exception as e:
            logger.error('error: %s', e)
            raise e

    def forward(self, local_port, remote_port):
        if self._Initializer__adb.forward(local_port, remote_port) != 0:
            raise Exception('bind {} to {} error:'.format(local_port, remote_port))

    def __launch_touchserver(self):
        while self._Initializer__running is True:
            try:
                logger.info('touchserver run begin...')
                p = self._Initializer__adb.cmd('shell', '/data/local/tmp/wetest/touchserver')
                time.sleep(0.5)
                while self._Initializer__running is True:
                    time.sleep(0.5)
                    retvalue = p.poll()
                    if retvalue is not None and retvalue != 0:
                        logger.error('touchserver run over, return value:%s' % str(retvalue))
                        break

            except Exception as e:
                logger.error('launch touchserver exception', exc_info=True)

            time.sleep(1)

    def __launch_inputserver(self):
        while self._Initializer__running is True:
            try:
                logger.info('inputserver run begin...')
                p = self._Initializer__adb.cmd('shell', '/data/local/tmp/wetest/inputserver')
                time.sleep(0.5)
                while self._Initializer__running is True:
                    time.sleep(0.5)
                    retvalue = p.poll()
                    if retvalue is not None and retvalue != 0:
                        logger.error('inputserver run over, return value:%s' % str(retvalue))
                        break

            except Exception as e:
                logger.error('launch inputserver exception', exc_info=True)

            time.sleep(1)

    def __launch_cloudscreen(self):
        while self._Initializer__running is True:
            try:
                logger.info('cloudscreen run begin...')
                p = self._Initializer__adb.cmd('shell', 'LD_LIBRARY_PATH=/data/local/tmp/wetest /data/local/tmp/wetest/cloudscreen')
                time.sleep(0.5)
                while self._Initializer__running is True:
                    time.sleep(0.5)
                    retvalue = p.poll()
                    if retvalue is not None and retvalue != 0:
                        logger.error('cloudscreen run over, return value:%s' % str(retvalue))
                        break

            except Exception as e:
                logger.error('launch cloudscreen exception', exc_info=True)

            time.sleep(1)

    def setup(self, touch_port, cloudscreen_port, install=False):
        self._Initializer__running = True
        if install:
            self._Initializer__adb.cmd_wait('shell', 'mkdir', '/data/local/tmp/wetest')
            self._Initializer__install_touch_server()
            self._Initializer__install_cloudscreen_server()
            self._Initializer__install_input_server()
            self._Initializer__adb.cmd_wait('shell', 'killall', 'touchserver')
            self._Initializer__adb.cmd_wait('shell', 'killall', 'cloudscreen')
            if self.sdk < 29:
                self._Initializer__touch_future = self._Initializer__thread_pool.submit(self._Initializer__launch_touchserver)
            else:
                self._Initializer__input_future = self._Initializer__thread_pool.submit(self._Initializer__launch_inputserver)
            self._Initializer__cloudscreen_future = self._Initializer__thread_pool.submit(self._Initializer__launch_cloudscreen)
        if self.sdk < 29:
            self.forward(touch_port, 25766)
        else:
            self.forward(touch_port, 15866)
        self.forward(cloudscreen_port, 15666)
        time.sleep(4)

    def quit(self):
        self._Initializer__running = False
        self._Initializer__adb.cmd_wait('shell', 'killall -s SIGKILL touchserver')
        self._Initializer__adb.cmd_wait('shell', 'killall -s SIGKILL cloudscreen')
        self._Initializer__adb.cmd_wait('shell', 'killall -s SIGKILL app_process')

    def wait(self):
        wait([self._Initializer__touch_future, self._Initializer__cloudscreen_future])