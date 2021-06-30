# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\performance_profile\speed_check.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 3554 bytes
import time, logging
from ..tool_manage import communicate_config as com_config
REMCORD_INTERVAL_NUM = 20
PROCESS_IMG_TIME_INTERVAL = 20
IMG_SPEED_PROCESS_INTERVAL_NUM = 50

class SpeedCheck(object):

    def __init__(self):
        self.MONITOR_LOGGER = logging.getLogger('monitor')
        self.img_recv_dict = {}
        self.process_img_dict = {}
        self.img_recv_num = 0
        self.process_action_num = 0
        self.process_img_num = 0
        self.avg_action_process_time = 0
        self.avg_img_process_time = 0
        self.sum_action_process_time = 0
        self.img_process_speed_dict = set()
        self.img_process_speed_start_time = 0

    def is_need_record(self):
        return com_config.IS_TEST_SPEED

    def add_img(self, img_id):
        if not self.is_need_record():
            return
        self.img_recv_dict[img_id] = time.time()
        self.img_recv_num += 1

    def caculate_ai_process_time(self, img_id):
        if not self.is_need_record():
            return
        self.record_img_process_speed(img_id)
        if self.img_recv_dict.__contains__(img_id):
            diff_time = time.time() - self.img_recv_dict[img_id]
            self.sum_action_process_time += diff_time
            self.process_action_num += 1
            self.process_img_dict[img_id] = time.time()
            if len(self.process_img_dict) % PROCESS_IMG_TIME_INTERVAL == 0:
                sum_time = 0
                for key in self.process_img_dict.keys():
                    sum_time += self.process_img_dict[key] - self.img_recv_dict[key]

                self.avg_img_process_time = (self.avg_img_process_time * self.process_img_num + sum_time) / (self.process_img_num + len(self.process_img_dict))
                self.process_img_num += len(self.process_img_dict)
                self.process_img_dict = {}
                key_list = []
                for key in self.img_recv_dict.keys():
                    if key <= img_id:
                        key_list.append(key)

                for key in key_list:
                    del self.img_recv_dict[key]

            if self.process_action_num % REMCORD_INTERVAL_NUM == 0:
                self.MONITOR_LOGGER.info('process action num:{a}, avg_action_process_time:{b}'.format(a=(self.process_action_num),
                  b=(self.sum_action_process_time / self.process_action_num)))
                self.MONITOR_LOGGER.info('process_img num:{a}, avg_img_process_time:{b}'.format(a=(self.process_img_num),
                  b=(self.avg_img_process_time)))

    def record_img_process_speed(self, img_id):
        if len(self.img_process_speed_dict) == 0:
            self.img_process_speed_dict.add(img_id)
            self.img_process_speed_start_time = time.time()
        else:
            self.img_process_speed_dict.add(img_id)
        if len(self.img_process_speed_dict) % IMG_SPEED_PROCESS_INTERVAL_NUM == 0:
            avg_time = (time.time() - self.img_process_speed_start_time) / len(self.img_process_speed_dict)
            self.MONITOR_LOGGER.info('sum img:{a}, img_process speed in recv:{b}'.format(a=(len(self.img_process_speed_dict)), b=avg_time))


speed_check_inst = SpeedCheck()