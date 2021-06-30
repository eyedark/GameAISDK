# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\aiclientapi\performance_profile\action_check.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 1903 bytes
import logging
from ..tool_manage import communicate_config as com_config
REMCORD_INTERVAL_NUM = 50

class ActionExcuteSpeedCheck(object):

    def __init__(self):
        self.MONITOR_LOGGER = logging.getLogger('monitor')
        self.action_num_dict = {}
        self.action_time_consume_dict = {}
        self.action_sum_num = 0
        self.action_sum_consume_time = 0

    def is_need_record(self):
        return com_config.IS_TEST_SPEED

    def add_action(self, op_code, elapse_time=0):
        if not self.is_need_record():
            return
        else:
            if self.action_num_dict.__contains__(op_code):
                self.action_num_dict[op_code] += 1
                self.action_time_consume_dict[op_code] += elapse_time
            else:
                self.action_num_dict[op_code] = 1
                self.action_time_consume_dict[op_code] = elapse_time
        self.action_sum_num += 1
        self.action_sum_consume_time += elapse_time
        if self.action_sum_num % REMCORD_INTERVAL_NUM == 0:
            self.MONITOR_LOGGER.info('excute action sum num:{}'.format(self.action_sum_num))
            self.MONITOR_LOGGER.info('excute action sum consume time:{}'.format(self.action_sum_consume_time))
            self.MONITOR_LOGGER.info('excute action avg consume time:{}'.format(self.action_sum_consume_time / self.action_sum_num))
            for op_code in self.action_num_dict.keys():
                self.MONITOR_LOGGER.info('op_code:{a}, action num:{b}, sum_consume_time:{c}, avg_consume_time:{d}'.format(a=op_code,
                  b=(self.action_num_dict[op_code]),
                  c=(self.action_time_consume_dict[op_code]),
                  d=(self.action_time_consume_dict[op_code] / self.action_num_dict[op_code])))


action_excute_check_inst = ActionExcuteSpeedCheck()