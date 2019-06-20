#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-30 19:44
# @Author : ryuchen
# @File : constants.py
# @Desc :
# ==================================================
CUCKOO_GUEST_PORT = 8000
CUCKOO_GUEST_INIT = 0x001
CUCKOO_GUEST_RUNNING = 0x002
CUCKOO_GUEST_COMPLETED = 0x003
CUCKOO_GUEST_FAILED = 0x004
GITHUB_URL = "https://github.com/cuckoosandbox/cuckoo"
ISSUES_PAGE_URL = "https://github.com/cuckoosandbox/cuckoo/issues"
DOCS_URL = "https://cuckoo.sh/docs"


def faq(entry):
    return "%s/faq/index.html#%s" % (DOCS_URL, entry)
