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

_current_dir = os.path.abspath(os.path.dirname(__file__))
CONFIG_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "config"))


class Settings:
    """
    This function to protect the custom setting config does not influence the program successfully start up.
    """

    default_path = os.path.join(CONFIG_ROOT, "config.yaml")
    default_config = {
        "version": "v1.0.0-alpha",
        "hostname": "default",
        "hostaddr": "192.168.10.1",
        "connection": {
            "redis": {
                "host": "127.0.0.1",
                "port": 6379,
                "timeout": 60
            },
            "database": {
                "host": "127.0.0.1",
                "port": 3306,
                "dbname": "panda",
                "username": "root",
                "password": "it's so secret",
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
        if os.path.exists(cls.default_path):
            with open(cls.default_path) as default_config:
                cls.settings = yaml.load(default_config, Loader=yaml.SafeLoader)

        if cls.default_config:
            cls.settings.update(cls.default_config)

        cls.settings["hostname"] = socket.gethostname()

        return cls.settings
