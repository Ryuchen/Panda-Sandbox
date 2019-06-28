#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:59
# @Author : ryuchen
# @File : operation.py
# @Desc :
# ==================================================


class PandaOperationalError(Exception):
    """Panda operation error."""


class PandaMachineError(PandaOperationalError):
    """Error managing analysis machine."""


class PandaMissingMachineError(PandaMachineError):
    """No such machine exists."""


class PandaMachineSnapshotError(PandaMachineError):
    """Error restoring snapshot from machine."""


class PandaAnalysisError(PandaOperationalError):
    """Error during analysis."""


class PandaProcessingError(PandaOperationalError):
    """Error in processor module."""


class PandaReportError(PandaOperationalError):
    """Error in reporting module."""


class PandaGuestError(PandaOperationalError):
    """Panda guest agent error."""


class PandaGuestCriticalTimeout(PandaGuestError):
    """The Host was unable to connect to the Guest."""


class PandaResultError(PandaOperationalError):
    """Panda result server error."""


class PandaDisableModule(PandaOperationalError):
    """Exception for disabling a module dynamically."""


class PandaFeedbackError(PandaOperationalError):
    """Error in feedback module."""


class PandaApiError(PandaOperationalError):
    """Error during API usage."""
