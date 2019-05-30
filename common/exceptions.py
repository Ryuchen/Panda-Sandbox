#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-30 19:57
# @Author : ryuchen
# @File : exceptions.py
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


class CuckooOperationalError(Exception):
    """Cuckoo operation error."""


class CuckooMachineError(CuckooOperationalError):
    """Error managing analysis machine."""


class CuckooMissingMachineError(CuckooMachineError):
    """No such machine exists."""


class CuckooMachineSnapshotError(CuckooMachineError):
    """Error restoring snapshot from machine."""


class CuckooAnalysisError(CuckooOperationalError):
    """Error during analysis."""


class CuckooProcessingError(CuckooOperationalError):
    """Error in processor module."""


class CuckooReportError(CuckooOperationalError):
    """Error in reporting module."""


class CuckooGuestError(CuckooOperationalError):
    """Cuckoo guest agent error."""


class CuckooGuestCriticalTimeout(CuckooGuestError):
    """The Host was unable to connect to the Guest."""


class CuckooResultError(CuckooOperationalError):
    """Cuckoo result server error."""


class CuckooDisableModule(CuckooOperationalError):
    """Exception for disabling a module dynamically."""


class CuckooFeedbackError(CuckooOperationalError):
    """Error in feedback module."""


class CuckooApiError(CuckooOperationalError):
    """Error during API usage."""
