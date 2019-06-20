#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:30
# @Author : ryuchen
# @File : utils.py
# @Desc :
# ==================================================
import threading


class Singleton(type):
    """Singleton.
    @see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ThreadSingleton(type):
    """Singleton per thread."""
    _instances = threading.local()

    def __call__(cls, *args, **kwargs):
        if not getattr(cls._instances, "instance", None):
            cls._instances.instance = super(ThreadSingleton, cls).__call__(*args, **kwargs)
        return cls._instances.instance
