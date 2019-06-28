#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:59
# @Author : ryuchen
# @File : critical.py
# @Desc :
# ==================================================


class PandaCriticalError(Exception):
    """Panda struggle in a critical error."""


class PandaStartupError(PandaCriticalError):
    """Error starting up Panda."""


class PandaDatabaseError(PandaCriticalError):
    """Panda database error."""


class PandaDependencyError(PandaCriticalError):
    """Missing dependency error."""


class PandaConfigurationError(PandaCriticalError):
    """Invalid configuration error."""
