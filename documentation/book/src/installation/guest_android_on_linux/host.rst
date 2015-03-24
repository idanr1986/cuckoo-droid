==================
Host Configuration
==================

``conf/cuckoo.conf`` configuration::

	# Specify the name of the machinery module to use, this module will
	# define the interaction between Cuckoo and your virtualization software
	# of choice.
	machinery = virtualbox
	
	[resultserver]
	# The Result Server is used to receive in real time the behavioral logs
	# produced by the analyzer.
	# Specify the IP address of the host. The analysis machines should be able
	# to contact the host through such address, so make sure it's valid.
	# NOTE: if you set resultserver IP to 0.0.0.0 you have to set the option
	# `resultserver_ip` for all your virtual machines in machinery configuration.
	ip = 192.168.56.1
	
		
``conf/virtualbox.conf`` configuration::	

	[android_on_linx]
	label = android_on_linx
	platform = android_on_linux
	ip = 192.168.56.201
	snapshot = clean_snapshot
	interface = vboxnet0
	resultserver_ip = 192.168.56.1
	resultserver_port = 2042
	
	
``conf/auxiliary.conf`` configuration::	

	[sniffer]
	# Enable or disable the use of an external sniffer (tcpdump) [yes/no].
	enabled = yes

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
	
``conf/reporting.conf`` configuration::	
	
	[reporthtml]
	enabled = no

	[reportandroidhtml]
	enabled = yes

	

