# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\plugin\state_notify\state_notify.py
# Compiled at: 2021-02-23 16:10:42
# Size of source mod 2**32: 1903 bytes
import logging

class StateNotify(object):

    def __init__(self):
        self.MAIN_THREAD_LOGGER = logging.getLogger('main_thread')

    def on_start(self, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on start')

    def on_restore(self, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on restore')

    def on_pause(self, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on pause')

    def on_stop(self, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on stop')

    def on_service_over(self, task_id):
        self.MAIN_THREAD_LOGGER.debug('call on on_service_over')

    def on_ai_service_state(self, state, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on ai_service_state')

    def on_resource_apply_state(self, state, description, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('call on resource_apply')

    def on_exception(self, exception_type, description, task_id=None):
        self.MAIN_THREAD_LOGGER.debug('encounter exception, exception_type: {}, err: {}'.format(exception_type, description))