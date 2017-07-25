#/usr/bin/env bash

#this script is meant for easy creation on an analysis machine for android device (android port_x86)

#Path to the local installation of the adb - android debug bridge utility.
#ADB=/Applications/adt-bundle/sdk/platform-tools/adb

ADB=$(which adb)

if [ ! -f $ADB ]
then
    echo "Error: adb path is not valid."
    exit
fi
echo "adb has been found."

# Install Xposed Application
echo "Installing Xposed Application"
$ADB install apps/de.robv.android.xposed.installer_v33_36570c.apk

# Install Droidmon Application
echo "Installing Droidmon Application"
$ADB install hooking/Droidmon.apk

# Install Anti Emulator Detection Application
echo "Installing Anti Emulator Detection Application"
$ADB install hooking/EmulatorAntiDetect.apk
$ADB push anti-vm/fake-build.prop /data/local/tmp/
$ADB push anti-vm/fake-cpuinfo /data/local/tmp/
$ADB push anti-vm/fake-drivers /data/local/tmp/

# Install Content Generator
echo "Installing Content Generator"
$ADB install apps/ImportContacts.apk

# Install Cuckoo Agent
echo "Installing Cuckoo Agent"
$ADB remount
$ADB push ../../agent/android/java_agent/CuckooAgent.apk /system/app/

echo "Device is ready!"


