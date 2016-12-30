class NodeDevice(object):
    """Node devices manages guest interfaces via. passthrough from host.

    Node devices deal with management of various interfaces form host machine
    which are handed to guests. These devices could be storage interfaces,
    network interfaces, usb devices, pci ports etc.

    The end result would look similar to the below given XML snippet.

        <device>
          <name>pci_0000_02_00_0</name>
          <path>/sys/devices/pci0000:00/0000:00:04.0/0000:02:00.0</path>
          <parent>pci_0000_00_04_0</parent>
          <driver>
            <name>igb</name>
          </driver>
          <capability type='pci'>
            <domain>0</domain>
            <bus>2</bus>
            <slot>0</slot>
            <function>0</function>
            <product id='0x10c9'>82576 Gigabit Network Connection</product>
            <vendor id='0x8086'>Intel Corporation</vendor>
            <capability type='virt_functions'>
              <address domain='0x0000' bus='0x02' slot='0x10' function='0x0'/>
              <address domain='0x0000' bus='0x02' slot='0x10' function='0x2'/>
              <address domain='0x0000' bus='0x02' slot='0x10' function='0x4'/>
              <address domain='0x0000' bus='0x02' slot='0x10' function='0x6'/>
              <address domain='0x0000' bus='0x02' slot='0x11' function='0x0'/>
              <address domain='0x0000' bus='0x02' slot='0x11' function='0x2'/>
              <address domain='0x0000' bus='0x02' slot='0x11' function='0x4'/>
            </capability>
            <iommuGroup number='12'>
              <address domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
              <address domain='0x0000' bus='0x02' slot='0x00' function='0x1'/>
            </iommuGroup>
            <pci-express>
              <link validity='cap' port='1' speed='2.5' width='1'/>
              <link validity='sta' speed='2.5' width='1'/>
            </pci-express>
          </capability>
        </device>

    Before passing this XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initializing the NodeDevice module.

    Libvirt connection object or libvirt connection URI is required to
    connect to libvirt on the host.

    Description of various values, properties and flags. These could
    be passed as optional variables. These variables should be used,
    and override defaults unless explicitly overridden.
    """

        # TODO(dbite): Rethink the libvirt.conn object handling and it's scope.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    def list_all_node_devices(self, cap=None, flags=0):
        """List node devices."""

        return self.conn.listDevices(cap, flags=flags[flags])

    def list_no_of_node_devices(self, cap=None, flags=0):
        """List number of node devices."""

        return self.conn.numOfDevices(cap, flags=0)

    def create(self, xml_desc):
        """Define a new node device."""

        return self.conn.nodeDeviceCreateXML(xml_desc)

    def destroy(self, **kwargs):
        """Undefine an existing node device by name, uuid or uuidstr."""

        vnodeobjs = self._get_vnodeobj(**kwargs)

        node_device_destroy = []

        for vnodeobj in vnodeobjs:
            node_device_destroy.append(vnodeobj.destroy())

        return node_device_destroy

    def dettach(self, **kwargs):
        """Dettach an existing node device from the host.

        This allows the node device to be free for attaching to a guest.
        """

        vnodeobj = self._get_vnodeobj(**kwargs)

        return vnodeobj.dettach()

    def reattach(self, **kwargs):
        """Reattach a previously dettached node device.

        This allows the host to use a previously dettached node device. This
        method should be frequently called after dettaching a node device.
        """

        vnodeobj = self._get_vnodeobj(**kwargs)

        return vnodeobj.reAttach()

    def _get_vnodeobj(self, cap, flags=0, **kwargs):
        """Helper function to get virNodeDevice object.

        Accepts the following arguments, but only uses one (random).
        {
            name: <name of the node device>,
            wwnn: <SCSI fc_host's WWNN & WWPN of the node device>,
        }
        """

        lookup_table = {
            'name': self.conn.nodeDeviceLookupByName,
            'wwn': self.conn.networkLookupBySCSIHostByWWN,
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)
