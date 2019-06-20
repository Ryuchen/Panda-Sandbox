#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 14:27
# @Author : ryuchen
# @File : router.py
# @Desc :
# ==================================================

from apps.apis.api import app


@app.route('/')
def hello_world():
    return 'Hello, World!'
