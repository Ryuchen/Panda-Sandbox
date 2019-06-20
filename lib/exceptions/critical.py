#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:59
# @Author : ryuchen
# @File : critical.py
# @Desc :
# ==================================================


class CuckooCriticalError(Exception):
    """Cuckoo struggle in a critical error."""


class CuckooStartupError(CuckooCriticalError):
    """Error starting up Cuckoo."""


class CuckooDatabaseError(CuckooCriticalError):
    """Cuckoo database error."""


class CuckooDependencyError(CuckooCriticalError):
    """Missing dependency error."""


class CuckooConfigurationError(CuckooCriticalError):
    """Invalid configuration error."""
