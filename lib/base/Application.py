#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 14:33
# @Author : ryuchen
# @File : Application.py
# @Desc :
# ==================================================

from multiprocessing import Process


class Application(Process):

    def __init__(self):
        super(Application, self).__init__()
