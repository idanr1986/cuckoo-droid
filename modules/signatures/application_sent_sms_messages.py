# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidSMS(Signature):
    name = "application_sent_sms_messages"
    description = "Application Sending SMS messages (Dynamic)"
    severity = 3
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "sms" in self.results["droidmon"]:
                for sms in self.results["droidmon"]["sms"]:
                    self.add_match(None,sms["dest_number"], sms["content"])
            return self.has_matches()
        except:
            return False
