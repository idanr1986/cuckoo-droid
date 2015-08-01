# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidCamera(Signature):
    name = "application_using_the_camera"
    description = "Application Using The Camera (Dynamic)"
    severity = 2
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "camera" in self.results["droidmon"]["events"]:
                return True
            else:
                return False
        except:
            return False
