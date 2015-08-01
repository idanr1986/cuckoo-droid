# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class ApplicationUsesLocation(Signature):
    name = "application_uses_location"
    description = "Application Uses Location (Dynamic)"
    severity = 5
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "location" in self.results["droidmon"]["data_leak"]:
                return True
            else:
                return False
        except:
            return False
