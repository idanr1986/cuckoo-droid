====================
Installing the Agent
====================

From release 0.4 on, Cuckoo has a custom agent that runs inside the guest and
handles communication and the exchange of data with the host.
This agent is designed to be cross-platform, and can therefore be used on Windows as well as on Linux and OS X.
To make Cuckoo work properly, install and start this agent.

It's very simple.

In the *agent/* directory you will find an *agent.py* file. Copy it
to the guest operating system (in any way you want, perhaps a temporary
shared folder or by downloading it from a host webserver) and run it.
This launches the XMLRPC server which will be listening for connections.

On Linux, launch the script from terminal window,::

	$ python agent.py
