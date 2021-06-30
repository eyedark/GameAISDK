# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\demop\action_process.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 2614 bytes
import threading, time

class ActionProcess(threading.Thread):

    def __init__(self, aiclientapi):
        threading.Thread.__init__(self)
        self.aiclientapi = aiclientapi
        self.last_time = None
        self.action_dict = {}
        self.action_num = 0

    def run(self):
        print('prepare recv action msg')
        start_time = time.time()
        while True:
            print('recv msg')
            msg = self.aiclientapi.recv_msg()
            if msg is None:
                if time.time() - start_time > 5:
                    print('msg is None')
                time.sleep(0.1)
            start_time = time.time()
            self.action_excute(msg, convert_rate=1)

    def action_excute(self, msg, convert_rate=1.0):
        print('recv msg', msg)
        if self.last_time is None:
            self.last_time = time.time()
        else:
            print('time elapse:{}'.format(time.time() - self.last_time))
        img_id = msg.get('img_id', -1)
        self.action_num += 1
        self.action_dict[img_id] = 0
        print('action_num:{}'.format(self.action_num))
        print('img num:{}'.format(len(self.action_dict)))
        status = msg.get('status', 0)
        if status == 1:
            self.aiclientapi.game_has_start = True
        op_code = msg['op_code']
        if op_code == 1:
            x = int(msg['px'] * convert_rate)
            y = int(msg['py'] * convert_rate)
            contact = msg['contact']
            print(x, y, contact)
        else:
            if op_code == 2:
                x1 = int(msg['start_x'] * convert_rate)
                y1 = int(msg['start_y'] * convert_rate)
                x2 = int(msg['end_x'] * convert_rate)
                y2 = int(msg['end_y'] * convert_rate)
            else:
                if op_code == 3:
                    x = int(msg['px'] * convert_rate)
                    y = int(msg['py'] * convert_rate)
                    contact = msg['contact']
                    print(x, y, contact)
                else:
                    if op_code == 4:
                        x = int(msg['px'] * convert_rate)
                        y = int(msg['py'] * convert_rate)
                        contact = msg['contact']
                        print(x, y, contact)
                    elif op_code == 5:
                        x = int(msg['px'] * convert_rate)
                        y = int(msg['py'] * convert_rate)
                        contact = msg['contact']
                        print(x, y, contact)