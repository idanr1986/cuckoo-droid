# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidComponentEnabledSetting(Signature):
    name = "application_setComponentEnabledSetting"
    description = "Application Set Component Enabled Setting (Dynamic)"
    severity = 4
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "ComponentEnabledSetting" in self.results["droidmon"]:
                for component in self.results["droidmon"]["ComponentEnabledSetting"]:
                    self.add_match(None, "Dynamic API Call", component)
            return self.has_matches()
        except:
            return False
