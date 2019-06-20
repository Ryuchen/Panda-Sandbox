#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 10:23
# @Author : ryuchen
# @File : celery.py
# @Desc :
# ==================================================

import os
import sys
import logging
import datetime
import importlib

from celery import Celery
from celery.signals import task_prerun
from celery.signals import task_success
from celery.signals import task_failure

from common.settings import Settings
from contrib.mysql.base import MysqlBase
from contrib.elastic.indices.host_aggtask import AggTaskLog

log = logging.getLogger(__name__)

# Once, as part of application setup, during deploy/migrations:
# We need to setup the global default settings
setting = Settings()
setting.loading_settings()
settings = setting.get_settings()

# Initialise the celery redis connection
redis_host = settings.get("connection", {}).get("redis", {}).get("host", "localhost")
redis_port = settings.get("connection", {}).get("redis", {}).get("port", 6379)

app = Celery(
    main='deadpool',
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
    try:
        # Initialise database connection
        databases_session_pool = {}
        for _ in settings.get("connection").get("database").get("database"):
            dsn = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?charset=utf8"
            username = settings.get("connection").get("database").get("username")
            password = settings.get("connection").get("database").get("password")
            host = settings.get("connection").get("database").get("host")
            port = settings.get("connection").get("database").get("port")
            db = MysqlBase(dsn.format(username, password, host, port, _))
            databases_session_pool.update({_: db.Session})
        setattr(sender, "databases_session_pool", databases_session_pool)
        log.debug("successes celery app on configure")
    except Exception as e:
        log.error(e)


# When celery after initialise we register our task into the celery.
@app.on_after_configure.connect
def setup_celery_tasks(sender, **kwargs):
    sys.path.append(os.getcwd())
    for task_name, task_option in settings.get("router", {}).items():
        module_path = 'apps.{0}.tasks.{1}'.format(task_option.get("module"), task_name)
        try:
            ip_module = importlib.import_module(module_path)
            ip_module_class = getattr(ip_module, task_option.get("class"))
            ip_module_class.options = task_option.get("options")
            task_instance = ip_module_class()
            sender.register_task(task_instance)
            log.debug("successes celery app on after configure")
        except Exception as e:
            log.error(e)


# When celery start the task, we need to tell it the last time running status.
@task_prerun.connect
def search_agg_task_log(signal, sender, *args, **kwargs):
    # This is to set this time running clock(super precision)
    running_time = datetime.datetime.now().replace(second=0, microsecond=0)
    sender.request.kwargs = {
        "datetime": running_time
    }


@task_success.connect
def insert_agg_task_log(signal, sender, result, *args, **kwargs):
    if result:
        index = '{0}-{1}'.format(
            AggTaskLog.Index.name,
            datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        for _ in result:
            agg_task_log = AggTaskLog(
                task_name=sender.name,
                rule_name=_.get("rule_name"),
                start_time=_.get("start_time"),
                end_time=_.get("end_time"),
                risk_host_cnt=_.get("risk_host_cnt")
            )
            agg_task_log.save(index=index)


@task_failure.connect
def record_agg_task_log(signal, sender, **kwargs):
    # Get last running time
    log.info("signals received: %s" % sender.name)
