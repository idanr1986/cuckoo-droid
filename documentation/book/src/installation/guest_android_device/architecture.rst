==========================
Guest Machine Architecture
==========================

Cuckoo Sandbox is a central management software for sample execution and analysis.
 
Each analysis is launched in a new and isolated virtual machine. Cuckoo’s infrastructure is composed of a host machine (the management software) and a number of guest machines (virtual machines that perform the analysis).
 
The host runs the core component of the sandbox that manages the entire analysis process, while the guests are the isolated environments where the malware samples are executed safely and then analyzed.
 
Each guest comprised of any android virtual machine (example: android x86 port) which is controlled by the machinery module (example: virtualbox). Additional components installed on the virtual machine to support the analysis process are:
	* CuckooAgent.apk java android application that support the cuckoo protocol.
	* analyzer.jar java package analyzer component that is sent to the guest machine at the beginning of the analysis.
	* Xposed - a framework for modules that can change the behavior of the system and apps without affecting any APKs. We created 2 additional modules with this framework:
	* Droidmon - Dalvik API call monitoring module.
	* Emulator anti-detection - a collection of known anti-detection techniques for hiding the android emulator.
	* Superuser app (already installed)- grants and manages Superuser rights for your phone.  
	* Content Generator - generates a random contact list for a more realistic appearance.
	
	
	.. image:: ../../_images/schemas/guest_android_device.png
				:align: center

