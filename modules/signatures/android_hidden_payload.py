# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
import os

from lib.cuckoo.common.abstracts import Signature




class Hidden_Payload(Signature):
    name = "android_hidden_payload"
    description = "Hidden Payload Found (Static)"
    severity = 4
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            for payload in self.results["apkinfo"]["hidden_payload"]:
                self.add_match(None,payload["name"], payload)
            return self.has_matches()

        except:
            return False
