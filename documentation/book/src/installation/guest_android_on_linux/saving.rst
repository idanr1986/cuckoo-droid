==========================
Saving the Virtual Machine
==========================

You are now ready to save the virtual machine to a snapshot state.

The ``agent.py`` script must be running and the ``android emulator`` fully configured.

	.. image:: ../../_images/screenshots/final_android_on_linux.png
		:align: center
		
Proceed to save the machine. The exact method depends on your virtualization software.

If you follow all of the following steps properly, your virtual machine is ready
for use.

VirtualBox
==========

With VirtualBox, you can take the snapshot from the graphical user
interface or from the command line::

    $ VBoxManage snapshot "<Name of VM>" take "<Name of snapshot>" --pause

After the snapshot creation is completed, you can power off the machine and
restore it::

    $ VBoxManage controlvm "<Name of VM>" poweroff
    $ VBoxManage snapshot "<Name of VM>" restorecurrent

VMware Workstation
==================

With VMware Workstation, you can take the snapshot from the graphical user
interface or from the command line::

    $ vmrun snapshot "/your/disk/image/path/wmware_image_name.vmx" your_snapshot_name

Your_snapshot_name is the name you choose for the snapshot.
Power off the machine from the GUI or from the command line::

    $ vmrun stop "/your/disk/image/path/wmware_image_name.vmx" hard
