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
import fcntl
import socket
import struct

_current_dir = os.path.abspath(os.path.dirname(__file__))
CONFIG_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "config"))


class Settings:
    """
    This function to protect the custom setting config does not influence the program successfully start up.
    """

    default_path = os.path.join(CONFIG_ROOT, "config.yaml")
    settings = {
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
    default_config = {}

    def __init__(self):
        pass

    @classmethod
    def loading_default(cls):
        """
        loading the settings of default.
        :return:
        """
        if os.path.exists(cls.default_path):
            with open(cls.default_path) as default_config:
                cls.default_config = yaml.load(default_config, Loader=yaml.SafeLoader)

    @classmethod
    def loading_settings(cls):
        """
        To merge the settings into the main setting.
        :return:
        """
        cls.loading_default()
        if cls.default_config:
            cls.settings.update(cls.default_config)

        cls.settings["hostname"] = socket.gethostname()

        try:
            manage_nic = os.environ["GEYE_MANAGENIC"]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            host_ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', manage_nic[:15]))[20:24])
        except:
            host_ip = cls.settings["host_ip"]

        cls.settings["host_ip"] = host_ip

        return cls
