#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-30 19:44
# @Author : ryuchen
# @File : constants.py
# @Desc :
# ==================================================
import os

SANDBOX_GUEST_PORT = 8000
SANDBOX_GUEST_INIT = 0x001
SANDBOX_GUEST_RUNNING = 0x002
SANDBOX_GUEST_COMPLETED = 0x003
SANDBOX_GUEST_FAILED = 0x004

SANDBOX_CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SANDBOX_CONFIG_DIR = os.path.normpath(os.path.join(SANDBOX_CURRENT_DIR, "..", "..", "etc"))
SANDBOX_DOC_DIR = os.path.normpath(os.path.join(SANDBOX_CURRENT_DIR, "..", "..", "doc"))

GITHUB_URL = "https://github.com/cuckoosandbox/cuckoo"
ISSUES_PAGE_URL = "https://github.com/cuckoosandbox/cuckoo/issues"
DOCS_URL = "https://cuckoo.sh/docs"


def faq(entry):
    return "%s/faq/index.html#%s" % (DOCS_URL, entry)
