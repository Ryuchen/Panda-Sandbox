#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:13
# @Author : ryuchen
# @File : start.py
# @Desc :
# ==================================================

from lib.implements.flask_app import FlaskApplication
from lib.implements.celery_app import CeleryApplication

FlaskApplication().start()
CeleryApplication().start()
