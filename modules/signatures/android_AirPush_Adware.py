# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidDynamicCode(Signature):
    name = "android_AirPush_Adware"
    description = "AirPush Adware SDK (Detection)"
    severity = 3
    categories = ["android"]
    authors = ["ofercas"]
    minimum = "0.5"



    def run(self):
        indicators = [
            "AirpushAdActivity.java",
            "&airpush_url=",
            "getAirpushAppId",
            "Airpush SDK is disabled",
            "api.airpush.com/dialogad/adclick.php",
            "res/layout/airpush_notify.xml"
    ]
        try:

            for string in self.results["strings"]:
                for indicator in indicators:
                    if indicator in string:
                        self.add_match(None, "string", indicator)

            return self.has_matches()

        except:
            return self.has_matches()

