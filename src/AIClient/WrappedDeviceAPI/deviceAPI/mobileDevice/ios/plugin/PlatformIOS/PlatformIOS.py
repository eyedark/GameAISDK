# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/ios/plugin/PlatformIOS/PlatformIOS.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 8031 bytes
import cv2, numpy, io, sys
from .Wda import wda
from ...APIDefineIOS import *
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, 'wda'))
PP_RET_OK = 0
PP_RET_ERR = -1

class PlatformIOS(object):

    def __init__(self):
        self._PlatformIOS__device = None
        self._PlatformIOS__game_width = 0
        self._PlatformIOS__game_height = 0
        self._PlatformIOS__device_width = 0
        self._PlatformIOS__device_height = 0
        self._PlatformIOS__UIKit_width = 0
        self._PlatformIOS__UIKit_height = 0
        self._PlatformIOS__scale = 0.0
        self._PlatformIOS__display_scale = None
        self._PlatformIOS__logger = None
        self._PlatformIOS__c = wda.Client('http://localhost:8100')
        self._PlatformIOS__s = None

    def init(self, serial=None, is_portrait=False, long_edge=1280):
        if serial is None:
            self._PlatformIOS__logger = logging.getLogger(LOG_DEFAULT)
        else:
            self._PlatformIOS__logger = logging.getLogger(serial)
        self._PlatformIOS__s = self._PlatformIOS__c.session()
        status = self._PlatformIOS__c.status()
        if status is None:
            return (False, 'init wda failed')
        self._PlatformIOS__UIKit_width = self._PlatformIOS__s.window_size().width
        self._PlatformIOS__UIKit_height = self._PlatformIOS__s.window_size().height
        raw_data = self._PlatformIOS__c.fast_screenshot_post(1.0, 0.1)
        from PIL import Image
        buff = io.BytesIO(raw_data)
        image = Image.open(buff)
        v = max(image.size) / max(self._PlatformIOS__UIKit_width, self._PlatformIOS__UIKit_height)
        self._PlatformIOS__display_scale = round(v)
        print('display scale: %d' % self._PlatformIOS__display_scale)
        self._PlatformIOS__device_width = self._PlatformIOS__UIKit_width * self._PlatformIOS__display_scale
        self._PlatformIOS__device_height = self._PlatformIOS__UIKit_height * self._PlatformIOS__display_scale
        if is_portrait:
            self._PlatformIOS__scale = long_edge * 1.0 / self._PlatformIOS__device_height
            self._PlatformIOS__game_width = int(self._PlatformIOS__device_width * self._PlatformIOS__scale)
            self._PlatformIOS__game_height = long_edge
        else:
            self._PlatformIOS__scale = long_edge * 1.0 / self._PlatformIOS__device_width
            self._PlatformIOS__game_width = long_edge
            self._PlatformIOS__game_height = int(self._PlatformIOS__device_height * self._PlatformIOS__scale)
        self._PlatformIOS__logger.info('game_width={}, height={}'.format(self._PlatformIOS__game_width, self._PlatformIOS__game_height))
        return (True, str())

    def get_display_scale(self):
        return self._PlatformIOS__display_scale

    def deinit(self):
        self._PlatformIOS__logger.info('deinit')
        return True

    def touch_up(self, contact=0):
        self._PlatformIOS__logger.info('touch up')

    def touch_down(self, px, py, contact=0, pressure=50):
        self._PlatformIOS__logger.info('touch down')

    def touch_move(self, px, py, contact=0, pressure=50):
        self._PlatformIOS__logger.info('touch move')

    def touch_wait(self, milliseconds):
        self._PlatformIOS__logger.info('touch wait')

    def touch_reset(self):
        self._PlatformIOS__logger.info('touch reset')

    def touch_finish(self):
        self._PlatformIOS__logger.info('touch finish')

    def get_device_info(self):
        return self._PlatformIOS__s.device_info()

    def install_app(self, apk_path):
        self._PlatformIOS__logger.info('install app')

    def launch_app(self, package_name, activity_name):
        self._PlatformIOS__logger.info('launch app')

    def exit_app(self, package_name):
        self._PlatformIOS__logger.info('exit app')

    def current_app(self):
        return self._PlatformIOS__s.app_current()

    def clear_app_data(self, app_package_name):
        self._PlatformIOS__logger.info('clear app data')

    def key(self, key):
        self._PlatformIOS__logger.info('key')

    def sleep(self):
        return self._PlatformIOS__s.lock()

    def wake(self):
        self._PlatformIOS__s.unlock()
        self._PlatformIOS__c.home()

    def click(self, px, py):
        """
        x, y can be float(percent) or int
        """
        x, y = self._PlatformIOS__game2UIKit(px, py)
        return self._PlatformIOS__s.click(x, y)

    def swipe(self, sx, sy, ex, ey, duration_ms=50):
        """
        Args:
            x1, y1, x2, y2 (int, float): float(percent), int(coordicate)
            duration (float): start coordinate press duration (seconds)

        [[FBRoute POST:@"/wda/dragfromtoforduration"] respondWithTarget:self action:@selector(handleDragCoordinate:)],
        :param duration: (float)start coordinate press duration (seconds)
        """
        duration = 0
        x1, y1 = self._PlatformIOS__game2UIKit(sx, sy)
        x2, y2 = self._PlatformIOS__game2UIKit(ex, ey)
        return self._PlatformIOS__s.swipe(x1, y1, x2, y2, duration)

    def swipe_hold(self, sx, sy, ex, ey, duration_ms=1000):
        x1, y1 = self._PlatformIOS__game2UIKit(sx, sy)
        x2, y2 = self._PlatformIOS__game2UIKit(ex, ey)
        dx = x2 - x1
        dy = y2 - y1
        return self._PlatformIOS__s.swipe_hold(x1, y1, dx, dy, duration_ms)

    def long_tap(self, px, py, duration_ms):
        """
        Tap and hold for a moment

        Args:
            - x, y(int, float): float(percent) or int(absolute coordicate)
            - duration_ms(float): seconds of hold time

        [[FBRoute POST:@"/wda/touchAndHold"] respondWithTarget:self action:@selector(handleTouchAndHoldCoordinate:)],
        """
        duration = duration_ms * 1.0 / 1000
        x, y = self._PlatformIOS__game2UIKit(px, py)
        return self._PlatformIOS__s.tap_hold(x, y, duration)

    def get_image(self, quality=0.6):
        raw = self._PlatformIOS__c.fast_screenshot_post(self._PlatformIOS__scale, quality)
        image = cv2.imdecode(numpy.frombuffer(raw, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        return (
         PP_RET_OK, image)

    def vm_size(self):
        return (
         self._PlatformIOS__device_width, self._PlatformIOS__device_height)

    def get_rotation(self):
        self._PlatformIOS__logger.info('get rotation')

    def orientation(self):
        """
        Return string
        One of <PORTRAIT | LANDSCAPE>
        """
        return self._PlatformIOS__s.orientation()

    def window_size(self):
        """
        Returns:
            namedtuple: eg
                Size(width=320, height=568)
        """
        return self._PlatformIOS__s.window_size()

    def deactivate(self, duration):
        """Put app into background and than put it back
        Args:
            - duration (float): deactivate time, seconds
        """
        return self._PlatformIOS__s.deactivate(duration)

    def app_state(self, bundle_id):
        """
        Returns example:
            {
                "value": 4,
                "sessionId": "0363BDC5-4335-47ED-A54E-F7CCB65C6A65"
            }

        value 1(not running) 2(running in background) 3(running in foreground)
        """
        return self._PlatformIOS__s.app_state(bundle_id)

    def app_launch(self, bundle_id, argument=[], environment={}, wait_for_quiescence=False):
        """
        Args:
            - bundle_id (str): the app bundle id
            - arguments (list): ['-u', 'https://www.google.com/ncr']
            - enviroment (dict): {"KEY": "VAL"}
            - wait_for_quiescence (bool): default False
        """
        return self._PlatformIOS__s.app_launch(bundle_id, argument, environment, wait_for_quiescence)

    def keyboard_dismiss(self):
        """
        Not working for now
        """
        return self._PlatformIOS__s.keyboard_dismiss()

    def home(self):
        """Press home button"""
        return self._PlatformIOS__c.home()

    def __game2UIKit(self, px, py):
        """
        将下发的坐标点转换成ios设备特有的UIKit坐标
        :param px:x方向的坐标
        :param py:y方向的坐标
        :return(int):UIKit的坐标值
        """
        rateX = px * 1.0 / self._PlatformIOS__game_width
        rateY = py * 1.0 / self._PlatformIOS__game_height
        UIKitX = rateX * self._PlatformIOS__UIKit_width
        UIKitY = rateY * self._PlatformIOS__UIKit_height
        return (
         round(UIKitX), round(UIKitY))

    def __phy2rate(self, px, py):
        """
        将下发的坐标点转换成坐标比例
        :param px:x方向的坐标
        :param py:y方向的坐标
        :return(float):实际坐标对应的比例坐标值
        """
        rx = px * 1.0 / self._PlatformIOS__game_width
        ry = py * 1.0 / self._PlatformIOS__game_height
        return (
         rx, ry)