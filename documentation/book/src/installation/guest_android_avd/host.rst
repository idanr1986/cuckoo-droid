==================
Host Configuration
==================

``conf/cuckoo.conf`` configuration::

	# Specify the name of the machinery module to use, this module will
	# define the interaction between Cuckoo and your virtualization software
	# of choice.
	machinery = avd
	
	[resultserver]
	# The Result Server is used to receive in real time the behavioral logs
	# produced by the analyzer.
	# Specify the IP address of the host. The analysis machines should be able
	# to contact the host through such address, so make sure it's valid.
	# NOTE: if you set resultserver IP to 0.0.0.0 you have to set the option
	# `resultserver_ip` for all your virtual machines in machinery configuration.
	ip = 127.0.0.1
	

		
``conf/avd.conf`` configuration::	

	[avd]
	#Path to the local installation of the android emulator
	emulator_path = <add>

	#Path to the local installation of the adb - android debug bridge utility.
	adb_path = <add>

	#Path to the emulator machine files is located
	avd_path = <add home_path>/.android/avd

	#name of the reference machine that is used to duplicate
	reference_machine = aosx

	# Specify a comma-separated list of available machines to be used. For each
	# specified ID you have to define a dedicated section containing the details
	# on the respective machine. (E.g. aosx_1,aosx_2,aosx_3)
	#currently supports only 1 machine for network limitations
	machines =aosx_1

	[aosx_1]
	# Specify the label name of the current machine as specified in your
	# aosx_1 configuration.
	label = aosx_1

	# Specify the operating system platform used by current machine
	platform = android

	# Specify the IP address of the current virtual machine. Make sure that the
	# IP address is valid and that the host machine is able to reach it. If not,
	# the analysis will fail.
	# its always 127.0.0.1 because android emulator networking configurations this the loopback of the host machine
	ip = 127.0.0.1

	#Specify the port for the emulator as your adb sees it.
	emulator_port=5554

	#10.0.2.2 is the loopback of the host machine very importent!!!
	resultserver_ip = 10.0.2.2
	
	resultserver_port = 2042
	
.. warning:: result server ip is always 10.0.2.2! (android emulator network configuration)
	
``conf/auxiliary.conf`` configuration::	

	[sniffer]
	# Enable or disable the use of an external sniffer (tcpdump) [yes/no].
	enabled = no

``conf/processing.conf`` configuration::	

	[droidmon]
	enabled = yes

	[googleplay]
	enabled = yes
	android_id = <add android_id>
	google_login = <add google_login>
	google_password = <add google_password>
	
	[apkinfo]
	enabled = yes
	#Decompiling dex with androguard in a heavy operation and for a big dex's
	#he can really consume performance from the cuckoo host ,so it's recommended to limit the size of dex that you will decompile
	#decompilation_threshold=2000000
	
	# disbale or enable decompilation, used for static info on reflection, crypto
	# dynamic loading, native calls and permissions extraction from code
	decompilation = yes 
	
``conf/reporting.conf`` configuration::	
	
	[reporthtml]
	enabled = no

	[reportandroidhtml]
	enabled = yes

	

