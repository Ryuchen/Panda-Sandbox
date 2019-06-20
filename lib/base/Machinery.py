#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-31 18:06
# @Author : ryuchen
# @File : Machinery.py
# @Desc :
# ==================================================
import time
import logging

from lib.common import config
from lib.common.exceptions import CuckooCriticalError
from lib.common.exceptions import CuckooMachineError
from lib.misc import cwd

log = logging.getLogger(__name__)


class Machinery(object):
    """Base abstract class for machinery modules."""

    # Default label used in machinery configuration file to supply virtual
    # machine name/label/vmx path. Override it if you dubbed it in another
    # way.
    LABEL = "label"

    def __init__(self):
        self.options = None
        self.remote_control = False

    @classmethod
    def init_once(cls):
        pass

    @staticmethod
    def pcap_path(task_id):
        """Returns the .pcap path for this task id."""
        return cwd("storage", "analyses", "%s" % task_id, "dump.pcap")

    def set_options(self, options):
        """Set machine manager options.
        @param options: machine manager options dict.
        """
        self.options = options

    def initialize(self, module_name):
        """Read, load, and verify machines configuration.
        @param module_name: module name.
        """
        # Load.
        self._initialize(module_name)

        # Run initialization checks.
        self._initialize_check()

    def _initialize(self, module_name):
        """Read configuration.
        @param module_name: module name.
        """
        machinery = self.options.get(module_name)
        for vmname in machinery["machines"]:
            options = self.options.get(vmname)

            # If configured, use specific network interface for this
            # machine, else use the default value.
            if options.get("interface"):
                interface = options["interface"]
            else:
                interface = machinery.get("interface")

            if options.get("resultserver_ip"):
                ip = options["resultserver_ip"]
            else:
                ip = config("cuckoo:resultserver:ip")

            if options.get("resultserver_port"):
                port = options["resultserver_port"]
            else:
                # The ResultServer port might have been dynamically changed,
                # get it from the ResultServer singleton. Also avoid import
                # recursion issues by importing ResultServer here.
                from cuckoo.core.resultserver import ResultServer
                port = ResultServer().port

            self.db.add_machine(
                name=vmname,
                label=options[self.LABEL],
                ip=options.ip,
                platform=options.platform,
                options=options.get("options", ""),
                tags=options.tags,
                interface=interface,
                snapshot=options.snapshot,
                resultserver_ip=ip,
                resultserver_port=port
            )

    def _initialize_check(self):
        """Runs checks against virtualization software when a machine manager
        is initialized.
        @note: in machine manager modules you may override or superclass
               his method.
        @raise CuckooMachineError: if a misconfiguration or a unkown vm state
                                   is found.
        """
        try:
            configured_vms = self._list()
        except NotImplementedError:
            return

        for machine in self.machines():
            # If this machine is already in the "correct" state, then we
            # go on to the next machine.
            if machine.label in configured_vms and \
                    self._status(machine.label) in [self.POWEROFF, self.ABORTED]:
                continue

            # This machine is currently not in its correct state, we're going
            # to try to shut it down. If that works, then the machine is fine.
            try:
                self.stop(machine.label)
            except CuckooMachineError as e:
                raise CuckooCriticalError(
                    "Please update your configuration. Unable to shut '%s' "
                    "down or find the machine in its proper state: %s" %
                    (machine.label, e)
                )

        if not config("cuckoo:timeouts:vm_state"):
            raise CuckooCriticalError(
                "Virtual machine state change timeout has not been set "
                "properly, please update it to be non-null."
            )

    def machines(self):
        """List virtual machines.
        @return: virtual machines list
        """
        return self.db.list_machines()

    def availables(self):
        """How many machines are free.
        @return: free machines count.
        """
        return self.db.count_machines_available()

    def acquire(self, machine_id=None, platform=None, tags=None):
        """Acquire a machine to start analysis.
        @param machine_id: machine ID.
        @param platform: machine platform.
        @param tags: machine tags
        @return: machine or None.
        """
        if machine_id:
            return self.db.lock_machine(label=machine_id)
        elif platform:
            return self.db.lock_machine(platform=platform, tags=tags)
        else:
            return self.db.lock_machine(tags=tags)

    def release(self, label=None):
        """Release a machine.
        @param label: machine name.
        """
        self.db.unlock_machine(label)

    def running(self):
        """Returns running virtual machines.
        @return: running virtual machines list.
        """
        return self.db.list_machines(locked=True)

    def shutdown(self):
        """Shutdown the machine manager. Kills all alive machines.
        @raise CuckooMachineError: if unable to stop machine.
        """
        if len(self.running()) > 0:
            log.info("Still %s guests alive. Shutting down...",
                     len(self.running()))
            for machine in self.running():
                try:
                    self.stop(machine.label)
                except CuckooMachineError as e:
                    log.warning("Unable to shutdown machine %s, please check "
                                "manually. Error: %s", machine.label, e)

    def set_status(self, label, status):
        """Set status for a virtual machine.
        @param label: virtual machine label
        @param status: new virtual machine status
        """
        self.db.set_machine_status(label, status)

    def start(self, label, task):
        """Start a machine.
        @param label: machine name.
        @param task: task object.
        @raise NotImplementedError: this method is abstract.
        """
        raise NotImplementedError

    def stop(self, label=None):
        """Stop a machine.
        @param label: machine name.
        @raise NotImplementedError: this method is abstract.
        """
        raise NotImplementedError

    def _list(self):
        """Lists virtual machines configured.
        @raise NotImplementedError: this method is abstract.
        """
        raise NotImplementedError

    def dump_memory(self, label, path):
        """Takes a memory dump of a machine.
        @param path: path to where to store the memory dump.
        """
        raise NotImplementedError

    def enable_remote_control(self, label):
        """Enable remote control interface (RDP/VNC/SSH).
        @param label: machine name.
        @return: None
        """
        raise NotImplementedError

    def disable_remote_control(self, label):
        """Disable remote control interface (RDP/VNC/SSH).
        @param label: machine name.
        @return: None
        """
        raise NotImplementedError

    def get_remote_control_params(self, label):
        """Return connection details for remote control.
        @param label: machine name.
        @return: dict with keys: protocol, host, port
        """
        raise NotImplementedError

    def _wait_status(self, label, *states):
        """Waits for a vm status.
        @param label: virtual machine name.
        @param state: virtual machine status, accepts multiple states as list.
        @raise CuckooMachineError: if default waiting timeout expire.
        """
        # This block was originally suggested by Loic Jaquemet.
        waitme = 0
        try:
            current = self._status(label)
        except NameError:
            return

        while current not in states:
            log.debug("Waiting %i cuckooseconds for machine %s to switch "
                      "to status %s", waitme, label, states)
            if waitme > config("cuckoo:timeouts:vm_state"):
                raise CuckooMachineError(
                    "Timeout hit while for machine %s to change status" % label
                )

            time.sleep(1)
            waitme += 1
            current = self._status(label)