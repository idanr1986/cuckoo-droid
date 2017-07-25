# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature


class IBankingMalware(Signature):
    name = "android_maware_iBanking"
    description = "iBanking Malware - Detects if files and strings related to iBanking is available in apk (Detection)"
    severity = 5
    categories = ["android", "banker", "malware"]
    authors = ["idanr1986"]
    minimum = "0.5"
    families = ["iBanking"]

    def check_file(self,pattern):
        for item in self.results["apkinfo"]["files"]:
            if item["name"] == pattern:
                return item

    def run(self):
        indicators = [
            "bot_id",
            "type_password2"
        ]
        try:
            for indicator in indicators:
                subject = self._check_value(pattern=indicator, subject=self.results["strings"])
                if subject:
                    self.add_match(None, 'string', subject)
            subject = self.check_file(pattern="res/drawable-xxhdpi/ok_btn.jpg")
            if subject:
                    self.add_match(None, 'file', subject)
            return self.has_matches()
        except:
            return self.has_matches()

