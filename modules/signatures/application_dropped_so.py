# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature


class ApplicationDroppedSo(Signature):
    name = "application_dropped_so"
    description = "Application Dropped Shared Object File (Dynamic)"
    severity = 1
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "dropped_so" in self.results["droidmon"]:
                for so in self.results["droidmon"]["dropped_so"]:
                    self.add_match(None, "File", so)
            return self.has_matches()
        except:
            return False