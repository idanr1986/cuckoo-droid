# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidStopProcess(Signature):
    name = "application_stopped_processes"
    description = "Application Stopped Processes (Dynamic)"
    severity = 3
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "killed_process" in self.results["droidmon"]:
                for application_process in self.results["droidmon"]["killed_process"]:
                    self.add_match(None, "Application Process", application_process)
            return self.has_matches()
        except:
            return False
