# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.


from lib.cuckoo.common.abstracts import Signature

class KnownVirustotal(Signature):
    name = "android_antivirus_virustotal"
    description = "File has been identified by at least one AntiVirus on VirusTotal as malicious (Osint)"
    severity = 2
    categories = ["antivirus"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        AvWhiteList = ["Kingsoft","NANO-Antivirus","F-Prot","McAfee-GW-Edition","McAfee","MicroWorld-eScan","AVG","CAT-QuickHeal","F-Secure","Emsisoft","VIPRE","BitDefender","Fortinet",
                     "Commtouch","TrendMicro-HouseCall", "DrWeb","Comodo", "Kaspersky","AntiVir","Avast","Sophos","Ikarus","GData","ESET-NOD32"]

        try:
            if ("virustotal" in self.results and "scans" in self.results["virustotal"]):
                for key in self.results["virustotal"]["scans"].keys():
                    if(key in AvWhiteList):
                        if(self.results["virustotal"]["scans"][key]["detected"]==True):
                            return True
                return True
        except:
            return False

