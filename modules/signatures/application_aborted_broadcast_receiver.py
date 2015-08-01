# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidAbortBroadcast(Signature):
    name = "application_aborted_broadcast_receiver"
    description = "Application Aborted Broadcast Receiver (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "abortBroadcast" in self.results["droidmon"]["events"]:
                return True
            else:
                return False
        except:
            return False
