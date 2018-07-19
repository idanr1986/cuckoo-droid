# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
import hashlib
import json
import os
import subprocess
import logging
from threading import Thread
from lib.common.abstracts import Auxiliary
from lib.common import utils
import random
import re
import uuid

log = logging.getLogger(__name__)
DELAY = 1

class FileCollector(Auxiliary, Thread):

    
    def __init__(self):
        Thread.__init__(self)
        self.do_run = True


    def stop(self):

        self.do_run = False



    def run(self):

        label = "Droidmon-apimonitor-"
        adb = subprocess.Popen("logcat -s Xposed", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, executable='/system/bin/sh')
        md5_list = set()
        #  Collect Xposed logs
        while self.do_run:
            try:
                logcatInput = adb.stdout.readline()
                if not logcatInput:
                    raise Exception("We have lost the connection with ADB.")

                if label in logcatInput:
                    boxlog = logcatInput.replace(":","$$$",2).split("$$$")
                    try:
                        apicall = json.loads(boxlog[2])

                        if apicall["class"] == "libcore.io.IoBridge" and apicall["method"] == "open":
                            file_path = apicall["args"][0]

                            if "/sys/" in file_path or "/proc/" in file_path or '/data/app' in file_path or '/data/misc/keychain' in file_path or '.xml' in file_path:
                                continue

                            if ".DROPPED_FILE" in file_path:
                                continue

                            file_name = os.path.basename(file_path)+"_"+str(uuid.uuid1())

                            if os.path.exists(file_path):
                                if os.stat(file_path).st_size == 0:
                                    continue

                                with open(file_path) as file_read:
                                    file_data = file_read.read()
                                    md5 = hashlib.md5(file_data).hexdigest()
                                    if md5 in md5_list:
                                        continue
                                    utils.send_file("files/"+file_name, file_data)
                                    md5_list.add(md5)
                                    #log.info("add md5:"+ md5 + " on:"+str(apicall))
                            else:
                                log.info("FileCollector - File Not Exists: "+file_path)
                        elif((apicall["class"] == "dalvik.system.DexFile" and apicall["method"] == "openDexFile") or (apicall["class"] == "java.lang.Runtime" and apicall["method"] == "load")):
                            if apicall["dump"]:
                                file_path = apicall["path"]
                                file_name = os.path.basename(file_path)#+str(random.randrange(10))
                                #log.info(file_name)
                                #proc = subprocess.Popen(["adb", "pull", file_path, file_name], stdout=subprocess.PIPE)
                                #proc.communicate()

                                if os.path.exists(file_path):
                                    with open(file_path) as file_read:
                                        file_data = file_read.read()
                                        md5 = hashlib.md5(file_data).hexdigest()
                                        #log.info(md5)
                                        if md5 in md5_list:
                                            #log.info(md5_list)
                                            continue
                                        utils.send_file("files/"+file_name.replace(".DROPPED_FILE", ""), file_data)
                                        md5_list.add(md5)
                                else:
                                    log.info("FileCollector - File Not Exists: "+file_path)

                    except:
                        pass
            except:
                return False
        return True