# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/device_remote_interaction/common/action_queue.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 587 bytes
import queue as Queue

class ActionResultQueue(object):

    def __init__(self):
        self.phone_result_queque = Queue.Queue()

    def add_action_item(self, msg):
        self.phone_result_queque.put_nowait(msg)

    def get_action_item(self):
        if self.phone_result_queque.empty():
            return
        else:
            return self.phone_result_queque.get_nowait()

    def get_queque_size(self):
        return self.phone_result_queque.qsize()

    def reset(self):
        self.phone_result_queque.queue.clear()


action_result_queue_inst = ActionResultQueue()