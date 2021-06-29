# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/common/freeport.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 1744 bytes
import threading

class BindFreePort(object):

    def __init__(self, start, stop):
        self.port = None
        import random, socket
        self.sock = socket.socket()
        while True:
            port = random.randint(start, stop)
            try:
                self.sock.bind(('', port))
                self.port = port
                break
            except Exception:
                continue

    def release(self):
        assert self.port is not None
        self.sock.close()


class FreePort(object):
    used_ports = set()

    def __init__(self, start=4000, stop=6000):
        self.lock = None
        self.bind = None
        self.port = None
        from fasteners.process_lock import InterProcessLock
        import time
        while 1:
            bind = BindFreePort(start, stop)
            if bind.port in self.used_ports:
                bind.release()
                continue
            else:
                lock = InterProcessLock(path='/tmp/socialdna/port_{}_lock'.format(bind.port))
                success = lock.acquire(blocking=False)
                if success:
                    self.lock = lock
                    self.port = bind.port
                    self.used_ports.add(bind.port)
                    bind.release()
                    break
                bind.release()
                time.sleep(0.01)

    def release(self):
        assert self.lock is not None
        assert self.port is not None
        self.used_ports.remove(self.port)
        self.lock.release()