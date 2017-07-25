# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidAccountInfo(Signature):
    name = "application_queried_account_info"
    description = "Application Queried Account Information (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "accounts" in self.results["droidmon"]:
                for account in self.results["droidmon"]["accounts"]:
                    self.add_match(None, "Account", account)

            if "getAccounts" in self.results["droidmon"]["data_leak"]:
                self.add_match(None, "Dynamic API Call", "getAccounts()")
        except:
            pass

        finally:
            return self.has_matches()

