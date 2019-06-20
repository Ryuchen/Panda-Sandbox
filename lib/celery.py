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
from celery.signals import task_prerun
from celery.signals import task_success
from celery.signals import task_failure

from lib.common.settings import Settings

log = logging.getLogger(__name__)

# Once, as part of application setup, during deploy/migrations:
# We need to setup the global default settings
settings = Settings.loading_settings()

# Initialise the celery redis connection
redis_host = settings.get("connection", {}).get("redis", {}).get("host", "localhost")
redis_port = settings.get("connection", {}).get("redis", {}).get("port", 6379)

app = Celery(
    main='Panda-Sandbox',
    broker='redis://{0}:{1}/3'.format(redis_host, redis_port),
    backend='redis://{0}:{1}/4'.format(redis_host, redis_port)
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


# When celery start to initialise need to load multiple database session to context.
@app.on_configure.connect
def setup_initialise(sender, **kwargs):
    print("app initialise signals received: %s" % sender.name)


# When celery after initialise we register our task into the celery.
@app.on_after_configure.connect
def setup_celery_tasks(sender, **kwargs):
    print("app after configure signals received: %s" % sender.name)


# When celery start the task, we need to tell it the last time running status.
@task_prerun.connect
def search_agg_task_log(signal, sender, *args, **kwargs):
    print("task prerun signals received: %s" % sender.name)


@task_success.connect
def insert_agg_task_log(signal, sender, result, *args, **kwargs):
    print("task success signals received: %s" % sender.name)


@task_failure.connect
def record_agg_task_log(signal, sender, **kwargs):
    # Get last running time
    print("task failure signals received: %s" % sender.name)
