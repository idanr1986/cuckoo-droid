# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature


class AndroratMalware(Signature):
    name = "android_maware_androrat"
    description = "Androrat Malware - Detects if static class related to Androrat is available in apk (Detection)"
    severity = 5
    categories = ["android", "mrat", "malware"]
    authors = ["idanr1986"]
    minimum = "0.5"
    families = ["androrat"]

    def check_static_methods(self,pattern):
        for item in self.results["apkinfo"]["static_method_calls"]["all_methods"]:
            if "class" in item:
                if item["class"] == pattern:
                    return item

    def run(self):
        indicators = [
            "Lmy/app/client/ProcessCommand"
        ]

        try:
            for indicator in indicators:
                subject = self.check_static_methods(indicator)
                if subject:
                    self.add_match(None, 'Static API Call', subject)
        except:
            pass

        finally:
            return self.has_matches()

