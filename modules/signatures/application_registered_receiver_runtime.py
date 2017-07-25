# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidRegisteredReceiver(Signature):
    name = "application_registered_receiver_runtime"
    description = "Application Registered Receiver In Runtime (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "registered_receivers" in self.results["droidmon"]:
                for receiver in self.results["droidmon"]["registered_receivers"]:
                    self.add_match(None,"Receiver", receiver)
            return self.has_matches()
        except:
            return False
