# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidDynamicCode(Signature):
    name = "android_dynamic_code"
    description = "Application Uses Dynamic Loading Methods (Static)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if self.results["apkinfo"]["static_method_calls"]["is_dynamic_code"] is True:
                for call in self.results["apkinfo"]["static_method_calls"]["dynamic_method_calls"]:
                    self.add_match(None,"Static API Call", call)
                return True
            else:
                return False
        except:
            return False
