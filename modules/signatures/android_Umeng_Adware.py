# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidDynamicCode(Signature):
    name = "android_Umeng_Adware"
    description = "Umeng Adware (Detection)"
    severity = 3
    categories = ["android"]
    authors = ["ofercas"]
    minimum = "0.5"



    def run(self):
        indicators = [
            "alog.umeng.com",
            "oc.umeng.com"
    ]
        try:
            if "dns" in self.results["network"]:
                for query in self.results["network"]["dns"]:
                    for indicator in indicators:
                        if indicator in query["request"]:
                            self.add_match(None, "dns", indicator)

            return self.has_matches()


        except:
            return self.has_matches()

