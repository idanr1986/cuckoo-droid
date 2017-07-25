============
Requirements
============

To make Cuckoo run properly in your virtualized Linux system, you
must install some required software and libraries.

Additional Software
===================

Linux dependencies are required::

    $ sudo apt-get install openjdk-7-jre libstdc++6:i386 libgcc1:i386 zlib1g:i386 libncurses5:i386

Install Android SDK
===================

Android SDK is a strict requirement for the Cuckoo android_on_linux guest component (*analyzer*) to run properly.

Download the latest SDK from the `official website`_.

After downloading the sdk, go to the folder containing the .tgz file::

    $ tar -xvf android-sdk_r24.0.2-linux.tgz
    $ cd android-sdk
    $ tools/android
	 
In the Android SDK Manager, install the following components:

* Tools
    * Android SDK Tools
    * Android Platform-tools Tools
    * newest Android SDK Tools
* Android 4.1.2 (API 16)
    * SDK Platform
    * ARM EABI v7a System Image

    .. image:: ../../_images/screenshots/android_SDK_check.png
        :align: center


Add the android SDK tool to ``$PATH`` variable::

    $ export PATH=$PATH:sdk_path/tool:sdk_path/build-tools/x.x.x.x/:sdk_path/platform-tools

.. _`official website`: http://developer.android.com/sdk/index.html


Create Android Virtual Device
=============================
Start the Android Virtual Device Manager::

	$ android avd

Press ``Create..`` and add the following configurations::

	AVD Name - aosx
	Device - Nexus One
	Target - android 4.1.2
	Cpu/Abi - arm
	Ram - 512mb
	Vm Heap - 32
	Internal Storage - 512mb
	Sdcard size - 512 mib
	Emulation options - use host GPU

and click OK.

	.. image:: ../../_images/screenshots/avd.png
		:align: center

Prepare the Android Virtual Device for Analysis
===============================================

Copy the folder ``utils/android_emulator_creator`` to the Linux guest machine::

	$ cd android_emulator_creator_path/
	
Start the emulator with ``/system`` in read-write mode::

	$ emulator -avd aosx -qemu -nand -system,size=0x1f400000,file=<sdk_path>/system-images/android-16/default/armeabi-v7a/system.img&

Run the script in ``utils/android_emulator_creator/create_guest_android_on_linux.sh``

* Press settings->security->screenlock->none
* Press settings->Display->sleep->30 minutes
* Start Generate contacts app
* Start Supersuser app
* Start xposedinstaller app
* In Modules, check both packages ``Droidmon`` , ``Android Blue Pill``

	.. image:: ../../_images/screenshots/android_xposed.png
		:align: center
* Press framework -> install -> cancel-> soft reboot

Leave the emulator on for the snapshot.
	

