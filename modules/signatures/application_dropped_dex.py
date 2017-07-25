# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature


class ApplicationDroppedDex(Signature):
    name = "application_dropped_dex"
    description = "Application Dropped Dex File (Dynamic)"
    severity = 1
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "dropped_dex" in self.results["droidmon"]:
                for dex in self.results["droidmon"]["dropped_dex"]:
                    self.add_match(None, "File", dex)
            return self.has_matches()
        except:
            return False
