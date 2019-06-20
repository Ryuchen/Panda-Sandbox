#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 14:17
# @Author : ryuchen
# @File : main.py.py
# @Desc :
# ==================================================
from lib.implements.flask_app import FlaskApplication
from lib.implements.celery_app import CeleryApplication

FlaskApplication().start()
CeleryApplication().start()
