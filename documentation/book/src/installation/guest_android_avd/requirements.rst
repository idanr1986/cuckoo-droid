============
Requirements
============

To make Cuckoo run properly with the Android Emulator, install these required software and libraries on the Cuckoo host.

Additional Software
===================

Linux dependencies are required::

    $ sudo apt-get install openjdk-7-jre libstdc++6:i386 libgcc1:i386 zlib1g:i386 libncurses5:i386

Install Android SDK
===================

Android SDK is a strict requirement for the Cuckoo android_on_linux guest component (*analyzer*) to run properly.

Download the latest SDK from the `official website`_.

After downloading the SDK, go to the folder containing the .tgz file::

    $ tar -xvf android-sdk_r24.0.2-linux.tgz
    $ cd android-sdk
    $ tools/android
	 
In The Android SDK Manager, check to install the following components:

* Tools
    * Android SDK Tools
    * Android Platform-tools Tools
    * newest Android SDK Tools
* Android 4.1.2 (API 16)
    * SDK Platform
    * ARM EABI v7a System Image

    .. image:: ../../_images/screenshots/android_SDK_check.png
        :align: center


The android SDK tool needs to be added to the ``$PATH`` variable::

    $ export PATH=$PATH:sdk_path/emulator:sdk_path/tools:sdk_path/build-tools/x.x.x.x/:sdk_path/platform-tools

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

Prepare the Android Virtual Device Reference Machine for Analysis
=================================================================
Before starting the emulator do the following::
    
    $ cp /sdk_path/system-images/android-16/default/armeabi-v7a/system.img /home/user/.android/avd/aosx.avd/system-qemu.img
    
Start the emulator with ``/system`` in read-write mode::

	$ emulator -avd aosx -qemu -nand -system,size=0x1f400000,file=/home/user/.android/avd/aosx.avd/system-qemu.img&

Run the script in ``utils/android_emulator_creator/create_guest_avd.sh``

* Press settings->security->screenlock->none
* Press settings->Display->sleep->30 minutes
* Start Generate contacts app
* Start Supersuser app
* Start xposedinstaller app
* In Modules, check both packages ``Droidmon`` , ``Android Blue Pill``

	.. image:: ../../_images/screenshots/android_xposed.png
		:align: center
* Press framework -> install -> cancel-> soft reboot

After the reboot, close the machine.

You have now created a reference machine to duplicate each analysis instead of reverting to snapshot.
	

