=====================
Network Configuration
=====================

It's time to set up the network for your virtual machine.

Linux Settings
================

Before configuring the underlying networking of the virtual machine, you may
want to tweak some settings inside Linux.

In the file ``/etc/network/interfaces``, edit ``eth0`` settings. 
For example, the virtualbox network::

	auto eth0
	iface eth0 inet static
	address 192.168.56.101
	netmask 255.255.255.0
	network 192.168.56.0
	broadcast 192.168.56.255
	gateway 192.168.56.1
	
Virtual Networking
==================

You need to decide how to make your virtual machine access the Internet or your local network.

In previous releases, Cuckoo used shared folders to exchange data between the host and guests. From release 0.4 on, it uses a custom agent that communicates
over the network with a simple XMLRPC protocol.

To make it work properly, configure your machine's network so that the host and the guest can communicate.
To ensure the virtual network was set up correctly, test the network access by pinging a guest. Use only static IP addresses for your guest, as Cuckoo doesn't support DHCP; using it will break your setup.

This stage depends heavily on your requirements and the characteristics of your virtualization software.

    .. warning:: Virtual networking errors!
        Virtual networking is a vital component for Cuckoo; be sure there is connectivity between host and guest.
        Most of the issues reported by users are related to an incorrect networking setup.
        Check your virtualization software documentation and test connectivity with ping and telnet.

The recommended setup uses a host-only networking layout with proper
forwarding and filtering configuration done with ``iptables`` on the host.

For example, using VirtualBox, you can enable Internet access to the virtual
machines using the following ``iptables`` rules: (Assuming that eth0 is your
outgoing interface, vboxnet0 is your virtual interface and 192.168.56.0/24 is
your subnet address).

    iptables -A FORWARD -o eth0 -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT
    iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -A POSTROUTING -t nat -j MASQUERADE

Add IP forwarding::

    sysctl -w net.ipv4.ip_forward=1
