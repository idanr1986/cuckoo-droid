# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidReflectionCode(Signature):
    name = "android_reflection_code"
    description = "Application Uses Reflection Methods (Static)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if self.results["apkinfo"]["static_method_calls"]["is_reflection_code"] is True:
                for call in self.results["apkinfo"]["static_method_calls"]["reflection_method_calls"]:
                    self.add_match(None,"Static API Call", call)
                return True
            else:
                return False
        except:
            return False