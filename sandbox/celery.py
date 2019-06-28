#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 10:23
# @Author : ryuchen
# @File : celery.py
# @Desc :
# ==================================================
import logging

from celery import Celery
from lib.settings import Settings

log = logging.getLogger(__name__)

# Once, as part of application setup, during deploy/migrations:
# We need to setup the global default settings
settings = Settings.loading_settings()

# Initialise the celery redis connection
redis_host = settings.get("connection", {}).get("redis", {}).get("host", "localhost")
redis_port = settings.get("connection", {}).get("redis", {}).get("port", 6379)

app = Celery(
    main='Panda-Sandbox',
    broker='redis://{0}:{1}/93'.format(redis_host, redis_port),
    backend='redis://{0}:{1}/77'.format(redis_host, redis_port)
)

# Optional configuration, see the application user guide.
# See more: https://docs.celeryproject.org/en/latest/userguide/configuration.html
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=['json'],
    result_expires=3600,
    worker_concurrency=1,
    worker_max_tasks_per_child=1,
    worker_prefetch_multiplier=1,
)


@app.on_configure.connect
def setup_initialise_check(sender, **kwargs):
    print("app setup_initialise_check signals received")


@app.on_after_configure.connect
def setup_backend_service(sender, **kwargs):
    print("app setup_backend_service signals received")


@app.on_after_finalize.connect
def setup_finalize_check(sender, **kwargs):
    print("app setup_finalize_check signals received")



