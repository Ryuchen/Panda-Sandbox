#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-05 10:15
# @Author : ryuchen
# @File : unittest_vmware.py
# @Desc :
# ==================================================
"""
Using this unittest to test vmware guest operate function
The function below was assemble from Machinery
"""
import os
import sys
import time
import subprocess

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))


class VMwareUnitTest(object):
    def __init__(self, vmx_path):
        self.mode = "gui"
        self.vmware = {
            "path": "vmrun"
        }
        self.vmx_path = vmx_path

    def check_snapshot(self, snapshot):
        """Checks snapshot existance.
        @param snapshot: snapshot name
        @raise CuckooMachineError: if snapshot not found
        """
        try:
            p = subprocess.Popen([self.vmware.get("path"), "listSnapshots", self.vmx_path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output, _ = p.communicate()
            output = output.decode("utf-8")
        except OSError as e:
            print("Unable to get snapshot list for %s. Reason: %s" % (self.vmx_path, e))
            return False
        else:
            if output:
                output_lines = output.splitlines()
                if snapshot in output_lines:
                    print("Found the snapshots name is %s" % snapshot)
                    return True
                else:
                    print("Doesn't has the correct snapshot setting")
                    return False
            else:
                print("Unable to get snapshot list for %s. No output from `vmrun listSnapshots`" % self.vmx_path)
                return False

    def revert_to_snapshot(self, snapshot):
        """Revert machine to snapshot.
        @param snapshot: snapshot name
        @raise CuckooMachineError: if unable to revert
        """
        print("Revert snapshot for vm %s" % self.vmx_path)
        try:
            if subprocess.call([self.vmware.get("path"), "revertToSnapshot", self.vmx_path, snapshot],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE):
                print("Unable to revert snapshot for machine %s: vmrun exited with error" % self.vmx_path)
        except OSError as e:
            print("Unable to revert snapshot for machine %s: %s" % (self.vmx_path, e))

    def _is_running(self):
        """Checks if virtual machine is running.
        @return: running status
        """
        try:
            p = subprocess.Popen([self.vmware.get("path"), "list"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output, error = p.communicate()
            output = output.decode("utf-8")
        except OSError as e:
            print("Unable to check running status for %s. Reason: %s" % (self.vmx_path, e))
        else:
            if output:
                output_lines = output.splitlines()
                print(output_lines)
                if self.vmx_path in output_lines:
                    print("Found the snapshots name is %s" % self.vmx_path)
                    return True
                else:
                    print("Doesn't has the correct snapshot setting")
                    return False
            else:
                return False

    def start_machine(self, snapshot):

        self.revert_to_snapshot(snapshot)

        print("Starting vm %s" % self.vmx_path)
        try:
            p = subprocess.Popen([self.vmware.get("path"), "start", self.vmx_path, self.mode],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            if self.mode.lower() == "gui":
                output, _ = p.communicate()
                output = output.decode("utf-8")
                if output:
                    print("Unable to start machine %s: %s" % (self.vmx_path, output))
        except OSError as e:
            print("Unable to start machine %s in %s mode: %s" % (self.vmx_path, self.mode.upper(), e))

    def stop_machine(self):
        print("Stopping vm %s" % self.vmx_path)
        if self._is_running():
            try:
                if subprocess.call([self.vmware.get("path"), "stop", self.vmx_path, "hard"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE):
                    print("Error shutting down machine %s" % self.vmx_path)
            except OSError as e:
                print("Error shutting down machine %s: %s" % (self.vmx_path, e))
        else:
            print("Trying to stop an already stopped machine: %s", self.vmx_path)


if __name__ == '__main__':
    vm = VMwareUnitTest(vmx_path="/Users/ryuchen/Virtual Machines.localized/Windows.vmwarevm/Windows.vmx")
    if vm.check_snapshot("snapshot-1"):
        vm.start_machine("snapshot-1")

        time.sleep(10)

        vm.stop_machine()

