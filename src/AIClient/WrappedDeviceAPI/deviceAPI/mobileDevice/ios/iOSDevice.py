# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/ios/iOSDevice.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 18335 bytes
import sys, cv2, traceback, logging.config
from .iOSDeviceAPI import IOSDeviceAPI
from ...iDevice import IDevice
from .APIDefineIOS import *
PP_RET_OK = 0
PP_RET_ERR = -1
PP_RET_ERR_SOCKET_EXCEPTION = -2
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)

class IOSDevice(IDevice):

    def __init__(self, platform):
        IDevice.__init__(self, platform)
        self._IOSDevice__deviceApi = IOSDeviceAPI(platform)
        self._IOSDevice__height = -1
        self._IOSDevice__width = -1
        self._IOSDevice__serial = '*'
        self._IOSDevice__pid = os.getpid()
        self._IOSDevice__showScreen = False
        self._IOSDevice__maxContact = 0

    def initialize(self, log_dir, level=LOG_DEBUG, long_edge=1280, device_serial=None, is_portrait=False, show_raw_screen=False):
        """
        :param device_serial: str, 手机序列号,默认为None，当接入一个设备时可不指定序列号，当接入多个设备时需要指定
        :param is_portrait: bool, 手机为横屏还是竖屏，True为竖屏，False为横屏
        :param long_edge: int, 长边的长度
        :param log_dir: str, 日志存放目录
        :param level: enum, 指定日志级别，取值为[LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_CRITICAL]，默认为LOG_DEBUG
        :param show_raw_screen: bool, 是否显示手机图片
        :param kwargs: dict, 一些组件需要的参数，可以自己定义，例如端口号等等
        """
        try:
            if device_serial is not None:
                log_dir = log_dir + '/' + device_serial + '/'
                self._IOSDevice__serial = device_serial
                if not self._LogInit(log_dir, level, device_serial):
                    raise RuntimeError('init log failed')
            else:
                log_dir = log_dir + '/' + LOG_DEFAULT + '/'
                if not self._LogInit(log_dir, level, LOG_DEFAULT):
                    raise RuntimeError('init log failed')
                if not self._IOSDevice__deviceApi.Initialize(device_serial, is_portrait, long_edge):
                    self._IOSDevice__logger.error('DeviceAPI initial failed')
                    raise RuntimeError('DeviceAPI initial failed')
                self._IOSDevice__showScreen = show_raw_screen
                self._IOSDevice__maxContact = self._IOSDevice__deviceApi.GetMaxContact()
                self._IOSDevice__height, self._IOSDevice__width, strError = self._IOSDevice__deviceApi.GetScreenResolution()
                if self._IOSDevice__height == -1 and self._IOSDevice__width == -1:
                    self._IOSDevice__logger.error(strError)
                    raise RuntimeError(strError)
                if is_portrait:
                    height = long_edge
                    width = round(self._IOSDevice__width * height / self._IOSDevice__height)
                else:
                    width = long_edge
                    height = round(self._IOSDevice__height * width / self._IOSDevice__width)
            exec('self.__width = width')
            exec('self.__height = height')
            self._IOSDevice__logger.info('init successful')
            return True
        except Exception as e:
            self._IOSDevice__logger.error(e)
            traceback.print_exc()
            raise e

    def deInitialize(self):
        return self._IOSDevice__deviceApi.DeviceInfo()

    def getScreen(self):
        """
        :return: Mat类型的图像/None
        """
        try:
            self._CheckException()
            err, image = self._IOSDevice__deviceApi.GetFrame()
            self._IOSDevice__logger.info('get image')
            if err != PP_RET_OK:
                raise Exception('get image error')
            if image is not None and self._IOSDevice__showScreen:
                self._IOSDevice__logger.info('get image')
                cv2.imshow('pid:' + str(self._IOSDevice__pid) + ' serial:' + str(self._IOSDevice__serial), image)
                cv2.waitKey(1)
            return image
        except Exception as e:
            self._IOSDevice__logger.error('get image error [{}]'.format(e))
            self._IOSDevice__logger.error(traceback.format_exc())
            raise e

    def doAction(self, **kwargs):
        aType = kwargs['aType']
        if aType in TOUCH_CMD_LIST:
            return self.TouchCMD(**kwargs)
        if aType in DEVICE_CMD_LIST:
            return self.DeviceCMD(**kwargs)
        raise Exception('unknown action type: {}, {}'.format(aType, kwargs))

    def TouchCMD(self, **kwargs):
        try:
            self._CheckException()
            for key in kwargs.keys():
                if key not in TOUCH_KEY:
                    self._IOSDevice__logger.error('wrong key of kwargs: {0}'.format(key))
                    return False

            neededFlag, actionType = self._GetValuesInkwargs('aType', True, None, kwargs)
            if not neededFlag:
                self._IOSDevice__logger.error('aType is needed when exec TouchCommand')
                return False
            else:
                if actionType == TOUCH_CLICK:
                    neededFlag, px = self._GetValuesInkwargs('sx', True, None, kwargs)
                    if not self._CheckVar(neededFlag, 'sx', actionType, px, int, 'var >= 0 and var < self.__width'):
                        return False
                    neededFlag, py = self._GetValuesInkwargs('sy', True, None, kwargs)
                    if not self._CheckVar(neededFlag, 'sy', actionType, py, int, 'var >= 0 and var < self.__height'):
                        return False
                    neededFlag, contact = self._GetValuesInkwargs('contact', False, 0, kwargs)
                    neededFlag, durationMS = self._GetValuesInkwargs('durationMS', False, -1, kwargs)
                    if not self._CheckVar(neededFlag, 'durationMS', actionType, durationMS, int, 'var >= -1'):
                        return False
                    neededFlag, wait_time = self._GetValuesInkwargs('wait_time', False, 0, kwargs)
                    if not neededFlag or not (isinstance(wait_time, int) or isinstance(wait_time, float)) or wait_time < 0:
                        self._IOSDevice__logger.error('wrong wait_time when exec click, wait_time:{0}'.format(wait_time))
                        return False
                    self._IOSDevice__logger.info('platform click, x: {0}, y {1}, contact: {2}, durationMS: {3}, waitTime: {4}'.format(px, py, contact, durationMS, wait_time))
                    self._IOSDevice__deviceApi.Click(px, py, durationMS, wait_time)
                else:
                    if actionType == TOUCH_SWIPE:
                        neededFlag, sx = self._GetValuesInkwargs('sx', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'sx', actionType, sx, int, 'var >= 0 and var < self.__width'):
                            return False
                        neededFlag, sy = self._GetValuesInkwargs('sy', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'sy', actionType, sy, int, 'var >= 0 and var < self.__height'):
                            return False
                        neededFlag, ex = self._GetValuesInkwargs('ex', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'ex', actionType, ex, int, 'var >= 0 and var < self.__width'):
                            return False
                        neededFlag, ey = self._GetValuesInkwargs('ey', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'ey', actionType, ey, int, 'var >= 0 and var < self.__height'):
                            return False
                        neededFlag, contact = self._GetValuesInkwargs('contact', False, 0, kwargs)
                        neededFlag, durationMS = self._GetValuesInkwargs('durationMS', False, 50, kwargs)
                        if not self._CheckVar(neededFlag, 'durationMS', actionType, durationMS, int, 'var >= 0'):
                            return False
                        neededFlag, needUp = self._GetValuesInkwargs('needUp', False, True, kwargs)
                        if not self._CheckVar(neededFlag, 'needUp', actionType, needUp, bool, 'True'):
                            return False
                        neededFlag, wait_time = self._GetValuesInkwargs('wait_time', False, 0, kwargs)
                        if not neededFlag or not (isinstance(wait_time, int) or isinstance(wait_time, float)) or wait_time < 0:
                            self._IOSDevice__logger.error('wrong wait_time when exec swipe, wait_time:{0}'.format(wait_time))
                            return False
                        self._IOSDevice__logger.info('platform swipe, sx: {0}, sy {1}, ex: {2}, ey {3}, needUp: {4}, durationMS: {5}'.format(sx, sy, ex, ey, needUp, durationMS))
                        self._IOSDevice__deviceApi.Swipe(sx, sy, ex, ey, contact, durationMS, needUp, wait_time)
                    else:
                        if actionType == TOUCH_RESET:
                            neededFlag, wait_time = self._GetValuesInkwargs('wait_time', False, 0, kwargs)
                            if not neededFlag or not (isinstance(wait_time, int) or isinstance(wait_time, float)) or wait_time < 0:
                                self._IOSDevice__logger.error('wrong wait_time when exec reset, wait_time:{0}'.format(wait_time))
                                return False
                            self._IOSDevice__logger.info('platform reset, waitTime: {0}'.format(wait_time))
                            self._IOSDevice__deviceApi.Reset(wait_time=wait_time)
                        else:
                            self._IOSDevice__logger.error('Wrong aType when TouchCommand, aType:{0}'.format(actionType))
                            return False
                return True
        except Exception as e:
            self._IOSDevice__logger.error(e)
            traceback.print_exc()
            return False

    def DeviceCMD(self, **kwargs):
        try:
            self._CheckException()
            neededFlag, actionType = self._GetValuesInkwargs('aType', True, None, kwargs)
            if not neededFlag:
                self._IOSDevice__logger.error('aType is needed when exec DeviceCommand')
                return False
            else:
                if actionType == DEVICE_INSTALL:
                    neededFlag, APKPath = self._GetValuesInkwargs('APKPath', True, None, kwargs)
                    if not self._CheckVar(neededFlag, 'APKPath', actionType, APKPath, str, 'True'):
                        return False
                    if not self._IOSDevice__deviceApi.InstallAPP(APKPath):
                        self._IOSDevice__logger.error('install app failed: {0}'.format(APKPath))
                        return False
                else:
                    if actionType == DEVICE_START:
                        neededFlag, PKGName = self._GetValuesInkwargs('PKGName', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'PKGName', actionType, PKGName, str, 'True'):
                            return False
                        neededFlag, ActivName = self._GetValuesInkwargs('ActivityName', True, None, kwargs)
                        if not self._CheckVar(neededFlag, 'ActivityName', actionType, ActivName, str, 'True'):
                            return False
                        self._IOSDevice__deviceApi.LaunchAPP(PKGName, ActivName)
                    else:
                        if actionType == DEVICE_EXIT:
                            neededFlag, PKGName = self._GetValuesInkwargs('PKGName', True, None, kwargs)
                            if not self._CheckVar(neededFlag, 'PKGName', actionType, PKGName, str, 'True'):
                                return False
                            self._IOSDevice__deviceApi.ExitAPP(PKGName)
                        else:
                            if actionType == DEVICE_CURAPP:
                                return self._IOSDevice__deviceApi.current_app()
                            if actionType == DEVICE_KEY:
                                neededFlag, key = self._GetValuesInkwargs('key', True, None, kwargs)
                                if not self._CheckVar(neededFlag, 'key', actionType, key, str, 'True'):
                                    return False
                                self._IOSDevice__deviceApi.Key(key)
                            else:
                                if actionType == DEVICE_TEXT:
                                    neededFlag, text = self._GetValuesInkwargs('text', True, None, kwargs)
                                    if not self._CheckVar(neededFlag, 'text', actionType, text, str, 'True'):
                                        return False
                                    self._IOSDevice__deviceApi.Text(text)
                                else:
                                    if actionType == DEVICE_SLEEP:
                                        self._IOSDevice__deviceApi.Sleep()
                                    else:
                                        if actionType == DEVICE_WAKE:
                                            self._IOSDevice__deviceApi.Wake()
                                        else:
                                            if actionType == DEVICE_WMSIZE:
                                                return self._IOSDevice__deviceApi.WMSize()
                                            else:
                                                if actionType == DEVICE_MAXCONTACT:
                                                    return self._IOSDevice__maxContact
                                                self._IOSDevice__logger.error('wrong aType when exec DeviceCommand, aType:{0}'.format(actionType))
                                                return False
                return True
        except Exception as e:
            self._IOSDevice__logger.error(e)
            traceback.print_exc()
            return False

    def _LogInit(self, log_dir, level, device_serial):
        try:
            if not isinstance(log_dir, str):
                logging.ERROR('wrong log_dir when init LOG, log_dir:{0}'.format(log_dir))
                return False
            else:
                if level not in LOG_LIST:
                    logging.WARNING('wrong level when init LOG, level:{0}, use default level: DEBUG'.format(level))
                    level = LOG_DEBUG
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                self._IOSDevice__logger = logging.getLogger(device_serial)
                if not self._IOSDevice__logger.handlers:
                    console = logging.StreamHandler()
                    formatter = logging.Formatter(LOG_FORMAT)
                    console.setFormatter(formatter)
                    fileHandler = RotatingFileHandler(filename=os.path.join(log_dir, 'DeviceAPI.log'), maxBytes=2048000, backupCount=10)
                    fileHandler.setFormatter(formatter)
                    self._IOSDevice__logger.addHandler(fileHandler)
                    self._IOSDevice__logger.addHandler(console)
                    self._IOSDevice__logger.setLevel(level)
                loggerWeTest = logging.getLogger('PlatformWeTest')
                if not loggerWeTest.handlers:
                    fileHandler = RotatingFileHandler(filename=os.path.join(log_dir, 'PlatformWeTest.log'), maxBytes=2048000, backupCount=10)
                    fileHandler.setFormatter(formatter)
                    loggerWeTest.addHandler(fileHandler)
                    loggerWeTest.setLevel(level)
                return True
        except Exception as e:
            logging.error(e)
            return False

    def _CheckException(self):
        if exceptionQueue.empty() is False:
            errorStr = exceptionQueue.get()
            while exceptionQueue.empty() is False:
                errorStr = exceptionQueue.get()

            raise Exception(errorStr)

    def _GetandCheck(self, varname, needed, default, kwargs, actionType, type, describ):
        try:
            neededFlag, var = self._GetValuesInkwargs(varname, needed, default, kwargs)
            if not self._CheckVar(neededFlag, varname, actionType, var, type, describ):
                return False
            else:
                return var
        except Exception as e:
            self._IOSDevice__logger.error(e)
            return False

    def _GetValuesInkwargs(self, key, isNessesary, defaultValue, kwargs):
        try:
            if not isNessesary:
                if key not in kwargs:
                    return (True, defaultValue)
                else:
                    return (
                     True, kwargs[key])
            else:
                return (
                 True, kwargs[key])
        except Exception as e:
            self._IOSDevice__logger.error(e)
            return False

    def _CheckVar(self, needFlag, varname, aType, var, typed, execd):
        try:
            if not needFlag:
                self._IOSDevice__logger.error('can not find {0}'.format(varname))
                return False
            else:
                if not isinstance(var, typed):
                    self._IOSDevice__logger.error('wrong type of {0}: {1}, {2} is needed'.format(varname, type(var), typed))
                    return False
                if not eval(execd):
                    self._IOSDevice__logger.error('wrong value of {0}: {1}'.format(varname, var))
                    return False
                return True
        except Exception as e:
            self._IOSDevice__logger.error(e)
            return False


if __name__ == '__main__':
    device_serial = None
    is_portrait = False
    long_edge = 1280
    log_dir = './logs'
    log_level = LOG_DEBUG
    showScreen = True
    test_ios_api = IOSDevice()
    test_ios_api.initialize(log_dir, log_level, device_serial, is_portrait, long_edge, showScreen)
    image = test_ios_api.getScreen()
    ret = test_ios_api.TouchWDA(aType=TOUCH_CLICK, sx=1080, sy=430, contact=0, durationMS=-1, wait_time=0)
    ret = test_ios_api.TouchWDA(aType=TOUCH_SWIPE, sx=250, sy=430, ex=250, ey=350, contact=0, durationMS=0, needUp=True, wait_time=0)