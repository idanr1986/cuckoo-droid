# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidPhoneNumber(Signature):
    name = "application_fingerprint"
    description = "Application Fingerprint (Dynamic)"
    severity = 1
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "fingerprint" in self.results["droidmon"]:
                for fingerprint in self.results["droidmon"]["fingerprint"]:
                    self.add_match(None, "Dynamic API Call", fingerprint+"()")
        except:
            pass

        finally:
            return self.has_matches()