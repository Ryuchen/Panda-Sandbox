#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========================================================
# @Author: Ryuchen
# @Time: 2019/05/30-19:30
# @Site: https://ryuchen.github.io
# @Contact: chenhaom1993@hotmail.com
# @Copyright: Copyright (C) 2019-2020 Panda-Sandbox.
# ========================================================
"""
This to load the custom.yaml and merge into the default.yaml
At same time, to check type of each setting
"""

import os
import json
import yaml

from lib.defines.types import Int
from lib.defines.types import String
from lib.defines.context import SANDBOX_CONFIG_DIR


class Variable(object):
    hostname = String(default="default", allow_empty=True)
    hostaddr = String(default="192.168.0.1", allow_empty=True)


class Advanced(object):
    mode = Int(default=1, allow_empty=False, v_range=(1, 2))


class Settings(object):
    """
    This function to protect the custom setting config does not influence the program successfully start up.
    """
    # The default program settings
    default_path = os.path.join(SANDBOX_CONFIG_DIR, "default.yaml")

    # The finally running settings
    version = String(default="v1.0.0-alpha", allow_empty=False)
    variable = Variable()
    advanced = Advanced()

    @classmethod
    def loading_settings(cls):
        """
        To merge the settings of default.yaml & the settings of custom.yaml into the running setting.
        :return:
        """
        def merge_dict(target, source):
            for key, value in source.items():
                if isinstance(value, dict):
                    merge_dict(target.__dict__[key], value)
                else:
                    setattr(target, key, value)

        if os.path.exists(cls.default_path):
            with open(cls.default_path) as default_config:
                cls.default_setting = yaml.load(default_config, Loader=yaml.SafeLoader)
                print(json.dumps(cls.default_setting, indent=4))

        # # TODO: where to place the custom.yaml file
        # if os.path.exists(cls.default_path):
        #     with open(cls.default_path) as default_config:
        #         cls.settings = yaml.load(default_config, Loader=yaml.SafeLoader)

        if cls.default_setting:
            merge_dict(cls, cls.default_setting)

        return cls
