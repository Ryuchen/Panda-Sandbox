#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-30 17:12
# @Author : ryuchen
# @File : GuestManager.py
# @Desc : We abandon the old agent, only adapt for new guest agent
# ==================================================
import datetime
import io
import json
import logging
import os
import requests
import socket
import time
import xmlrpclib
import zipfile

from cuckoo.common.config import config, parse_options
from cuckoo.common.constants import (
    CUCKOO_GUEST_PORT, CUCKOO_GUEST_INIT, CUCKOO_GUEST_COMPLETED,
    CUCKOO_GUEST_FAILED
)
from cuckoo.common.exceptions import (
    CuckooGuestError, CuckooGuestCriticalTimeout
)
from cuckoo.common.utils import TimeoutServer
from cuckoo.core.database import Database
from cuckoo.misc import cwd

log = logging.getLogger(__name__)
db = Database()


def analyzer_zipfile(platform, monitor):
    """Creates the Zip file that is sent to the Guest."""
    t = time.time()

    zip_data = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_data, "w", zipfile.ZIP_STORED)

    # Select the proper analyzer's folder according to the operating
    # system associated with the current machine.
    root = cwd("analyzer", platform)
    root_len = len(os.path.abspath(root))

    if not os.path.exists(root):
        log.error("No valid analyzer found at path: %s", root)
        raise CuckooGuestError(
            "No valid analyzer found for %s platform!" % platform
        )

    # Walk through everything inside the analyzer's folder and write
    # them to the zip archive.
    for root, dirs, files in os.walk(root):
        archive_root = os.path.abspath(root)[root_len:]
        for name in files:
            path = os.path.join(root, name)
            archive_name = os.path.join(archive_root, name)
            zip_file.write(path, archive_name)

    # Include the chosen monitoring component and any additional files.
    if platform == "windows":
        dirpath = cwd("monitor", monitor)

        # Generally speaking we should no longer be getting symbolic links for
        # "latest" anymore, so in the case of a file; follow it.
        if os.path.isfile(dirpath):
            monitor = os.path.basename(open(dirpath, "rb").read().strip())
            dirpath = cwd("monitor", monitor)

        for name in os.listdir(dirpath):
            zip_file.write(
                os.path.join(dirpath, name), os.path.join("bin", name)
            )

        # Dump compiled "dumpmem" Yara rules for zer0m0n usage.
        zip_file.write(cwd("stuff", "dumpmem.yarac"), "bin/rules.yarac")

    zip_file.close()
    data = zip_data.getvalue()

    if time.time() - t > 10:
        log.warning(
            "It took more than 10 seconds to build the Analyzer Zip for the "
            "Guest. This might be a serious performance penalty. Is your "
            "analyzer/windows/ directory bloated with unnecessary files?"
        )

    return data


class GuestManager(object):
    """This class represents the new Guest Manager. It operates on the new
    Cuckoo Agent which features a more abstract but more feature-rich API."""

    def __init__(self, vmid, ipaddr, platform, task_id, analysis_manager):
        self.vmid = vmid
        self.ipaddr = ipaddr
        self.port = CUCKOO_GUEST_PORT
        self.platform = platform
        self.task_id = task_id
        self.analysis_manager = analysis_manager
        self.timeout = None

        # We maintain the path of the Cuckoo Analyzer on the host.
        self.analyzer_path = None
        self.environ = {}

        self.options = {}

    @property
    def aux(self):
        return self.analysis_manager.aux

    def get(self, method, *args, **kwargs):
        """Simple wrapper around requests.get()."""
        do_raise = kwargs.pop("do_raise", True)
        url = "http://%s:%s%s" % (self.ipaddr, self.port, method)
        session = requests.Session()
        session.trust_env = False
        session.proxies = None

        try:
            r = session.get(url, *args, **kwargs)
        except requests.ConnectionError:
            raise CuckooGuestError(
                "Cuckoo Agent failed without error status, please try "
                "upgrading to the latest version of agent.py (>= 0.8) and "
                "notify us if the issue persists."
            )

        do_raise and r.raise_for_status()
        return r

    def post(self, method, *args, **kwargs):
        """Simple wrapper around requests.post()."""
        url = "http://%s:%s%s" % (self.ipaddr, self.port, method)
        session = requests.Session()
        session.trust_env = False
        session.proxies = None

        try:
            r = session.post(url, *args, **kwargs)
        except requests.ConnectionError:
            raise CuckooGuestError(
                "Cuckoo Agent failed without error status, please try "
                "upgrading to the latest version of agent.py (>= 0.8) and "
                "notify us if the issue persists."
            )

        r.raise_for_status()
        return r

    def wait_available(self):
        """Wait until the Virtual Machine is available for usage."""
        end = time.time() + self.timeout

        while db.guest_get_status(self.task_id) == "starting":
            try:
                socket.create_connection((self.ipaddr, self.port), 1).close()
                break
            except socket.timeout:
                log.debug("%s: not ready yet", self.vmid)
            except socket.error:
                log.debug("%s: not ready yet", self.vmid)
                time.sleep(1)

            if time.time() > end:
                raise CuckooGuestCriticalTimeout(
                    "Machine %s: the guest initialization hit the critical "
                    "timeout, analysis aborted." % self.vmid
                )

    def query_environ(self):
        """Query the environment of the Agent in the Virtual Machine."""
        self.environ = self.get("/environ").json()["environ"]

    def determine_analyzer_path(self):
        """Determine the path of the analyzer. Basically creating a temporary
        directory in the systemdrive, i.e., C:\\."""
        systemdrive = self.determine_system_drive()

        options = parse_options(self.options["options"])
        if options.get("analpath"):
            dirpath = systemdrive + options["analpath"]
            r = self.post("/mkdir", data={"dirpath": dirpath})
            self.analyzer_path = dirpath
        else:
            r = self.post("/mkdtemp", data={"dirpath": systemdrive})
            self.analyzer_path = r.json()["dirpath"]

    def determine_system_drive(self):
        if self.platform == "windows":
            return "%s/" % self.environ["SYSTEMDRIVE"]
        return "/"

    def determine_temp_path(self):
        if self.platform == "windows":
            return self.environ["TEMP"]
        return "/tmp"

    def upload_analyzer(self, monitor):
        """Upload the analyzer to the Virtual Machine."""
        zip_data = analyzer_zipfile(self.platform, monitor)

        log.debug(
            "Uploading analyzer to guest (id=%s, ip=%s, monitor=%s, size=%d)",
            self.vmid, self.ipaddr, monitor, len(zip_data)
        )

        self.determine_analyzer_path()
        data = {
            "dirpath": self.analyzer_path,
        }
        self.post("/extract", files={"zipfile": zip_data}, data=data)

    def add_config(self, options):
        """Upload the analysis.conf for this task to the Virtual Machine."""
        config = [
            "[analysis]",
        ]
        for key, value in options.items():
            # Encode datetime objects the way xmlrpc encodes them.
            if isinstance(value, datetime.datetime):
                config.append("%s = %s" % (key, value.strftime("%Y%m%dT%H:%M:%S")))
            else:
                config.append("%s = %s" % (key, value))

        data = {
            "filepath": os.path.join(self.analyzer_path, "analysis.conf"),
        }
        self.post("/store", files={"file": "\n".join(config)}, data=data)

    def start_analysis(self, options, monitor):
        """Start the analysis by uploading all required files.
        @param options: the task options
        @param monitor: identifier of the monitor to be used.
        """
        log.info("Starting analysis on guest (id=%s, ip=%s)",
                 self.vmid, self.ipaddr)

        self.options = options
        self.timeout = options["timeout"] + config("cuckoo:timeouts:critical")

        # Wait for the agent to come alive.
        self.wait_available()

        # Could be beautified a bit, but basically we have to perform the
        # same check here as we did in wait_available().
        if db.guest_get_status(self.task_id) != "starting":
            return

        # Check whether this is the new Agent or the old one (by looking at
        # the status code of the index page).
        r = self.get("/", do_raise=False)
        if r.status_code == 501:
            # log.info("Cuckoo 2.0 features a new Agent which is more "
            #          "feature-rich. It is recommended to make new Virtual "
            #          "Machines with the new Agent, but for now falling back "
            #          "to backwards compatibility with the old agent.")
            self.is_old = True
            self.aux.callback("legacy_agent")
            self.old.start_analysis(options, monitor)
            return

        if r.status_code != 200:
            log.critical(
                "While trying to determine the Agent version that your VM is "
                "running we retrieved an unexpected HTTP status code: %s. If "
                "this is a false positive, please report this issue to the "
                "Cuckoo Developers. HTTP response headers: %s",
                r.status_code, json.dumps(dict(r.headers)),
            )
            db.guest_set_status(self.task_id, "failed")
            return

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
            db.guest_set_status(self.task_id, "failed")
            return

        log.info("Guest is running Cuckoo Agent %s (id=%s, ip=%s)",
                 version, self.vmid, self.ipaddr)

        # Pin the Agent to our IP address so that it is not accessible by
        # other Virtual Machines etc.
        if "pinning" in features:
            self.get("/pinning")

        # Obtain the environment variables.
        self.query_environ()

        # Upload the analyzer.
        self.upload_analyzer(monitor)

        # Pass along the analysis.conf file.
        self.add_config(options)

        # Allow Auxiliary modules to prepare the Guest.
        self.aux.callback("prepare_guest")

        # If the target is a file, upload it to the guest.
        if options["category"] == "file" or options["category"] == "archive":
            data = {
                "filepath": os.path.join(
                    self.determine_temp_path(), options["file_name"]
                ),
            }
            files = {
                "file": ("sample.bin", open(options["target"], "rb")),
            }
            self.post("/store", files=files, data=data)

        if "execpy" in features:
            data = {
                "filepath": "%s/analyzer.py" % self.analyzer_path,
                "async": "yes",
                "cwd": self.analyzer_path,
            }
            self.post("/execpy", data=data)
        else:
            # Execute the analyzer that we just uploaded.
            data = {
                "command": "C:\\Python27\\pythonw.exe %s\\analyzer.py" % self.analyzer_path,
                "async": "yes",
                "cwd": self.analyzer_path,
            }
            self.post("/execute", data=data)

    def wait_for_completion(self):
        if self.is_old:
            self.old.wait_for_completion()
            return

        end = time.time() + self.timeout

        while db.guest_get_status(self.task_id) == "running":
            log.debug("%s: analysis still processing", self.vmid)

            time.sleep(1)

            # If the analysis hits the critical timeout, just return straight
            # away and try to recover the analysis results from the guest.
            if time.time() > end:
                log.info("%s: end of analysis reached!", self.vmid)
                return

            try:
                status = self.get("/status", timeout=5).json()
            except Exception as e:
                log.info("Virtual Machine /status failed (%r)", e)
                # this might fail due to timeouts or just temporary network issues
                # thus we don't want to abort the analysis just yet and wait for things to
                # recover
                continue

            if status["status"] == "complete":
                log.info("%s: analysis completed successfully", self.vmid)
                return
            elif status["status"] == "exception":
                log.warning(
                    "%s: analysis caught an exception\n%s",
                    self.vmid, status["description"]
                )
                return

    @property
    def server(self):
        """Currently the Physical machine manager is using GuestManager in
        an incorrect way. This should be fixed up later but for now this
        workaround will do."""
        return self.old.server
