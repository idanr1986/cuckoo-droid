============
Requirements
============

To make Cuckoo run properly in your virtualized Linux system, you
must install some required software and libraries.

Install Android Debug Bridge
============================

There is no need to download all the SDK to the cuckoo host. Only adb is required.

    $ sudo add-apt-repository ppa:nilarimogard/webupd8
    $ sudo apt-get update
    $ sudo apt-get install android-tools-adb

Prepare Android Virtual Machine for Analysis
============================================


Start the Android virtual machine after :doc:`configuring the network. <./network>`::

    $ adb root
    $ adb connect 192.168.56.10

Run the script in ``utils/android_emulator_creator/create_guest_device.sh``

* Press settings->security->screenlock->none
* Press settings->Display->sleep->Never Timeout
* Press settings->security->checkout verify apps
* Press settings->security->check Unknown sources

* Start Generate contacts app
* Start Supersuser app -> automatic response -> allow
                       -> notification None
* Start xposedinstaller app
* In Modules check both packeages ``Droidmon`` , ``Android Blue Pill``

	.. image:: ../../_images/screenshots/android_xposed.png

* Press framework -> install -> cancel-> soft reboot

Start cuckooAgent app.
Press esc and take snapshot.
