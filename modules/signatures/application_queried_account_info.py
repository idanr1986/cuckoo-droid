# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidAccountInfo(Signature):
    name = "application_queried_account_info"
    description = "Application Queried Account Information (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["Check Point Software Technologies LTD"]
    minimum = "0.5"

    def run(self):
        try:
            if "getAccounts" in self.results["droidmon"]["data_leak"]:
                return True
            else:
                return False
        except:
            return False
