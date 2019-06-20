#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 14:40
# @Author : ryuchen
# @File : flask_app.py
# @Desc :
# ==================================================
from apps.apis.router import app

from lib.base.Application import Application


class FlaskApplication(Application):

    def __init__(self) -> None:
        super(FlaskApplication, self).__init__()

    def run(self) -> None:
        app.run(port=8000, threaded=True)
