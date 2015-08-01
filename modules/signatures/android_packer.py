# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidDynamicCode(Signature):
    name = "android_packer"
    description = "Application Uses Packer (Static)"
    severity = 3
    categories = ["android"]
    authors = ["ofercas"]
    minimum = "0.5"



    def run(self):
        files = {
            "APKProtect":["libAPKProtect.so","libbaiduprotect.so"],
            "Bangcle":["libapkprotect2.so", "assets/bangcleplugin/container.dex", "bangcleclasses.jar", "libsecexe.so", "bangcle_classes.jar", "libsecmain"],
            "LIAPP":["/LIAPPEgg"],
            "Qihoo":["libprotectClass.so"],
            "NQ Shield":["libNSaferOnly.so", "nqshield", "nqshell"],
            "Tencent":["libshell.so"],
            "Ijiami":["ijiami.dat"],
            "Naga":["libddog.so"],
            "Alibaba":["libmobisec.so"]
        }

        try:

            for file in self.results["apkinfo"]["files"]:
                for key in files:
                    for indicator in files[key]:
                        if indicator in file["name"]:
                            self.add_match(None, "Packer: " + key, "File: "+file["name"])
                            AndroidDynamicCode.description = "Application Uses "+key+" Packer (Static)"

            return self.has_matches()

        except:
            return self.has_matches()

