# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature


class ApplicationDroppedFiles(Signature):
    name = "application_dropped_files"
    description = "Application Dropped Files (Dynamic)"
    severity = 1
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "dropped" in self.results:
                for file in self.results["dropped"]:
                    self.add_match(None, file["name"], file)
            return self.has_matches()
        except:
            return False
