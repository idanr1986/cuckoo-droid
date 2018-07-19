# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import logging
from lib.common.exceptions import CuckooPackageError
from lib.common import utils
import os
import re
import string
import subprocess
from zipfile import BadZipfile
from lib.api.androguard import apk
from lib.api.mypopen import MyPopen

log = logging.getLogger()

def install_sample(path):
    """Install the sample on the emulator via adb"""
    log.info("installing sample on emulator: pm install "+path)
    stdout, stderr = subprocess.Popen("/system/bin/pm install "+path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, executable="/system/bin/sh").communicate()

    if len(stdout) > 0:
        log.info("pm install stdout: " + stdout)
    if len(stderr) > 0:
        log.info("pm install stderr: " + stderr)
    lines = stderr.split("\n")
    for line in lines:
        #if in command output will appear "Failure" it means that the sample did not install
        if("Failure" in line):
            raise CuckooPackageError("failed to install sample on emulator:"+line)
    log.info("finished")

def get_package_activity_name(path):
    """Using the Android Asset Packaging Tool to extract from apk the package name and main activity"""
    shellcommand = "/data/local/aapt dump badging " + path
    process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/system/bin/sh")
    apkInfo = process.communicate()[0].splitlines()
    package=""
    activity=""

    for info in apkInfo:
        #Package info:
        if string.find(info, "package:", 0) != -1:
            package = findBetween(info, "name='", "'")
            continue

        #main activity:
        if string.find(info, "launchable-activity:", 0) != -1:
            activity = findBetween(info, "name='", "'")
            continue

    if(activity.__eq__("") or package.__eq__("")):
        return get_package_activity_name_androguard(path)
    return package, activity

def findBetween(s, prefix, suffix):
    try:
        start = s.index(prefix) + len(prefix)
        end = s.index(suffix, start)
        return s[start:end]
    except ValueError:
        return ""

def get_package_activity_name_androguard(path):
    """Using - Androguard to extract from apk the package name and main activity"""
    package=""
    main_activity=""

    try :
        a = apk.APK(path)
        if a.is_valid_APK():
            package = a.get_package()
            if package is None:
                raise CuckooPackageError("NO_PACKAGE_NAME_FOUND:"+os.path.basename(path))
            andro_main_activity = a.get_main_activity()
            if andro_main_activity is None:
                activities =  a.get_activities()
                for activity in activities:
                    activity = activity.lower()
                    if ("main" in activity):
                        log.warning('main activity from: if "main" in activity')
                        main_activity=activity
                        break
                    elif ("start" in activity):
                        log.warning('main activity from: if "start" in activity')
                        main_activity=activity
                        break

                if main_activity is "":
                    if activities.__len__()>0:
                        main_activity = activities[0]
                        log.warning("main activity from: activities[0]")
                    else:
                        raise CuckooPackageError("NO_MAIN_ACTIVITY_FOUND:"+os.path.basename(path))
            else:
                main_activity=andro_main_activity
            return package,main_activity
        else:
            raise CuckooPackageError("INVALID_APK:"+os.path.basename(path))

    except (IOError, OSError,BadZipfile) as e:
        raise CuckooPackageError("BAD_APK:"+os.path.basename(path)+","+e.message)

def execute_sample(package,activity):
    """Execute the sample on the emulator via adb"""
    log.debug("executing sample on emulator :adb shell am start -n " +package+"/"+activity)
    try:
        with MyPopen("/system/bin/am start -n "+ package + "/" + activity,
                     stdout=subprocess.PIPE,
                     shell=True,
                     stderr=subprocess.PIPE,
                     executable='/system/bin/sh') as proc:  # adb shell am start -n $pkg/$act

            log.info(str(proc.communicate()))
    except Exception as e:
        log.info("Exception in Popen: %s",e)


def dump_droidmon_logs(package):
    filename="/data/data/de.robv.android.xposed.installer/log/error.log"
    with open(filename) as log_file:
        tag = "Droidmon-apimonitor-"+package
        tag_error = "Droidmon-shell-"+package
        apimonitor = ""
        shell = ""
        for line in log_file:
            if tag in line:
                out = re.sub(tag+":", "", line)
                apimonitor=apimonitor+out
            if tag_error in line:
                out = re.sub(tag_error+":", "", line)
                shell=shell+out
        utils.send_file("logs/droidmon.log",apimonitor)
        utils.send_file("logs/droidmon_error.log",shell)

def execute_browser(url):
    """Execute the url on the emulator via adb"""
    str=""
    proc = subprocess.Popen("am start -a android.intent.action.VIEW -d " + url, stdout=subprocess.PIPE, shell = True, executable="/system/bin/sh")
    for s in proc.stdout.xreadlines():
        log.info(s)
        str=str+s

    lines = str.split("\n")
    for line in lines:
        if("Error" in line):
            raise CuckooPackageError("failed to execute default browser on emulator:"+line)

def take_screenshot(filename):
    proc1= subprocess.Popen("/system/bin/screencap -p /sdcard/"+filename, stdout=subprocess.PIPE, shell=True,
                                stderr=subprocess.PIPE,
                                executable='/system/bin/sh')
    proc1.communicate()
    return "/sdcard/"+filename

def simulate_touch(x,y):
    #log.info("simulating touch")
    cmd = "/system/bin/input tap "+x+" "+y
    try:
        stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True,
                            executable="/system/bin/sh").communicate()
        log.info("Simulated touch " + cmd)
        if len(stdout)>0:
            log.info("simulate touch stdout :" +  stdout)
        if len(stderr)>0:
            log.info("simulate touch stderr :" + stderr)
    except Exception as e:
        log.debug("Exception in simulate touch : ", str(e))

def check_package_on_top(package):
    try:
        #output = os.popen("/system/bin/dumpsys window windows").read()
        proc = subprocess.Popen("/system/bin/dumpsys window windows", stdout=subprocess.PIPE, shell=True,
                                stderr=subprocess.PIPE,
                                executable='/system/bin/sh')
        stdout, stderr = proc.communicate()
        for s in stdout.split("\n"):
            if ("mFocusedApp" in s):
                if package in s:
                    return True
        return False
    except Exception as e:
        log.info("Exception in check_package_on_top" + str(e))
        return False


def get_package_on_top():
    try:
        proc = subprocess.Popen("/system/bin/dumpsys window windows", stdout=subprocess.PIPE, shell=True,
                                stderr=subprocess.PIPE,
                                executable='/system/bin/sh')
        output, stderr = proc.communicate()

        for s in output.split("\n"):
            if ("mFocusedApp" in s):
                return s[s.find("ActivityRecord"):].split(" ")[1].split("/")[0]
    except Exception as e:
        log.info("Exception in get_package_on_top" + str(e))


def get_intents(path):
    a = apk.APK(path)
    if a.is_valid_APK():
        manifestxml = a.xml["AndroidManifest.xml"]

        intents = []

        for intent in manifestxml.getElementsByTagName("intent-filter"):
            for action in intent.getElementsByTagName("action"):
                intents.append(action.getAttribute("android:name"))
        return intents
