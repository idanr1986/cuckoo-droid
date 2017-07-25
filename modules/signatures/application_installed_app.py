# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidInstalledApps(Signature):
    name = "application_installed_app"
    description = "Application installed App (Dynamic)"
    severity = 5
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "android/app/ApplicationPackageManager->installPackage" in self.results["droidmon"]:
                return True
            elif "Package Installer" in self.results["debug"]["log"]:
                return True
            else:
                return False
        except:
            return False
