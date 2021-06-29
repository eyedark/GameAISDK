# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/device_interface/libs/uiauto/uiautomator.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 52158 bytes
"""Python wrapper for Android uiautomator tool."""
import sys, os, subprocess, time, itertools, json, hashlib, socket, re, collections, xml.dom.minidom, logging, libs.imap_utf7 as imap_utf7, six
logger = logging.getLogger(__name__)
DEVICE_PORT = int(os.environ.get('UIAUTOMATOR_DEVICE_PORT', '9008'))
LOCAL_PORT = int(os.environ.get('UIAUTOMATOR_LOCAL_PORT', '9008'))
if 'localhost' not in os.environ.get('no_proxy', ''):
    os.environ['no_proxy'] = 'localhost,%s' % os.environ.get('no_proxy', '')
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

try:
    from httplib import HTTPException
except:
    from http.client import HTTPException

try:
    if os.name == 'nt':
        import urllib3
except:
    pass

__author__ = 'Xiaocong He'
__all__ = ['device', 'Device', 'rect', 'point', 'Selector', 'JsonRPCError']

def U(x):
    if sys.version_info.major == 2:
        if type(x) is str:
            return x.decode('utf-8')
        return x
    if sys.version_info.major == 3:
        return x


def param_to_property(*props, **kwprops):
    if props and kwprops:
        raise SyntaxError('Can not set both props and kwprops at the same time.')

    class Wrapper(object):

        def __init__(self, func):
            self.func = func
            self.kwargs, self.args = {}, []

        def __getattr__(self, attr):
            if kwprops:
                for prop_name, prop_values in kwprops.items():
                    if attr in prop_values and prop_name not in self.kwargs:
                        self.kwargs[prop_name] = attr
                        return self

            elif attr in props:
                self.args.append(attr)
                return self
            raise AttributeError('%s parameter is duplicated or not allowed!' % attr)

        def __call__(self, *args, **kwargs):
            if kwprops:
                kwargs.update(self.kwargs)
                self.kwargs = {}
                return self.func(*args, **kwargs)
            else:
                new_args, self.args = self.args + list(args), []
                return self.func(*new_args, **kwargs)

    return Wrapper


class JsonRPCError(Exception):

    def __init__(self, code, message):
        self.code = int(code)
        self.message = message

    def __str__(self):
        return 'JsonRPC Error code: %d, Message: %s' % (self.code, self.message)


class JsonRPCMethod(object):
    if os.name == 'nt':
        try:
            pool = urllib3.PoolManager()
        except:
            pass

    def __init__(self, url, method, timeout=30):
        self.url, self.method, self.timeout = url, method, timeout

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise SyntaxError('Could not accept both *args and **kwargs as JSONRPC parameters.')
        data = {'jsonrpc': '2.0', 'method': self.method, 'id': self.id()}
        if args:
            data['params'] = args
        else:
            if kwargs:
                data['params'] = kwargs
            jsonresult = {'result': ''}
            if os.name == 'nt':
                res = self.pool.urlopen('POST', self.url, headers={'Content-Type': 'application/json'}, body=json.dumps(data).encode('utf-8'), timeout=self.timeout)
                jsonresult = json.loads(res.data.decode('utf-8'))
            else:
                result = None
                try:
                    req = urllib2.Request(self.url, json.dumps(data).encode('utf-8'), {'Content-type': 'application/json'})
                    result = urllib2.urlopen(req, timeout=self.timeout)
                    jsonresult = json.loads(result.read().decode('utf-8'))
                finally:
                    if result is not None:
                        result.close()

        if 'error' in jsonresult and jsonresult['error']:
            raise JsonRPCError(jsonresult['error']['code'], '%s: %s' % (jsonresult['error']['data']['exceptionTypeName'], jsonresult['error']['message']))
        return jsonresult['result']

    def id(self):
        m = hashlib.md5()
        m.update(('%s at %f' % (self.method, time.time())).encode('utf-8'))
        return m.hexdigest()


class JsonRPCClient(object):

    def __init__(self, url, timeout=30, method_class=JsonRPCMethod):
        self.url = url
        self.timeout = timeout
        self.method_class = method_class

    def __getattr__(self, method):
        return self.method_class(self.url, method, timeout=self.timeout)


class Selector(dict):
    __doc__ = 'The class is to build parameters for UiSelector passed to Android device.\n    '
    _Selector__fields = {'text': (1, None), 
     'textContains': (2, None), 
     'textMatches': (4, None), 
     'textStartsWith': (8, None), 
     'className': (16, None), 
     'classNameMatches': (32, None), 
     'description': (64, None), 
     'descriptionContains': (128, None), 
     'descriptionMatches': (256, None), 
     'descriptionStartsWith': (512, None), 
     'checkable': (1024, False), 
     'checked': (2048, False), 
     'clickable': (4096, False), 
     'longClickable': (8192, False), 
     'scrollable': (16384, False), 
     'enabled': (32768, False), 
     'focusable': (65536, False), 
     'focused': (131072, False), 
     'selected': (262144, False), 
     'packageName': (524288, None), 
     'packageNameMatches': (1048576, None), 
     'resourceId': (2097152, None), 
     'resourceIdMatches': (4194304, None), 
     'index': (8388608, 0), 
     'instance': (16777216, 0)}
    _Selector__mask, _Selector__childOrSibling, _Selector__childOrSiblingSelector = ('mask',
                                                                                     'childOrSibling',
                                                                                     'childOrSiblingSelector')

    def __init__(self, **kwargs):
        super(Selector, self).__setitem__(self._Selector__mask, 0)
        super(Selector, self).__setitem__(self._Selector__childOrSibling, [])
        super(Selector, self).__setitem__(self._Selector__childOrSiblingSelector, [])
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self._Selector__fields:
            super(Selector, self).__setitem__(U(k), U(v))
            super(Selector, self).__setitem__(self._Selector__mask, self[self._Selector__mask] | self._Selector__fields[k][0])
        else:
            raise ReferenceError('%s is not allowed.' % k)

    def __delitem__(self, k):
        if k in self._Selector__fields:
            super(Selector, self).__delitem__(k)
            super(Selector, self).__setitem__(self._Selector__mask, self[self._Selector__mask] & ~self._Selector__fields[k][0])

    def clone(self):
        kwargs = dict((k, self[k]) for k in self if k not in [self._Selector__mask, self._Selector__childOrSibling, self._Selector__childOrSiblingSelector])
        selector = Selector(**kwargs)
        for v in self[self._Selector__childOrSibling]:
            selector[self._Selector__childOrSibling].append(v)

        for s in self[self._Selector__childOrSiblingSelector]:
            selector[self._Selector__childOrSiblingSelector].append(s.clone())

        return selector

    def child(self, **kwargs):
        self[self._Selector__childOrSibling].append('child')
        self[self._Selector__childOrSiblingSelector].append(Selector(**kwargs))
        return self

    def sibling(self, **kwargs):
        self[self._Selector__childOrSibling].append('sibling')
        self[self._Selector__childOrSiblingSelector].append(Selector(**kwargs))
        return self

    child_selector, from_parent = child, sibling


def rect(top=0, left=0, bottom=100, right=100):
    return {'top': top, 'left': left, 'bottom': bottom, 'right': right}


def intersect(rect1, rect2):
    top = rect1['top'] if rect1['top'] > rect2['top'] else rect2['top']
    bottom = rect1['bottom'] if rect1['bottom'] < rect2['bottom'] else rect2['bottom']
    left = rect1['left'] if rect1['left'] > rect2['left'] else rect2['left']
    right = rect1['right'] if rect1['right'] < rect2['right'] else rect2['right']
    return (left, top, right, bottom)


def point(x=0, y=0):
    return {'x': x, 'y': y}


class Adb(object):

    def __init__(self, serial=None, adb_server_host=None, adb_server_port=None):
        self._Adb__adb_cmd = None
        self.default_serial = serial if serial else os.environ.get('ANDROID_SERIAL', None)
        self.adb_server_host = str(adb_server_host if adb_server_host else 'localhost')
        self.adb_server_port = str(adb_server_port if adb_server_port else '5037')
        self.adbHostPortOptions = []
        if self.adb_server_host not in ('localhost', '127.0.0.1'):
            self.adbHostPortOptions += ['-H', self.adb_server_host]
        if self.adb_server_port != '5037':
            self.adbHostPortOptions += ['-P', self.adb_server_port]

    def adb(self):
        return
        if self._Adb__adb_cmd is None:
            if 'ANDROID_HOME' in os.environ:
                filename = 'adb.exe' if os.name == 'nt' else 'adb'
                adb_cmd = os.path.join(os.environ['ANDROID_HOME'], 'platform-tools', filename)
                if not os.path.exists(adb_cmd):
                    raise EnvironmentError('Adb not found in $ANDROID_HOME path: %s.' % os.environ['ANDROID_HOME'])
            else:
                filename = 'wadb.exe' if os.name == 'nt' else 'wadb'
                adb_cmd = os.path.join(os.getcwd(), '../../wadb', filename)
                logger.info('The adb being used is ' + str(adb_cmd))
            self._Adb__adb_cmd = adb_cmd
        return self._Adb__adb_cmd

    def cmd(self, *args, **kwargs):
        return
        serial = self.device_serial()
        if serial:
            if ' ' in serial:
                serial = "'%s'" % serial
            return self.raw_cmd(*args)
        else:
            return self.raw_cmd(*args)

    def raw_cmd(self, *args):
        return
        cmd_line = [
         self.adb()] + self.adbHostPortOptions + list(args)
        logger.info(cmd_line)
        if os.name != 'nt':
            cmd_line = [
             ' '.join(cmd_line)]
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def device_serial(self):
        return
        devices = self.default_serial or self.devices()
        if devices:
            if len(devices) is 1:
                self.default_serial = list(devices.keys())[0]
            else:
                raise EnvironmentError('Multiple devices attached but default android serial not set.')
        else:
            raise EnvironmentError('Device not attached.')
        return self.default_serial

    def devices(self):
        return
        out = self.raw_cmd('devices').communicate()[0].decode('utf-8')
        match = 'List of devices attached'
        index = out.find(match)
        if index < 0:
            raise EnvironmentError('adb is not working.')
        return dict([s.split('\t') for s in out[index + len(match):].strip().splitlines() if s.strip()])

    def forward(self, local_port, device_port):
        return
        return self.cmd('forward', 'tcp:%d' % local_port, 'tcp:%d' % device_port).wait()

    def forward_list(self):
        """adb forward --list"""
        return
        version = self.version()
        if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
            raise EnvironmentError('Low adb version.')
        lines = self.raw_cmd('forward', '--list').communicate()[0].decode('utf-8').strip().splitlines()
        return [line.strip().split() for line in lines]

    def version(self):
        return
        match = re.search('(\\d+)\\.(\\d+)\\.(\\d+)', self.raw_cmd('version').communicate()[0].decode('utf-8'))
        return [match.group(i) for i in range(4)]


_init_local_port = LOCAL_PORT - 1

def next_local_port(adbHost=None):
    global _init_local_port

    def is_port_listening(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((str(adbHost) if adbHost else '127.0.0.1', port))
        s.close()
        return result == 0

    _init_local_port = _init_local_port + 1 if _init_local_port < 32764 else LOCAL_PORT
    while is_port_listening(_init_local_port):
        _init_local_port += 1

    return _init_local_port


class NotFoundHandler(object):
    __doc__ = "\n    Handler for UI Object Not Found exception.\n    It's a replacement of UiAutomator watcher on device side.\n    "

    def __init__(self):
        self._NotFoundHandler__handlers = collections.defaultdict(lambda : {'on': True, 'handlers': []})

    def __get__(self, instance, type):
        return self._NotFoundHandler__handlers[instance.adb.device_serial()]


class AutomatorServer(object):
    __doc__ = 'start and quit rpc server on device.\n    '
    _AutomatorServer__jar_files = {'bundle.jar': 'libs/bundle.jar', 
     'uiautomator-stub.jar': 'libs/uiautomator-stub.jar'}
    _AutomatorServer__apk_files = [
     'libs/app-uiautomator.apk', 'libs/app-uiautomator-test.apk']
    _AutomatorServer__sdk = 0
    handlers = NotFoundHandler()

    def __init__(self, serial=None, local_port=None, device_port=None, adb_server_host=None, adb_server_port=None):
        self.uiautomator_process = None
        self.adb = Adb(serial=serial, adb_server_host=adb_server_host, adb_server_port=adb_server_port)
        self.device_port = int(device_port) if device_port else DEVICE_PORT
        if local_port:
            self.local_port = local_port
        else:
            try:
                for s, lp, rp in self.adb.forward_list():
                    if s == self.adb.device_serial() and rp == 'tcp:%d' % self.device_port:
                        self.local_port = int(lp[4:])
                        break
                else:
                    self.local_port = next_local_port(adb_server_host)

            except:
                self.local_port = next_local_port(adb_server_host)

    def push(self):
        base_dir = os.path.dirname(__file__)
        for jar, url in self._AutomatorServer__jar_files.items():
            filename = os.path.join(base_dir, url)
            self.adb.cmd('push', filename, '/data/local/tmp/').wait()

        return list(self._AutomatorServer__jar_files.keys())

    def install(self):
        base_dir = os.path.dirname(__file__)
        for apk in self._AutomatorServer__apk_files:
            self.adb.cmd('install', '-rt', os.path.join(base_dir, apk)).wait()

    @property
    def jsonrpc(self):
        return self.jsonrpc_wrap(timeout=int(os.environ.get('jsonrpc_timeout', 90)))

    @property
    def jsonmonitor(self):
        return self.jsonmonitor_wrap(timeout=int(os.environ.get('jsonrpc_timeout', 90)))

    def jsonrpc_wrap(self, timeout):
        server = self
        ERROR_CODE_BASE = -32000

        def _JsonRPCMethod(url, method, timeout, restart=True):
            _method_obj = JsonRPCMethod(url, method, timeout)

            def wrapper(*args, **kwargs):
                logger.debug('Request start'.format(*args))
                URLError = urllib3.exceptions.HTTPError if os.name == 'nt' else urllib2.URLError
                try:
                    try:
                        return _method_obj(*args, **kwargs)
                    except (URLError, socket.error, HTTPException) as e:
                        if restart:
                            server.stop()
                            server.start(timeout=30)
                            return _JsonRPCMethod(url, method, timeout, False)(*args, **kwargs)
                        raise
                    except JsonRPCError as e:
                        if e.code >= ERROR_CODE_BASE - 1:
                            server.stop()
                            server.start()
                            return _method_obj(*args, **kwargs)
                        if e.code == ERROR_CODE_BASE - 2 and self.handlers['on']:
                            try:
                                self.handlers['on'] = False
                                any(handler(self.handlers.get('device', None)) for handler in self.handlers['handlers'])
                            finally:
                                self.handlers['on'] = True

                            return _method_obj(*args, **kwargs)
                        raise

                finally:
                    logger.debug('Request end')

            return wrapper

        return JsonRPCClient(self.rpc_uri, timeout=timeout, method_class=_JsonRPCMethod)

    def jsonmonitor_wrap(self, timeout):
        server = self
        ERROR_CODE_BASE = -32000

        def _JsonRPCMethod(url, method, timeout, restart=True):
            _method_obj = JsonRPCMethod(url, method, timeout)

            def wrapper(*args, **kwargs):
                URLError = urllib3.exceptions.HTTPError if os.name == 'nt' else urllib2.URLError
                try:
                    return _method_obj(*args, **kwargs)
                except (URLError, socket.error, HTTPException) as e:
                    if restart:
                        server.stop()
                        server.start(timeout=30)
                        return _JsonRPCMethod(url, method, timeout, False)(*args, **kwargs)
                    raise
                except JsonRPCError as e:
                    if e.code >= ERROR_CODE_BASE - 1:
                        server.stop()
                        server.start()
                        return _method_obj(*args, **kwargs)
                    if e.code == ERROR_CODE_BASE - 2 and self.handlers['on']:
                        try:
                            self.handlers['on'] = False
                            any(handler(self.handlers.get('device', None)) for handler in self.handlers['handlers'])
                        finally:
                            self.handlers['on'] = True

                        return _method_obj(*args, **kwargs)
                    raise

            return wrapper

        return JsonRPCClient(self.monitor_uri, timeout=timeout, method_class=_JsonRPCMethod)

    def __jsonrpc(self):
        return JsonRPCClient(self.rpc_uri, timeout=int(os.environ.get('JSONRPC_TIMEOUT', 90)))

    def sdk_version(self):
        """sdk version of connected device."""
        if self._AutomatorServer__sdk == 0:
            try:
                self._AutomatorServer__sdk = int(self.adb.cmd('shell', 'getprop', 'ro.build.version.sdk').communicate()[0].decode('utf-8').strip())
            except:
                pass

            return self._AutomatorServer__sdk

    def start(self, timeout=5):
        return
        logger.info('Start the rpc server.')
        files = self.push()
        cmd = list(itertools.chain([
         'shell', 'uiautomator', 'runtest'], files, [
         '-c', 'com.github.uiautomatorstub.Stub']))
        self.uiautomator_process = self.adb.cmd(*cmd)
        self.adb.forward(self.local_port, self.device_port)
        while not self.alive and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1

        if not self.alive:
            raise IOError('RPC server not started!')

    def ping(self):
        try:
            return self._AutomatorServer__jsonrpc().ping()
        except:
            return

    @property
    def alive(self):
        """Check if the rpc server is alive."""
        return self.ping() == 'pong'

    def stop(self):
        return
        logger.info('stop the rpc server.')
        logger.info(self.uiautomator_process)
        if self.uiautomator_process and self.uiautomator_process.poll() is None:
            res = None
            try:
                try:
                    res = urllib2.urlopen(self.stop_uri)
                    self.uiautomator_process.wait()
                except:
                    self.uiautomator_process.kill()

            finally:
                if res is not None:
                    res.close()
                self.uiautomator_process = None

        try:
            out = self.adb.cmd('shell', 'ps', '-C', 'uiautomator').communicate()[0].decode('utf-8').strip().splitlines()
            if out:
                index = out[0].split().index('PID')
                for line in out[1:]:
                    if len(line.split()) > index:
                        self.adb.cmd('shell', 'kill', '-9', line.split()[index]).wait()

        except:
            pass

    @property
    def monitor_uri(self):
        return 'http://%s:%d/permission' % (self.adb.adb_server_host, self.local_port)

    @property
    def stop_uri(self):
        return 'http://%s:%d/stop' % (self.adb.adb_server_host, self.local_port)

    @property
    def rpc_uri(self):
        return 'http://%s:%d/jsonrpc/0' % (self.adb.adb_server_host, self.local_port)

    @property
    def screenshot_uri(self):
        return 'http://%s:%d/screenshot/0' % (self.adb.adb_server_host, self.local_port)

    def screenshot(self, filename=None, scale=1.0, quality=100):
        if self.sdk_version() >= 18:
            try:
                req = urllib2.Request('%s?scale=%f&quality=%f' % (self.screenshot_uri, scale, quality))
                result = urllib2.urlopen(req, timeout=30)
                if filename:
                    with open(filename, 'wb') as (f):
                        f.write(result.read())
                        return filename
                else:
                    return result.read()
            except:
                pass


class AutomatorDevice(object):
    __doc__ = 'uiautomator wrapper of android device'
    _AutomatorDevice__orientation = ((0, 'natural', 'n', 0), (1, 'left', 'l', 90),
                                     (2, 'upsidedown', 'u', 180), (3, 'right', 'r', 270))
    _AutomatorDevice__alias = {'width': 'displayWidth', 
     'height': 'displayHeight'}

    def __init__(self, serial=None, local_port=None, adb_server_host=None, adb_server_port=None):
        self.server = AutomatorServer(serial=serial, local_port=local_port, adb_server_host=adb_server_host, adb_server_port=adb_server_port)

    def __call__(self, **kwargs):
        return AutomatorDeviceObject(self, Selector(**kwargs))

    def __getattr__(self, attr):
        """alias of fields in info property."""
        info = self.info
        if attr in info:
            return info[attr]
        if attr in self._AutomatorDevice__alias:
            return info[self._AutomatorDevice__alias[attr]]
        raise AttributeError('%s attribute not found!' % attr)

    @property
    def info(self):
        """Get the device info.
        {u'model': u'HUAWEI P7-L00', u'displayRotation': 1, u'displaySizeDpY': 360, u'displaySizeDpX': 640, u'brand': u'Huawei', u'displayWidth': 1794,
         u'productName': u'P7-L00', u'release': u'4.4.2',
         u'currentPackageName': u'com.yhkd.jztkc', u'device': u'hwp7', u'sdkInt': 19, u'displayHeight': 1080, u'id': u'HuaweiP7-L00', u'naturalOrientation': False}
        """
        return self.server.jsonrpc.deviceInfo()

    def click(self, x, y):
        """click at arbitrary coordinates."""
        return self.server.jsonrpc.click(x, y)

    def long_click(self, x, y):
        """long click at arbitrary coordinates."""
        return self.swipe(x, y, x + 1, y + 1)

    def swipe(self, sx, sy, ex, ey, steps=100):
        return self.server.jsonrpc.swipe(sx, sy, ex, ey, steps)

    def swipePoints(self, points, steps=100):
        ppoints = []
        for p in points:
            ppoints.append(p[0])
            ppoints.append(p[1])

        return self.server.jsonrpc.swipePoints(ppoints, steps)

    def drag(self, sx, sy, ex, ey, steps=100):
        """Swipe from one point to another point."""
        return self.server.jsonrpc.drag(sx, sy, ex, ey, steps)

    def dump(self, filename=None, compressed=True, pretty=True):
        """dump device window and pull to local file."""
        content = self.server.jsonrpc.dumpWindowHierarchy(compressed, None)
        if content is None:
            logger.info('uiauto dump content is none')
            return
        if filename:
            with open(filename, 'wb') as (f):
                f.write(content.encode('utf-8'))
        if pretty and '\n ' not in content:
            xml_text = xml.dom.minidom.parseString(content.encode('utf-8'))
            content = U(xml_text.toprettyxml(indent='  '))
        return content

    def setdialogtextpattern(self, content):
        if six.PY2:
            content = content.decode('UTF-8')
        logger.info('Set text check regex pattern = ' + content)
        res = self.server.jsonmonitor.setTextPattern(content)

    def setdialogtextgrouppattern(self, content):
        if six.PY2:
            content = content.decode('UTF-8')
        logger.info('Set textgroup check regex pattern = ' + content)
        res = self.server.jsonmonitor.setTextMatchGroups(content)

    def setdialogpkgpattern(self, content):
        if six.PY2:
            content = content.decode('UTF-8')
        logger.info('Set packge check regex pattern = ' + content)
        res = self.server.jsonmonitor.setPackagePattern(content)

    def setPermissionMonitor(self, resume):
        logger.info('setPermissionMonitor = ' + str(resume))
        res = self.server.jsonmonitor.setPermissionMonitor(resume)

    def screenshot(self, filename, scale=1.0, quality=100):
        """take screenshot."""
        result = self.server.screenshot(filename, scale, quality)
        if result:
            return result
        device_file = self.server.jsonrpc.takeScreenshot('screenshot.png', scale, quality)
        if not device_file:
            return
        p = self.server.adb.cmd('pull', device_file, filename)
        p.wait()
        self.server.adb.cmd('shell', 'rm', device_file).wait()
        if p.returncode is 0:
            return filename

    def freeze_rotation(self, freeze=True):
        """freeze or unfreeze the device rotation in current status."""
        self.server.jsonrpc.freezeRotation(freeze)

    @property
    def orientation(self):
        """
        orienting the devie to left/right or natural.
        left/l:       rotation=90 , displayRotation=1
        right/r:      rotation=270, displayRotation=3
        natural/n:    rotation=0  , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        """
        return self._AutomatorDevice__orientation[self.info['displayRotation']][1]

    @orientation.setter
    def orientation(self, value):
        """setter of orientation property."""
        for values in self._AutomatorDevice__orientation:
            if value in values:
                self.server.jsonrpc.setOrientation(values[1])
                break
        else:
            raise ValueError('Invalid orientation.')

    @property
    def last_traversed_text(self):
        """get last traversed text. used in webview for highlighted text."""
        return self.server.jsonrpc.getLastTraversedText()

    def clear_traversed_text(self):
        """clear the last traversed text."""
        self.server.jsonrpc.clearLastTraversedText()

    @property
    def open(self):
        """
        Open notification or quick settings.
        Usage:
        d.open.notification()
        d.open.quick_settings()
        """

        @param_to_property(action=['notification', 'quick_settings'])
        def _open(action):
            if action == 'notification':
                return self.server.jsonrpc.openNotification()
            else:
                return self.server.jsonrpc.openQuickSettings()

        return _open

    @property
    def handlers(self):
        obj = self

        class Handlers(object):

            def on(self, fn):
                if fn not in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].append(fn)
                obj.server.handlers['device'] = obj
                return fn

            def off(self, fn):
                if fn in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].remove(fn)

        return Handlers()

    @property
    def watchers(self):
        obj = self

        class Watchers(list):

            def __init__(self):
                for watcher in obj.server.jsonrpc.getWatchers():
                    self.append(watcher)

            @property
            def triggered(self):
                return obj.server.jsonrpc.hasAnyWatcherTriggered()

            def remove(self, name=None):
                if name:
                    obj.server.jsonrpc.removeWatcher(name)
                else:
                    for name in self:
                        obj.server.jsonrpc.removeWatcher(name)

            def reset(self):
                obj.server.jsonrpc.resetWatcherTriggers()
                return self

            def run(self):
                obj.server.jsonrpc.runWatchers()
                return self

        return Watchers()

    def watcher(self, name):
        obj = self

        class Watcher(object):

            def __init__(self):
                self._Watcher__selectors = []

            @property
            def triggered(self):
                return obj.server.jsonrpc.hasWatcherTriggered(name)

            def remove(self):
                obj.server.jsonrpc.removeWatcher(name)

            def when(self, **kwargs):
                self._Watcher__selectors.append(Selector(**kwargs))
                return self

            def click(self, **kwargs):
                obj.server.jsonrpc.registerClickUiObjectWatcher(name, self._Watcher__selectors, Selector(**kwargs))

            @property
            def press(self):

                @param_to_property('home', 'back', 'left', 'right', 'up', 'down', 'center', 'search', 'enter', 'delete', 'del', 'recent', 'volume_up', 'menu', 'volume_down', 'volume_mute', 'camera', 'power')
                def _press(*args):
                    obj.server.jsonrpc.registerPressKeyskWatcher(name, self._Watcher__selectors, args)

                return _press

        return Watcher()

    @property
    def press(self):
        """
        press key via name or key code. Supported key name includes:
        home, back, left, right, up, down, center, menu, search, enter,
        delete(or del), recent(recent apps), volume_up, volume_down,
        volume_mute, camera, power.
        Usage:
        d.press.back()  # press back key
        d.press.menu()  # press home key
        d.press(89)     # press keycode
        """

        @param_to_property(key=[
         'home', 'back', 'left', 'right', 'up', 'down', 'center',
         'menu', 'search', 'enter', 'delete', 'del', 'recent',
         'volume_up', 'volume_down', 'volume_mute', 'camera', 'power'])
        def _press(key, meta=None):
            if isinstance(key, int):
                if meta:
                    return self.server.jsonrpc.pressKeyCode(key, meta)
                return self.server.jsonrpc.pressKeyCode(key)
            else:
                return self.server.jsonrpc.pressKey(str(key))

        return _press

    def wakeup(self):
        """turn on screen in case of screen off."""
        self.server.jsonrpc.wakeUp()

    def sleep(self):
        """turn off screen in case of screen on."""
        self.server.jsonrpc.sleep()

    @property
    def screen(self):
        """
        Turn on/off screen.
        Usage:
        d.screen.on()
        d.screen.off()

        d.screen == 'on'  # Check if the screen is on, same as 'd.screenOn'
        d.screen == 'off'  # Check if the screen is off, same as 'not d.screenOn'
        """
        devive_self = self

        class _Screen(object):

            def on(self):
                return devive_self.wakeup()

            def off(self):
                return devive_self.sleep()

            def __call__(self, action):
                if action == 'on':
                    return self.on()
                if action == 'off':
                    return self.off()
                raise AttributeError('Invalid parameter: %s' % action)

            def __eq__(self, value):
                info = devive_self.info
                if 'screenOn' not in info:
                    raise EnvironmentError('Not supported on Android 4.3 and belows.')
                if value in ('on', 'On', 'ON'):
                    return info['screenOn']
                if value in ('off', 'Off', 'OFF'):
                    return not info['screenOn']
                raise ValueError('Invalid parameter. It can only be compared with on/off.')

            def __ne__(self, value):
                return not self.__eq__(value)

        return _Screen()

    @property
    def wait(self):
        """
        Waits for the current application to idle or window update event occurs.
        Usage:
        d.wait.idle(timeout=1000)
        d.wait.update(timeout=1000, package_name="com.android.settings")
        """

        @param_to_property(action=['idle', 'update'])
        def _wait(action, timeout=1000, package_name=None):
            if timeout / 1000 + 5 > int(os.environ.get('JSONRPC_TIMEOUT', 90)):
                http_timeout = timeout / 1000 + 5
            else:
                http_timeout = int(os.environ.get('JSONRPC_TIMEOUT', 90))
            if action == 'idle':
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForIdle(timeout)
            if action == 'update':
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForWindowUpdate(package_name, timeout)

        return _wait

    def exists(self, **kwargs):
        """Check if the specified ui object by kwargs exists."""
        return self(**kwargs).exists


Device = AutomatorDevice

class AutomatorDeviceUiObject(object):
    __doc__ = 'Represent a UiObject, on which user can perform actions, such as click, set text\n    '
    _AutomatorDeviceUiObject__alias = {'description': 'contentDescription'}

    def __init__(self, device, selector):
        self.device = device
        self.jsonrpc = device.server.jsonrpc
        self.selector = selector

    @property
    def exists(self):
        """check if the object exists in current window."""
        return self.jsonrpc.exist(self.selector)

    def __getattr__(self, attr):
        """alias of fields in info property."""
        info = self.info
        if attr in info:
            return info[attr]
        if attr in self._AutomatorDeviceUiObject__alias:
            return info[self._AutomatorDeviceUiObject__alias[attr]]
        raise AttributeError('%s attribute not found!' % attr)

    @property
    def info(self):
        """ui object info."""
        return self.jsonrpc.objInfo(self.selector)

    def set_text(self, text):
        """set the text field."""
        if text in (None, ''):
            return self.jsonrpc.clearTextField(self.selector)
        else:
            if isinstance(text, str):
                text = imap_utf7.encode(text.decode('utf-8'))
            else:
                text = imap_utf7.encode(text)
            return self.jsonrpc.setText(self.selector, text)

    def clear_text(self):
        """clear text. alias for set_text(None)."""
        self.set_text(None)

    def get_text(self):
        return self.jsonrpc.getText(self.selector)

    @property
    def click(self):
        """
        click on the ui object.
        Usage:
        d(text="Clock").click()  # click on the center of the ui object
        d(text="OK").click.wait(timeout=3000) # click and wait for the new window update
        d(text="John").click.topleft() # click on the topleft of the ui object
        d(text="John").click.bottomright() # click on the bottomright of the ui object
        """

        @param_to_property(action=['tl', 'topleft', 'br', 'bottomright', 'wait'])
        def _click(action=None, timeout=3000):
            if action is None:
                return self.jsonrpc.click(self.selector)
            else:
                if action in ('tl', 'topleft', 'br', 'bottomright'):
                    return self.jsonrpc.click(self.selector, action)
                return self.jsonrpc.clickAndWaitForNewWindow(self.selector, timeout)

        return _click

    @property
    def long_click(self):
        """
        Perform a long click action on the object.
        Usage:
        d(text="Image").long_click()  # long click on the center of the ui object
        d(text="Image").long_click.topleft()  # long click on the topleft of the ui object
        d(text="Image").long_click.bottomright()  # long click on the topleft of the ui object
        """

        @param_to_property(corner=['tl', 'topleft', 'br', 'bottomright'])
        def _long_click(corner=None):
            info = self.info
            if info['longClickable']:
                if corner:
                    return self.jsonrpc.longClick(self.selector, corner)
                else:
                    return self.jsonrpc.longClick(self.selector)
            else:
                bounds = info.get('visibleBounds') or info.get('bounds')
                if corner in ('tl', 'topleft'):
                    x = (5 * bounds['left'] + bounds['right']) / 6
                    y = (5 * bounds['top'] + bounds['bottom']) / 6
                else:
                    if corner in ('br', 'bottomright'):
                        x = (bounds['left'] + 5 * bounds['right']) / 6
                        y = (bounds['top'] + 5 * bounds['bottom']) / 6
                    else:
                        x = (bounds['left'] + bounds['right']) / 2
                        y = (bounds['top'] + bounds['bottom']) / 2
                    return self.device.long_click(x, y)

        return _long_click

    @property
    def drag(self):
        """
        Drag the ui object to other point or ui object.
        Usage:
        d(text="Clock").drag.to(x=100, y=100)  # drag to point (x,y)
        d(text="Clock").drag.to(text="Remove") # drag to another object
        """

        def to(obj, *args, **kwargs):
            if len(args) >= 2 or 'x' in kwargs or 'y' in kwargs:
                drag_to = lambda x, y, steps=100: self.jsonrpc.dragTo(self.selector, x, y, steps)
            else:
                drag_to = lambda steps=100, **kwargs: self.jsonrpc.dragTo(self.selector, Selector(**kwargs), steps)
            return drag_to(*args, **kwargs)

        return type('Drag', (object,), {'to': to})()

    def gesture(self, start1, start2, *args, **kwargs):
        """
        perform two point gesture.
        Usage:
        d().gesture(startPoint1, startPoint2).to(endPoint1, endPoint2, steps)
        d().gesture(startPoint1, startPoint2, endPoint1, endPoint2, steps)
        """

        def to(obj_self, end1, end2, steps=100):
            ctp = lambda pt: point(*pt) if type(pt) == tuple else pt
            s1, s2, e1, e2 = (ctp(start1), ctp(start2), ctp(end1), ctp(end2))
            return self.jsonrpc.gesture(self.selector, s1, s2, e1, e2, steps)

        obj = type('Gesture', (object,), {'to': to})()
        if len(args) == 0:
            return obj
        return to(None, *args, **kwargs)

    @property
    def pinch(self):
        """
        Perform two point gesture from edge to center(in) or center to edge(out).
        Usages:
        d().pinch.In(percent=100, steps=10)
        d().pinch.Out(percent=100, steps=100)
        """

        @param_to_property(in_or_out=['In', 'Out'])
        def _pinch(in_or_out='Out', percent=100, steps=50):
            if in_or_out in ('Out', 'out'):
                return self.jsonrpc.pinchOut(self.selector, percent, steps)
            if in_or_out in ('In', 'in'):
                return self.jsonrpc.pinchIn(self.selector, percent, steps)

        return _pinch

    @property
    def swipe(self):
        """
        Perform swipe action. if device platform greater than API 18, percent can be used and value between 0 and 1
        Usages:
        d().swipe.right()
        d().swipe.left(steps=10)
        d().swipe.up(steps=10)
        d().swipe.down()
        d().swipe("right", steps=20)
        d().swipe("right", steps=20, percent=0.5)
        """

        @param_to_property(direction=['up', 'down', 'right', 'left'])
        def _swipe(direction='left', steps=10, percent=1):
            if percent == 1:
                return self.jsonrpc.swipe(self.selector, direction, steps)
            else:
                return self.jsonrpc.swipe(self.selector, direction, percent, steps)

        return _swipe

    @property
    def wait(self):
        """
        Wait until the ui object gone or exist.
        Usage:
        d(text="Clock").wait.gone()  # wait until it's gone.
        d(text="Settings").wait.exists() # wait until it appears.
        """

        @param_to_property(action=['exists', 'gone'])
        def _wait(action, timeout=3000):
            if timeout / 1000 + 5 > int(os.environ.get('JSONRPC_TIMEOUT', 90)):
                http_timeout = timeout / 1000 + 5
            else:
                http_timeout = int(os.environ.get('JSONRPC_TIMEOUT', 90))
            method = self.device.server.jsonrpc_wrap(timeout=http_timeout).waitUntilGone if action == 'gone' else self.device.server.jsonrpc_wrap(timeout=http_timeout).waitForExists
            return method(self.selector, timeout)

        return _wait


class AutomatorDeviceNamedUiObject(AutomatorDeviceUiObject):

    def __init__(self, device, name):
        super(AutomatorDeviceNamedUiObject, self).__init__(device, name)

    def child(self, **kwargs):
        return AutomatorDeviceNamedUiObject(self.device, self.jsonrpc.getChild(self.selector, Selector(**kwargs)))

    def sibling(self, **kwargs):
        return AutomatorDeviceNamedUiObject(self.device, self.jsonrpc.getFromParent(self.selector, Selector(**kwargs)))


class AutomatorDeviceObject(AutomatorDeviceUiObject):
    __doc__ = 'Represent a generic UiObject/UiScrollable/UiCollection,\n    on which user can perform actions, such as click, set text\n    '

    def __init__(self, device, selector):
        super(AutomatorDeviceObject, self).__init__(device, selector)

    def child(self, **kwargs):
        """set childSelector."""
        return AutomatorDeviceObject(self.device, self.selector.clone().child(**kwargs))

    def sibling(self, **kwargs):
        """set fromParent selector."""
        return AutomatorDeviceObject(self.device, self.selector.clone().sibling(**kwargs))

    child_selector, from_parent = child, sibling

    def child_by_text(self, txt, **kwargs):
        if 'allow_scroll_search' in kwargs:
            allow_scroll_search = kwargs.pop('allow_scroll_search')
            name = self.jsonrpc.childByText(self.selector, Selector(**kwargs), txt, allow_scroll_search)
        else:
            name = self.jsonrpc.childByText(self.selector, Selector(**kwargs), txt)
        return AutomatorDeviceNamedUiObject(self.device, name)

    def child_by_description(self, txt, **kwargs):
        if 'allow_scroll_search' in kwargs:
            allow_scroll_search = kwargs.pop('allow_scroll_search')
            name = self.jsonrpc.childByDescription(self.selector, Selector(**kwargs), txt, allow_scroll_search)
        else:
            name = self.jsonrpc.childByDescription(self.selector, Selector(**kwargs), txt)
        return AutomatorDeviceNamedUiObject(self.device, name)

    def child_by_instance(self, inst, **kwargs):
        return AutomatorDeviceNamedUiObject(self.device, self.jsonrpc.childByInstance(self.selector, Selector(**kwargs), inst))

    @property
    def count(self):
        return self.jsonrpc.count(self.selector)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        count = self.count
        if index >= count:
            raise IndexError()
        else:
            if count == 1:
                return self
            else:
                selector = self.selector.clone()
                selector['instance'] = index
                return AutomatorDeviceObject(self.device, selector)

    def __iter__(self):
        obj, length = self, self.count

        class Iter(object):

            def __init__(self):
                self.index = -1

            def next(self):
                self.index += 1
                if self.index < length:
                    return obj[self.index]
                raise StopIteration()

            __next__ = next

        return Iter()

    def right(self, **kwargs):

        def onrightof(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            if top < bottom:
                return rect2['left'] - rect1['right']
            return -1

        return self._AutomatorDeviceObject__view_beside(onrightof, **kwargs)

    def left(self, **kwargs):

        def onleftof(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            if top < bottom:
                return rect1['left'] - rect2['right']
            return -1

        return self._AutomatorDeviceObject__view_beside(onleftof, **kwargs)

    def up(self, **kwargs):

        def above(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            if left < right:
                return rect1['top'] - rect2['bottom']
            return -1

        return self._AutomatorDeviceObject__view_beside(above, **kwargs)

    def down(self, **kwargs):

        def under(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            if left < right:
                return rect2['top'] - rect1['bottom']
            return -1

        return self._AutomatorDeviceObject__view_beside(under, **kwargs)

    def __view_beside(self, onsideof, **kwargs):
        bounds = self.info['bounds']
        min_dist, found = (-1, None)
        for ui in AutomatorDeviceObject(self.device, Selector(**kwargs)):
            dist = onsideof(bounds, ui.info['bounds'])
            if dist >= 0 and (min_dist < 0 or dist < min_dist):
                min_dist, found = dist, ui

        return found

    @property
    def fling(self):
        """
        Perform fling action.
        Usage:
        d().fling()  # default vertically, forward
        d().fling.horiz.forward()
        d().fling.vert.backward()
        d().fling.toBeginning(max_swipes=100) # vertically
        d().fling.horiz.toEnd()
        """

        @param_to_property(dimention=[
         'vert', 'vertically', 'vertical', 'horiz', 'horizental', 'horizentally'], action=[
         'forward', 'backward', 'toBeginning', 'toEnd'])
        def _fling(dimention='vert', action='forward', max_swipes=1000):
            vertical = dimention in ('vert', 'vertically', 'vertical')
            if action == 'forward':
                return self.jsonrpc.flingForward(self.selector, vertical)
            if action == 'backward':
                return self.jsonrpc.flingBackward(self.selector, vertical)
            if action == 'toBeginning':
                return self.jsonrpc.flingToBeginning(self.selector, vertical, max_swipes)
            if action == 'toEnd':
                return self.jsonrpc.flingToEnd(self.selector, vertical, max_swipes)

        return _fling

    @property
    def scroll(self):
        """
        Perfrom scroll action.
        Usage:
        d().scroll(steps=50) # default vertically and forward
        d().scroll.horiz.forward(steps=100)
        d().scroll.vert.backward(steps=100)
        d().scroll.horiz.toBeginning(steps=100, max_swipes=100)
        d().scroll.vert.toEnd(steps=100)
        d().scroll.horiz.to(text="Clock")
        """

        def __scroll(vertical, forward, steps=100):
            method = self.jsonrpc.scrollForward if forward else self.jsonrpc.scrollBackward
            return method(self.selector, vertical, steps)

        def __scroll_to_beginning(vertical, steps=100, max_swipes=1000):
            return self.jsonrpc.scrollToBeginning(self.selector, vertical, max_swipes, steps)

        def __scroll_to_end(vertical, steps=100, max_swipes=1000):
            return self.jsonrpc.scrollToEnd(self.selector, vertical, max_swipes, steps)

        def __scroll_to(vertical, **kwargs):
            return self.jsonrpc.scrollTo(self.selector, Selector(**kwargs), vertical)

        @param_to_property(dimention=[
         'vert', 'vertically', 'vertical', 'horiz', 'horizental', 'horizentally'], action=[
         'forward', 'backward', 'toBeginning', 'toEnd', 'to'])
        def _scroll(dimention='vert', action='forward', **kwargs):
            vertical = dimention in ('vert', 'vertically', 'vertical')
            if action in ('forward', 'backward'):
                return _AutomatorDeviceObject__scroll(vertical, action == 'forward', **kwargs)
            if action == 'toBeginning':
                return _AutomatorDeviceObject__scroll_to_beginning(vertical, **kwargs)
            if action == 'toEnd':
                return _AutomatorDeviceObject__scroll_to_end(vertical, **kwargs)
            if action == 'to':
                return _AutomatorDeviceObject__scroll_to(vertical, **kwargs)

        return _scroll