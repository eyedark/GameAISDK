# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ./phone_aiclientapi\demo.py
# Compiled at: 2020-12-29 14:14:17
# Size of source mod 2**32: 3075 bytes
import os, sys, signal, time
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, 'log')
sys.path.append(ROOT_DIR)
from tools.resource_apply import ResourceApply
from aiclient.start_service import ActionExecute
from aiclient.py_logger import setup_logging
from aiclient.aiclientapi.tool_manage import communicate_config as com_config
pause_flag = False

class Main(object):

    def __init__(self):
        setup_logging()
        self.action_execute_inst = ActionExecute()

    def init(self):
        return self.action_execute_inst.init()

    def exit_adb(self):
        if sys.platform.startswith('linux'):
            time.sleep(5)
            cmd_str = "ps -ef|grep 'adb -s' |grep -v grep |awk '{print $2}'|xargs kill -9"
            os.system(cmd_str)

    def finish(self):
        self.action_execute_inst.finish()
        self.exit_adb()

    def run(self):
        self.action_execute_inst.run()

    def restart_ai(self):
        self.action_execute_inst.restart_ai()

    def start_game(self):
        self.action_execute_inst.start_game()

    def pause_ai(self):
        self.action_execute_inst.pause_ai()

    def restore_ai(self):
        self.action_execute_inst.restore_ai()

    def stop_ai(self):
        self.action_execute_inst.stop_ai()

    def add_signal(self):

        def exit_aiclient(sig_num, frame):
            print('begin to stop aiclient......')
            self.finish()
            exit(1)

        def restart_ai(siga_num, frame):
            self.restart_ai()
            self.start_game()

        def pause_ai(sig_num, frame):
            global pause_flag
            if not pause_flag:
                self.pause_ai()
                pause_flag = True
            else:
                self.restore_ai()
                pause_flag = False

        if sys.platform.startswith('win'):
            pass
        elif sys.platform.startswith('linux'):
            signal.signal(signal.SIGUSR1, exit_aiclient)
            signal.signal(signal.SIGUSR2, pause_ai)


def set_com_config():
    com_config.terminate = False
    com_config.test_id = '0'
    com_config.game_id = 0
    com_config.game_version = '0'
    com_config.runtimes = 0


def start_ai():
    set_com_config()
    main_inst = Main()
    try:
        if main_inst.init():
            main_inst.add_signal()
            main_inst.run()
        main_inst.finish()
    except KeyboardInterrupt:
        print('KeyboardInterrupt .......................')
        main_inst.finish()


def resource_pre_apply():
    resource_apply_main_inst = ResourceApply()
    ret, error_str = resource_apply_main_inst.init()
    if not ret:
        return False
    else:
        resource_apply_main_inst.run()
        return True


if __name__ == '__main__':
    start_ai()