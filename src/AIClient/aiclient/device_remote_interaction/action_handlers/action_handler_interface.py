# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\device_remote_interaction\action_handlers\action_handler_interface.py
# Compiled at: 2021-02-23 16:10:41
# Size of source mod 2**32: 237 bytes
from abc import ABCMeta, abstractmethod

class IActionHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def do_action(self, msg):
        raise NotImplementedError()