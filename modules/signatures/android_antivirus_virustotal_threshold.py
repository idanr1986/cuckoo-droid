# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class KnownVirustotalThreshold(Signature):
    name = "android_antivirus_virustotal_threshold"
    description = "File has been identified by more the 10 AntiVirus on VirusTotal as malicious (Osint)"
    severity = 4
    categories = ["antivirus"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        counterThreshold=10

        AvWhiteList = ["Kingsoft","NANO-Antivirus","F-Prot","McAfee-GW-Edition","McAfee","MicroWorld-eScan","AVG","CAT-QuickHeal","F-Secure","Emsisoft","VIPRE","BitDefender","Fortinet",
                     "Commtouch","TrendMicro-HouseCall", "DrWeb","Comodo", "Kaspersky","AntiVir","Avast","Sophos","Ikarus","GData","ESET-NOD32"]
        try:
            avCounter=0
            if ("virustotal" in self.results and "scans" in self.results["virustotal"]):
                for key in self.results["virustotal"]["scans"].keys():
                    if(key in AvWhiteList):
                        if(self.results["virustotal"]["scans"][key]["detected"]==True):
                            self.add_match(None,key,self.results["virustotal"]["scans"][key]["result"])
                            avCounter=avCounter+1

            if(avCounter>=counterThreshold):
                return True
            else:
                return False
        except:
            return False

