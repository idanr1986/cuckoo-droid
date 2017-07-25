# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidPrivateInfoQuery(Signature):
    name = "application_queried_private_information"
    description = "Application Queried Private Information (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "ContentResolver_queries" in self.results["droidmon"]:
                for query in self.results["droidmon"]["ContentResolver_queries"]:
                    self.add_match(None,"Query", query)
                return self.has_matches()
        except:
            return False
