==========================
Saving the Virtual Machine
==========================

You are now ready to save the virtual machine to a snapshot state.

The ``CuckooAgent.apk`` app
must be running in the background and the ``Android Virtual Machine`` is fully configured.

	.. image:: ../../_images/screenshots/guest_snapshot.png
		:align: center
		
You can now proceed saving the machine. The method obviously depends on
your virtualization software.

If you follow all of the following steps properly, your virtual machine will be ready
for Cuckoo use.

VirtualBox
==========

In VirtualBox, you can take the snapshot from the graphical user
interface or from the command line::

    $ VBoxManage snapshot "<Name of VM>" take "<Name of snapshot>" --pause

After the snapshot creation is completed, you can power off the machine and
restore it::

    $ VBoxManage controlvm "<Name of VM>" poweroff
    $ VBoxManage snapshot "<Name of VM>" restorecurrent

VMware Workstation
==================

In VMware Workstation, you can take the snapshot from the graphical user
interface or from the command line::

    $ vmrun snapshot "/your/disk/image/path/wmware_image_name.vmx" your_snapshot_name

Your_snapshot_name is the name you choose for the snapshot.
Power off the machine from the GUI or from the command line::

    $ vmrun stop "/your/disk/image/path/wmware_image_name.vmx" hard
