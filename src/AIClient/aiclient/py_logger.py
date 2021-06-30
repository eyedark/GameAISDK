# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi\aiclient\py_logger.py
# Compiled at: 2021-02-23 16:10:42
# Size of source mod 2**32: 725 bytes
import os, logging, logging.config, shutil, json
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT_DIR, 'log')
LOG_CONFIG_FILE = os.path.join(ROOT_DIR, 'aiclient', 'cfg', 'logging.json')

def setup_logging():
    try:
        if os.path.exists(LOG_DIR):
            shutil.rmtree(LOG_DIR)
        os.makedirs(LOG_DIR, exist_ok=True)
    except Exception:
        pass

    if os.path.exists(LOG_CONFIG_FILE):
        with open(LOG_CONFIG_FILE, 'rt') as (f):
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        raise Exception('LOG_CONFIG_FILE does not exist')