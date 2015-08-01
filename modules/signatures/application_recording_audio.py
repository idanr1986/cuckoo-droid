# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidAudio(Signature):
    name = "application_recording_audio"
    description = "Application Recording Audio (Dynamic)"
    severity = 4
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "mediaRecorder" in self.results["droidmon"]["events"]:
                return True
            else:
                return False
        except:
            return False
