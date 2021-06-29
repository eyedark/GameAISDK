# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/common/AdbTool.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 4845 bytes
__author__ = 'minhuaxu'
import logging, os, re, subprocess, sys
logger = logging.getLogger(__name__)
_IS_PY2 = sys.version_info[0] < 3

class AdbTool(object):

    def __init__(self, serial=None, adb_server_host=None, adb_server_port=None):
        self._AdbTool__adb_cmd = None
        self.default_serial = serial if serial else os.environ.get('ANDROID_SERIAL', None)
        self.adb_server_host = str(adb_server_host if adb_server_host else 'localhost')
        self.adb_server_port = str(adb_server_port if adb_server_port else '5037')

    def adb(self):
        if self._AdbTool__adb_cmd is None:
            if 'ANDROID_HOME' in os.environ:
                filename = 'adb.exe' if os.name == 'nt' else 'adb'
                adb_cmd = os.path.join(os.environ['ANDROID_HOME'], 'platform-tools', filename)
                if not os.path.exists(adb_cmd):
                    raise EnvironmentError('Adb not found in $ANDROID_HOME path: %s.' % os.environ['ANDROID_HOME'])
            else:
                adb_cmd = 'adb.exe' if os.name == 'nt' else 'adb'
            self._AdbTool__adb_cmd = adb_cmd
        return self._AdbTool__adb_cmd

    def cmd(self, *args):
        """adb command, add -s serial by default. return the subprocess.Popen object."""
        serial = self.device_serial()
        if serial:
            return self.raw_cmd(*['-s', serial] + list(args))
        else:
            return self.raw_cmd(*args)

    def cmd_wait(self, *args):
        cmd = self.cmd(*args)
        cmd.wait()
        erro, out = cmd.communicate()
        return out

    def raw_cmd(self, *args):
        """adb command. return the subprocess.Popen object."""
        if _IS_PY2:
            cmd_line = [
             self.adb()] + [i.decode('UTF8') for i in list(args)]
        else:
            cmd_line = [
             self.adb()] + list(args)
        if os.name != 'nt':
            cmd_line = [
             ' '.join(cmd_line)]
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def device_serial(self):
        if not self.default_serial:
            devices = self.devices()
            if devices:
                if len(devices) is 1:
                    self.default_serial = list(devices.keys())[0]
                else:
                    raise EnvironmentError('Multiple devices attached but default android serial not set.')
            else:
                raise EnvironmentError('Device not attached.')
            return self.default_serial

    def devices(self):
        """get a dict of attached devices. key is the device serial, value is device name."""
        out = self.raw_cmd('devices').communicate()[0].decode('utf-8')
        match = 'List of devices attached'
        index = out.find(match)
        if index < 0:
            raise EnvironmentError('adb is not working.')
        search_result = re.findall('^\\s*(\\S+)\\s+device\\s*$', out, re.MULTILINE)
        if search_result:
            rlt = {}
            for sid in search_result:
                rlt[sid] = 'device'

            return rlt
        return {}

    def forward(self, local_port, device_port):
        """adb port forward. return 0 if success, else non-zero."""
        return self.cmd('forward', 'tcp:{0}'.format(local_port), 'tcp:{0}'.format(device_port)).wait()

    def forward_list(self):
        """list all forward socket connections."""
        version = self.version()
        if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
            raise EnvironmentError('Low adb version.')
        lines = self.cmd('forward', '--list').communicate()[0].decode('utf-8').strip().splitlines()
        return [line.strip().split() for line in lines]

    def push(self, src, dest):
        """push file to phone"""
        return self.cmd('push', src, dest)

    def version(self):
        """adb version"""
        match = re.search('(\\d+)\\.(\\d+)\\.(\\d+)', self.cmd('version').communicate()[0].decode('utf-8'))
        return [match.group(i) for i in range(4)]