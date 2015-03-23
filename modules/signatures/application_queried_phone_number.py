# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidPhoneNumber(Signature):
    name = "application_queried_phone_number"
    description = "Application Queried Phone Number (Dynamic)"
    severity = 1
    categories = ["android"]
    authors = ["Check Point Software Technologies LTD"]
    minimum = "0.5"

    def run(self):
        try:
            if "getLine1Number" in self.results["droidmon"]["fingerprint"]:
                return True
            else:
                return False
        except:
            return False
