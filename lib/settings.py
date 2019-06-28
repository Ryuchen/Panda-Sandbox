#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-30 19:30
# @Author : ryuchen
# @File : config.py
# @Desc :
# ==================================================
import os
import yaml
import socket

from lib.defines.types import String
from lib.defines.context import SANDBOX_CONFIG_DIR


class Settings:
    """
    This function to protect the custom setting config does not influence the program successfully start up.
    """

    default_path = os.path.join(SANDBOX_CONFIG_DIR, "default.yaml")
    default_config = {
        "version": String(default="v1.0.0-alpha", allow_empty=False),
        "hostname": String(default="default", allow_empty=True),
        "hostaddr": String(default="192.168.93.77", allow_empty=True),
        "connection": {
            "redis": {
                "host": "127.0.0.1",
                "port": 6379,
                "timeout": 60
            },
            "elasticsearch": {
                "host": ["127.0.0.1:9200"],
                "timeout": 60
            }
        }
    }

    settings = {}

    @classmethod
    def loading_settings(cls):
        """
        To merge the settings into the main setting.
        :return:
        """
        def merge_dict(target, source):
            for key, value in source.items():
                if isinstance(value, dict):
                    merge_dict(target.get(key), value)
                else:
                    if value:
                        target.update(source)

        if os.path.exists(cls.default_path):
            with open(cls.default_path) as default_config:
                cls.settings = yaml.load(default_config, Loader=yaml.SafeLoader)

        if cls.default_config:
            merge_dict(cls.settings, cls.default_config)

        cls.settings["hostname"] = socket.gethostname()

        return cls.settings
