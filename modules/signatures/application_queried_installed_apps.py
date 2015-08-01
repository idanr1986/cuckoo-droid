# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidAppInfo(Signature):
    name = "application_queried_installed_apps"
    description = "Application Queried Installed Apps (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "getInstalledPackages" in self.results["droidmon"]["data_leak"]:
                self.add_match(None, "Dynamic API Call", "getInstalledPackages()")
        except:
            pass

        finally:
            return self.has_matches()
