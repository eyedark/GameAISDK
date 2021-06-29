# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/PlatformWeTest.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 17818 bytes
import os, time, logging, logging.config, json, cv2, numpy
from .Initializer import Initializer
from .devicePlatform.IPlatformProxy import *
from .TcpSocketHandler import TouchSocketHandler, InputSocketHandler, CloudscreenSocketHandler
from .common.AdbTool import AdbTool
from .pb.touch.TouchPkgPB_pb2 import *
from .pb.input.InputPkgPB_pb2 import *
from .pb.cloudscreen.CloudscreenPkgPB_pb2 import *
logger = logging.getLogger(__name__)

def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as (f):
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class PlatformWeTest(IPlatformProxy):

    def __init__(self, host='127.0.0.1', touch_port=Initializer.TOUCH_SEVER_PORT, cloudscreen_port=Initializer.CLOUD_SCREEN_PORT, force_orientation=False, quality=80, minInterval=40):
        super(PlatformWeTest, self).__init__()
        self._PlatformWeTest__deviceInfo = DeviceInfo()
        self._PlatformWeTest__touch_handler = None
        self._PlatformWeTest__host = host
        self._PlatformWeTest__touch_port = touch_port
        self._PlatformWeTest__cloudscreen_port = cloudscreen_port
        self._PlatformWeTest__cloudscreen_handler = None
        self._PlatformWeTest__seq = 0
        self._PlatformWeTest__game_width = 0
        self._PlatformWeTest__game_height = 0
        self._PlatformWeTest__regular_height = 0
        self._PlatformWeTest__scale = None
        self._PlatformWeTest__orientation = None
        self._PlatformWeTest__force_orientation = force_orientation
        self._PlatformWeTest__is_portrait = None
        self._PlatformWeTest__quality = quality
        self._PlatformWeTest__minInterval = minInterval
        self._PlatformWeTest__init_ok = False
        self._PlatformWeTest__sdk = None
        self._inject_event_func = None
        self._PlatformWeTest__initializer = None

    def touch_finish(self):
        pass

    def __get_seq(self):
        self._PlatformWeTest__seq = self._PlatformWeTest__seq + 1
        return self._PlatformWeTest__seq

    def init(self, serial=None, is_portrait=True, long_edge=None, timeout=60, **kwargs):
        standalone = kwargs['standalone'] if 'standalone' in kwargs else True
        __dir__ = os.path.dirname(os.path.abspath(__file__))
        self._PlatformWeTest__initializer = Initializer(resource_dir=os.path.join(__dir__, '..'), serial=serial)
        if not serial:
            serial = AdbTool().device_serial()
        if serial and serial.lower().find('wetest') != -1:
            standalone = False
        logger.info('standalone:%s' % standalone)
        self._PlatformWeTest__initializer.setup(self._PlatformWeTest__touch_port, self._PlatformWeTest__cloudscreen_port, install=standalone)
        self._PlatformWeTest__sdk = self._PlatformWeTest__initializer.sdk
        if self._PlatformWeTest__sdk < 29:
            self._PlatformWeTest__touch_handler = TouchSocketHandler(self._PlatformWeTest__host, self._PlatformWeTest__touch_port)
            self._PlatformWeTest__touch_handler.start()
            logger.info('touch thread started')
            self._inject_event_func = self._inject_touch_event
        else:
            self._PlatformWeTest__touch_handler = InputSocketHandler(self._PlatformWeTest__host, self._PlatformWeTest__touch_port)
            self._PlatformWeTest__touch_handler.start()
            logger.info('input thread started')
            self._inject_event_func = self._inject_input_event
        self._PlatformWeTest__cloudscreen_handler = CloudscreenSocketHandler(self._PlatformWeTest__host, self._PlatformWeTest__cloudscreen_port)
        self._PlatformWeTest__cloudscreen_handler.start()
        logger.info('cloudscreen thread started')
        ret, desc = self.get_device_info(timeout=timeout)
        if ret is None:
            logger.error('cannot get device info: {}'.format(desc))
            return (
             False, desc)
        self._PlatformWeTest__scale = long_edge * 1.0 / self._PlatformWeTest__deviceInfo.display_height
        self._PlatformWeTest__is_portrait = True
        if self._PlatformWeTest__is_portrait:
            self._PlatformWeTest__game_width = self._PlatformWeTest__deviceInfo.display_width * self._PlatformWeTest__scale
            self._PlatformWeTest__game_height = long_edge
        else:
            self._PlatformWeTest__game_width = long_edge
            self._PlatformWeTest__game_height = self._PlatformWeTest__deviceInfo.display_width * self._PlatformWeTest__scale
        self._PlatformWeTest__regular_height = long_edge
        logger.info('game_width={}, height={}'.format(self._PlatformWeTest__game_width, self._PlatformWeTest__game_height))
        self._PlatformWeTest__init_ok = True
        return (True, '')

    def deinit(self):
        logger.info('deinit enter')
        if self._PlatformWeTest__cloudscreen_handler:
            self._PlatformWeTest__cloudscreen_handler.quit()
            logger.info('stop cloudscreen_handler')
        if self._PlatformWeTest__touch_handler:
            self._PlatformWeTest__touch_handler.quit()
            logger.info('stop touch_handler')
        self._PlatformWeTest__initializer.quit()
        logger.info('deinit end')

    def get_rotation(self):
        return self._PlatformWeTest__orientation

    def get_device_info(self, timeout=60):
        if self._PlatformWeTest__init_ok:
            return (self._PlatformWeTest__deviceInfo, '')
        logger.info('get_device_info: timeout={}'.format(timeout))
        one_timeout = 3
        count = int(timeout / one_timeout)
        display_ret = None
        if count <= 0:
            count = 1
        for i in range(0, count):
            display_ret = self._PlatformWeTest__get_display_info(timeout=one_timeout)
            if display_ret:
                break

        if display_ret is None:
            return (None, 'get_device_info: get display info error')
        logger.info('get_device_info: display info={}'.format(display_ret))
        self._PlatformWeTest__deviceInfo.display_height = display_ret['dp_height']
        self._PlatformWeTest__deviceInfo.display_width = display_ret['dp_width']
        if self._PlatformWeTest__sdk < 29:
            touch_ret = None
            for i in range(0, count):
                touch_ret = self._PlatformWeTest__get_touch_info(timeout=one_timeout)
                count = count - 1
                if touch_ret:
                    break

            if touch_ret is None:
                return (None, 'get_device_info: get touch info error')
            logger.info('get_device_info: touch_info={}'.format(touch_ret))
            self._PlatformWeTest__deviceInfo.touch_height = touch_ret['touch_height']
            self._PlatformWeTest__deviceInfo.touch_width = touch_ret['touch_width']
            self._PlatformWeTest__deviceInfo.touch_slot_number = touch_ret['touch_slot_number']
        else:
            self._PlatformWeTest__deviceInfo.touch_height = self._PlatformWeTest__deviceInfo.display_height
            self._PlatformWeTest__deviceInfo.touch_width = self._PlatformWeTest__deviceInfo.display_width
            self._PlatformWeTest__deviceInfo.touch_slot_number = 10
        return (self._PlatformWeTest__deviceInfo, '')

    def get_image(self):
        err, res = self._PlatformWeTest__get_frame()
        if err != 0 or res is None:
            logger.info('get image error: {}, res:{}'.format(err, res))
            return (
             err, None)
        else:
            image = cv2.imdecode(numpy.frombuffer(res['datas'], dtype=numpy.uint8), cv2.IMREAD_COLOR)
            if self._PlatformWeTest__force_orientation:
                if self._PlatformWeTest__game_width > self._PlatformWeTest__game_height:
                    return (
                     0, cv2.flip(cv2.transpose(image), 0))
                else:
                    return (
                     0, image)
            else:
                if self._PlatformWeTest__orientation == SCREEN_ORIENTATION_0:
                    return (0, image)
                if self._PlatformWeTest__orientation == SCREEN_ORIENTATION_90:
                    return (0, cv2.flip(cv2.transpose(image), 0))
                if self._PlatformWeTest__orientation == SCREEN_ORIENTATION_180:
                    return (
                     0, cv2.flip(cv2.transpose(image), 0))
                if self._PlatformWeTest__orientation == SCREEN_ORIENTATION_270:
                    return (0, cv2.flip(cv2.transpose(image), 1))
            return (
             0, image)

    def touch_down(self, x, y, contact, pressure=50):
        self._inject_event_func(TOUCH_TOUCH_DOWN, x, y, contact, pressure)

    def touch_move(self, x, y, contact, pressure=50):
        self._inject_event_func(TOUCH_TOUCH_MOVE, x, y, contact, pressure)

    def touch_up(self, contact):
        self._inject_event_func(TOUCH_TOUCH_UP, pointer_id=contact)

    def touch_reset(self):
        self._inject_event_func(TOUCH_RESET, pressure=0)

    def touch_wait(self, milliseconds):
        self._inject_event_func(TOUCH_WAIT, wait_time=milliseconds)

    def _inject_touch_event(self, touch_type, x=0, y=0, pointer_id=0, pressure=0, wait_time=0):
        self._PlatformWeTest__inject_touch_event(touch_type, x=x, y=y, pointer_id=pointer_id, pressure=pressure, wait_time=wait_time)
        self._PlatformWeTest__inject_touch_event(TOUCH_COMMIT)

    def __inject_touch_event(self, touch_type, x=0, y=0, pointer_id=0, pressure=0, wait_time=0):
        pkg = TouchPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = int(time.time())
        pkg.header.command = TOUCH_EVENT_NOTIFY
        if touch_type is TOUCH_TOUCH_MOVE or TOUCH_TOUCH_DOWN:
            _x, _y = self._PlatformWeTest__trans_xy(x, y)
        else:
            _x, _y = x, y
        event = pkg.body.touchEventNotify.touchevents.add()
        event.touchType = touch_type
        event.slotId = pointer_id
        event.x = _x
        event.y = _y
        event.pressure = pressure
        event.waittime = wait_time * 1000
        self._PlatformWeTest__touch_handler.queue.put(pkg)

    def _inject_input_event(self, touch_type, x=0, y=0, pointer_id=0, pressure=0, wait_time=0):
        if touch_type > INPUT_TOUCH_MOVE:
            return
        pkg = InputPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = int(time.time())
        pkg.header.command = INPUT_TOUCH_EVENT_NOTIFY
        _x, _y = int(x / self._PlatformWeTest__scale), int(y / self._PlatformWeTest__scale)
        logger.info('{},{} -> {},{}'.format(x, y, _x, _y))
        pkg.body.inputTouchEventNotify.inputTouchType = touch_type
        pkg.body.inputTouchEventNotify.slotId = pointer_id
        pkg.body.inputTouchEventNotify.x = _x
        pkg.body.inputTouchEventNotify.y = _y
        self._PlatformWeTest__touch_handler.queue.put(pkg)

    def __get_touch_info(self, timeout=5, interval=1):
        pkg = TouchPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = 0
        pkg.header.command = TOUCH_DEVICE_INIT_REQ
        self._PlatformWeTest__touch_handler.queue.put(pkg)
        for i in range(0, int(timeout / interval)):
            err, packet = self._PlatformWeTest__touch_handler.get_last_packet()
            if err != 0 or packet is None:
                logger.error('get_touch_info: err={}, packet={}'.format(err, packet))
                time.sleep(interval)
                continue
                if packet.header.command == TOUCH_DEVICE_INIT_RES and packet.body.touchDeviceInitRes.result.errorcode == TOUCH_SUCC:
                    logger.info('touch device info: {}'.format(packet))
                    recv_info = packet.body.touchDeviceInitRes.touchDeviceInfo
                    return dict(touch_name=recv_info.devicename, touch_devpath=recv_info.devpath, touch_slot_number=recv_info.maxTrackingID, touch_width=recv_info.maxPostionX, touch_height=recv_info.maxPostionY, touch_hasBtnTouch=recv_info.hasBtnTouch)
                logger.info('error: get packet {}'.format(packet))
                time.sleep(interval)

        logger.error('error: get touch info timeout!')

    def __get_display_info(self, timeout=5, interval=1):
        pkg = CloudscreenPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = 0
        pkg.header.command = DISPLAY_DEVICE_INFO_REQ
        self._PlatformWeTest__cloudscreen_handler.queue.put(pkg)
        for i in range(0, int(timeout / interval)):
            err, packet = self._PlatformWeTest__cloudscreen_handler.get_last_packet()
            if err != 0 or packet is None:
                logger.error('get_display_info: err={}, packet={}'.format(err, packet))
                time.sleep(interval)
                continue
                if packet.header.command == DISPLAY_DEVICE_INFO_RES and packet.body.displayDeviceInfoRes.result.errorcode == CLOUDSCREEN_SUCC:
                    logger.info('display device info: {}'.format(packet))
                    recv_info = packet.body.displayDeviceInfoRes
                    return dict(dp_width=recv_info.width, dp_height=recv_info.height, dp_fps=recv_info.fps, dp_density=recv_info.density, dp_xdpi=recv_info.xdpi, dp_ydpi=recv_info.ydpi, dp_orientation=recv_info.orientation, dp_secure=recv_info.secure)
                logger.info('error: get packet {}'.format(packet))
                time.sleep(interval)

        logger.error('error: cannot get display info')

    def __get_frame(self):
        err, packet = self._PlatformWeTest__cloudscreen_handler.get_last_packet()
        if err != 0:
            return (err, None)
        if self._PlatformWeTest__cloudscreen_handler.has_error:
            logger.info('the socket is connected, start push mode')
            self._PlatformWeTest__start_capture_screen_push_mode(height=self._PlatformWeTest__regular_height, quality=self._PlatformWeTest__quality, minInterval=self._PlatformWeTest__minInterval, landscape=False, alignment=False)
            self._PlatformWeTest__cloudscreen_handler.has_error = False
        if packet is None:
            return (0, None)
        if packet.header.command == SCREEN_CAPTURE_FRAME_NOTIFY and packet.body.screenCaptureFrameNotify.result.errorcode == CLOUDSCREEN_SUCC:
            recv_info = packet.body.screenCaptureFrameNotify
            self._PlatformWeTest__orientation = int(recv_info.orientation)
            return (
             0,
             dict(result=recv_info.result, index=recv_info.index, width=recv_info.width, height=recv_info.height, orientation=recv_info.orientation, len=recv_info.len, datas=recv_info.datas))
        return (
         packet.body.screenCaptureRes.result.errorcode, None)

    def __start_capture_screen_push_mode(self, **kwargs):
        pkg = CloudscreenPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = 0
        pkg.header.command = SCREEN_CAPTURE_PUSH_MODE_REQ
        pkg.body.screenCapturePushModeReq.height = int(kwargs['height']) if 'height' in kwargs else 0
        pkg.body.screenCapturePushModeReq.quality = kwargs['quality'] if 'quality' in kwargs else 0
        pkg.body.screenCapturePushModeReq.minInterval = kwargs['minInterval'] if 'minInterval' in kwargs else 50
        pkg.body.screenCapturePushModeReq.landscape = kwargs['landscape'] if 'landscape' in kwargs else False
        pkg.body.screenCapturePushModeReq.alignment = kwargs['alignment'] if 'alignment' in kwargs else False
        self._PlatformWeTest__cloudscreen_handler.queue.put(pkg)

    def __stop_capture_screen_push_mode(self):
        pkg = CloudscreenPkg()
        pkg.header.sequenceId = self._PlatformWeTest__get_seq()
        pkg.header.timestamp = 0
        pkg.header.command = SCREEN_CAPTURE_PUSH_STOP_REQ
        self._PlatformWeTest__cloudscreen_handler.queue.put(pkg)

    def __trans_xy(self, x, y):
        if self._PlatformWeTest__force_orientation:
            if self._PlatformWeTest__game_width > self._PlatformWeTest__game_height:
                nx, ny = self._PlatformWeTest__game_height - y, x
            else:
                nx, ny = x, y
        else:
            if self._PlatformWeTest__orientation != SCREEN_ORIENTATION_UNKNOW:
                orientation = self._PlatformWeTest__orientation
            else:
                orientation = SCREEN_ORIENTATION_90 if self._PlatformWeTest__game_height < self._PlatformWeTest__game_width else SCREEN_ORIENTATION_0
            if orientation == SCREEN_ORIENTATION_0:
                nx, ny = x, y
            else:
                if orientation == SCREEN_ORIENTATION_90:
                    nx, ny = self._PlatformWeTest__game_width - y, x
                else:
                    if orientation == SCREEN_ORIENTATION_180:
                        nx, ny = self._PlatformWeTest__game_width - x, self._PlatformWeTest__game_height - y
                    else:
                        if orientation == SCREEN_ORIENTATION_270:
                            nx, ny = y, self._PlatformWeTest__game_height - x
                        else:
                            nx, ny = x, y
            if not self._PlatformWeTest__is_portrait:
                _touch_scale_x = nx * 1.0 / self._PlatformWeTest__game_height
                _touch_scale_y = ny * 1.0 / self._PlatformWeTest__game_width
            else:
                _touch_scale_x = nx * 1.0 / self._PlatformWeTest__game_width
                _touch_scale_y = ny * 1.0 / self._PlatformWeTest__game_height
        _x = int(self._PlatformWeTest__deviceInfo.touch_width * _touch_scale_x)
        _y = int(self._PlatformWeTest__deviceInfo.touch_height * _touch_scale_y)
        logger.info('{},{} -> {},{}'.format(x, y, _x, _y))
        return (_x, _y)