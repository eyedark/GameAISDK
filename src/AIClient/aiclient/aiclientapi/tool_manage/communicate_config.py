# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/aiclient/aiclientapi/tool_manage/communicate_config.py
# Compiled at: 2020-12-29 09:25:42
# Size of source mod 2**32: 598 bytes
INTEGER_LENGTH = 4
IS_TEST_SPEED = True
GAME_STATE = 0
AI_SERVICE_ABNORMAL = -1
AI_SERVICE_READY = 0
RESOURCE_APPLY_FAILURE = -2
NETWORK_ABNORMAL = -1
NETWORK_CONNECTTING = 0
RESOURCE_APPLY_SUCCESS = 1
test_id = '0'
game_id = 0
game_version = '0'
runtimes = 0
is_ai_service_state_ok = True
msg_ai_service_state_desc = {0: 'processes ok', 
 1: 'agent process exit', 
 2: 'reg process exit', 
 4: 'ui process exit'}
ui_action_on = True
send_frame = True
terminate = False