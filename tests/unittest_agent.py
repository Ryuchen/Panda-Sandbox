#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========================================================
# @Author: Ryuchen
# @Time: 2019/12/05-13:24
# @Site: https://ryuchen.github.io
# @Contact: chenhaom1993@hotmail.com
# @Copyright: Copyright (C) 2019-2020 Panda-Sandbox.
# ========================================================
"""
Using this unittest to test with agent.py function
The function below was assemble from GuestManager

Running this unittest, before you should starting agent on your develop system.
"""
import os
import sys
import json
import logging
import requests

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.exceptions.operation import PandaGuestError

log = logging.getLogger(__name__)


class FakeMachine(object):
    def __init__(self):
        self.label = 'test.vm1'
        self.addr = '127.0.0.1'
        self.port = 8554


class AgentUnitTest(object):
    def __init__(self):
        self.machine = FakeMachine()

    def get(self, method, **kwargs):
        """Simple wrapper around requests.get()."""
        do_raise = kwargs.pop("do_raise", True)
        url = "http://%s:%s%s" % (self.machine.addr, self.machine.port, method)
        session = requests.Session()
        session.trust_env = False
        session.proxies = None

        try:
            r = session.get(url, **kwargs)
        except requests.ConnectionError:
            raise PandaGuestError(
                "Cuckoo Agent failed without error status, please try "
                "upgrading to the latest version of agent.py (>= 0.8) and "
                "notify us if the issue persists."
            )

        do_raise and r.raise_for_status()
        return r

    def post(self, method, *args, **kwargs):
        """Simple wrapper around requests.post()."""
        url = "http://%s:%s%s" % (self.machine.addr, self.machine.port, method)
        session = requests.Session()
        session.trust_env = False
        session.proxies = None

        try:
            r = session.post(url, *args, **kwargs)
        except requests.ConnectionError:
            raise PandaGuestError(
                "Cuckoo Agent failed without error status, please try "
                "upgrading to the latest version of agent.py (>= 0.8) and "
                "notify us if the issue persists."
            )

        r.raise_for_status()
        return r


if __name__ == '__main__':
    # Check whether this is the new Agent or the old one (by looking at
    # the status code of the index page).
    agent_unit_test = AgentUnitTest()
    r = agent_unit_test.get("/", do_raise=False)

    if r.status_code != 200:
        log.critical(
            "While trying to determine the Agent version that your VM is "
            "running we retrieved an unexpected HTTP status code: %s. If "
            "this is a false positive, please report this issue to the "
            "Cuckoo Developers. HTTP response headers: %s",
            r.status_code, json.dumps(dict(r.headers)),
        )
        sys.exit()

    try:
        status = r.json()
        version = status.get("version")
        features = status.get("features", [])
    except:
        log.critical(
            "We were unable to detect either the Old or New Agent in the "
            "Guest VM, are you sure you have set it up correctly? Please "
            "go through the documentation once more and otherwise inform "
            "the Cuckoo Developers of your issue."
        )
        sys.exit()

    log.critical(
        "Guest is running Cuckoo Agent %s (id=%s, ip=%s)",
        version, agent_unit_test.machine.label, agent_unit_test.machine.addr
    )

    # Pin the Agent to our IP address so that it is not accessible by
    # other Virtual Machines etc.
    if "pinning" in features:
        agent_unit_test.get("/pinning")
