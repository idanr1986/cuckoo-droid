# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class AndroidShellCommands(Signature):
    name = "application_executed_shell_command"
    description = "Application Executed Shell Command (Dynamic)"
    severity = 4
    categories = ["android"]
    authors = ["idanr1986"]
    minimum = "0.5"

    def run(self):
        try:
            if "commands" in self.results["droidmon"]:
                for command in self.results["droidmon"]["commands"]:
                    self.add_match(None, "Command", command)
            self.has_matches()
        except:
            return False
