# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidUsingReflection(Signature):
    name = "application_reflection"
    description = "Application Uses Reflection (Dynamic)"
    severity = 4
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if len(self.results["droidmon"]["reflection_calls"]) > 0:
                for call in self.results["droidmon"]["reflection_calls"]:
                    self.add_match(None, "Dynamic API Call", call)
                return True
            else:
                return False
        except:
            return False

