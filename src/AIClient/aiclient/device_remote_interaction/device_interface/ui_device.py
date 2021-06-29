# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/device_interface/ui_device.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 6023 bytes
import logging, os, sys, threading, time, traceback
__dir__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(__dir__)
LOG = logging.getLogger()
DEVICE_DRIVER_LOGGER = logging.getLogger('device_driver')
if '127.0.0.1' not in os.environ.get('no_proxy', ''):
    os.environ['no_proxy'] = '127.0.0.1,%s' % os.environ.get('no_proxy', '')
MSG_ID_UI_ACTION = 2001
MSG_ID_GAME_STATE = 2002
GAME_STATE_NONE = 0
GAME_STATE_UI = 1
GAME_STATE_START = 2
GAME_STATE_OVER = 3
GAME_STATE_MATCH_WIN = 4
MOBILE_QQ_PACKAGE_NAME = 'com.tencent.mobileqq'
MOBILE_QQ_PERMISSIONS = ['READ_SMS',
 'READ_CALENDAR',
 'ACCESS_FINE_LOCATION',
 'READ_EXTERNAL_STORAGE',
 'ACCESS_COARSE_LOCATION',
 'READ_PHONE_STATE',
 'SEND_SMS',
 'CALL_PHONE',
 'WRITE_CONTACTS',
 'CAMERA',
 'WRITE_CALENDAR',
 'GET_ACCOUNTS',
 'WRITE_EXTERNAL_STORAGE',
 'RECORD_AUDIO',
 'READ_CONTACTS']

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as (s):
        return s.connect_ex(('localhost', port)) == 0


def assign_ui_port():
    UIAUTOMATOR_PORT_DEFAULT = 19008
    PORT_MAX = 65535
    tmp_port = os.getpid() % (PORT_MAX - UIAUTOMATOR_PORT_DEFAULT) + UIAUTOMATOR_PORT_DEFAULT
    for i in range(tmp_port, PORT_MAX):
        if is_port_in_use(i):
            continue
        else:
            return str(tmp_port)


def screensnap_thread(report, stop, interval):
    LOG.info('time_snap Start')
    while 1:
        if stop.is_set():
            LOG.debug('end')
            return
            try:
                LOG.debug('auto screen shot')
                report.screenshot()
                stop.wait(interval)
            except:
                stack = traceback.format_exc()
                LOG.warning(stack)


class UIDevice:

    def __init__(self):
        self._UIDevice__device = None
        self._UIDevice__in_gaming = False
        self.report = None
        self.interval = 5
        self.snap_thread = None
        self.stop_snap_thread = threading.Event()

    def init(self, serial=None, use_wetest_screensnap=True):
        from .wpyscripts.common.adb_process import AdbTool
        adb = AdbTool()
        devices_num = len(adb.devices())
        if devices_num == 0:
            return (False, 'error: no devices/emulators found')
        if serial is not None and serial != '':
            os.environ['ANDROID_SERIAL'] = serial
        elif devices_num > 1:
            return (False, 'error: more than one device/emulator')
        in_wetest = os.environ.get('PLATFORM_IP')
        if not in_wetest:
            os.environ['UIAUTOMATOR_PORT'] = assign_ui_port()
        from .wpyscripts import manager
        self._UIDevice__device = manager.get_device()
        if use_wetest_screensnap and in_wetest:
            self.report = manager.get_reporter()
            self.snap_thread = threading.Thread(target=screensnap_thread, args=(
             self.report, self.stop_snap_thread, self.interval))
            self.snap_thread.setDaemon(True)
            self.snap_thread.start()
        self._reset_qq()
        return (True, '')

    def launch_app(self, package_name):
        return self._UIDevice__device.launch_app(package_name)

    def login_qq(self, msg_data=None, account=None, pwd=None):
        if not self._should_try_login(msg_data):
            DEVICE_DRIVER_LOGGER.info('no need try login_tencent')
            return True
        else:
            from .wpyscripts.uiautomator.login_tencent import login_tencent
            if account is not None and pwd is not None:
                DEVICE_DRIVER_LOGGER.info('try login_tencent[{}/{}]'.format(account, pwd))
                return login_tencent(account, pwd)
            account = os.getenv('QQNAME', None)
            pwd = os.getenv('QQPWD', None)
            if account is not None and pwd is not None:
                DEVICE_DRIVER_LOGGER.info('try login_tencent[{}/{}]'.format(account, pwd))
                return login_tencent(account, pwd)
            DEVICE_DRIVER_LOGGER.error('can not try login_tencent without account/pwd')
            return False

    def _reset_qq(self):
        self._UIDevice__device.clear_data(MOBILE_QQ_PACKAGE_NAME)
        for permission in MOBILE_QQ_PERMISSIONS:
            self._grant_permission(MOBILE_QQ_PACKAGE_NAME, permission)

    def _grant_permission(self, package_name, permission):
        cmd = 'shell pm grant {0} android.permission.{1}'.format(package_name, permission)
        return self._UIDevice__device.excute_adb(cmd)

    def _should_try_login(self, msg_data):
        if msg_data is not None:
            if msg_data['msg_id'] == MSG_ID_GAME_STATE and msg_data['game_state'] in [GAME_STATE_START,
             GAME_STATE_OVER,
             GAME_STATE_MATCH_WIN]:
                LOG.info('game_state != GAME_STATE_UI or GAME_STATE_NONE')
                return False
        else:
            LOG.info('msg_id != MSG_ID_GAME_STATE')
            return False
        from .wpyscripts.uiautomator.login_tencent import get_current_pkgname
        LOG.info('try to get_current_package')
        package_name = get_current_pkgname()
        LOG.info('get_current_package: {}'.format(package_name))
        if package_name == MOBILE_QQ_PACKAGE_NAME:
            return True
        else:
            return False


if __name__ == '__main__':
    ui_device = UIDevice()
    ret, errstr = ui_device.init()
    if ret:
        ui_device.launch_app(MOBILE_QQ_PACKAGE_NAME)
        time.sleep(10)
        ui_device.login_qq()
else:
    print(errstr)