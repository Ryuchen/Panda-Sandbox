#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========================================================
# @Author: Ryuchen
# @Time: 2019/12/05-13:41
# @Site: https://ryuchen.github.io
# @Contact: chenhaom1993@hotmail.com
# @Copyright: Copyright (C) 2019-2020 Panda-Sandbox.
# ========================================================
"""
Using this unittest to test with settings.py function
The function below was test with error configuration to change into correct
"""
import os
import sys
import logging

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.settings import Settings

log = logging.getLogger(__name__)


class SettingUnitTest(object):
    def __init__(self):
        # Once, as part of application setup, during deploy/migrations:
        # We need to setup the global default settings
        self.settings = Settings.loading_settings()


if __name__ == '__main__':
    setting_unit_test = SettingUnitTest()
    print(setting_unit_test.settings.variable.hostname)
    print(setting_unit_test.settings.advanced.mode)
    print(setting_unit_test.settings.advanced.master)
