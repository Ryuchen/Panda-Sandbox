#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 14:40
# @Author : ryuchen
# @File : celery_app.py
# @Desc :
# ==================================================
from celery.bin import worker

from sandbox.celery import app
from lib.base.Application import Application


class CeleryApplication(Application):

    def __init__(self):
        super(CeleryApplication, self).__init__()

    def run(self) -> None:
        application = worker.worker(app=app)

        options = {
            'loglevel': 'INFO',
            'traceback': True,
        }

        application.run(**options)
