# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
import os
import subprocess

import time
import logging
import StringIO
from threading import Thread
from lib.common.abstracts import Auxiliary
from lib.common.results import NetlogFile
from lib.api import adb,screenshot
from lib.api.screenshot import Screenshot
from lib.core.config import Config

log = logging.getLogger(__name__)
DELAY = 1

class TouchSimulator(Auxiliary, Thread):

    
    def __init__(self):
        Thread.__init__(self)
        self.do_run = True


    def stop(self):

        self.do_run = False

    def run(self):
        while self.do_run:
            time.sleep(DELAY)
            if adb.check_package_on_top("com.android.settings/.DeviceAdminAdd"):
                log.info("TouchSimulator - Device Admin Granted")
                time.sleep(DELAY)
                adb.simulate_touch("386","753")
            elif adb.check_package_on_top("com.android.packageinstaller/.PackageInstallerActivity") or adb.check_package_on_top("com.android.packageinstaller/.InstallAppProgress"):
                log.info("TouchSimulator - Package Installer")
                adb.simulate_touch("386","753")
                adb.simulate_touch("675","464")
            elif adb.check_package_on_top("com.noshufou.android.su/.SuRequestActivity") or adb.check_package_on_top("com.thirdparty.superuser/com.koushikdutta.superuser.MultitaskSuRequestActivity"):
                log.info("TouchSimulator - SuperSU Root Granted")
                adb.simulate_touch("386","553")
        return True

