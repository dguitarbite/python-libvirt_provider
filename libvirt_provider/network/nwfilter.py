class NetworkFilter(object):
    """Network filter defines firewall and network filtering in Libvirt.

    Higher level tasks like creation, deletion are implemented as per the
    life-cycle of the lower level definitions. These tasks are bound to the
    libvirt.conn object which defines certain actions. The finer details are
    provided by the virNWFilter object.

    The XML snippet should look like:

        <filter name='clean-traffic'>
          <uuid>6ef53069-ba34-94a0-d33d-17751b9b8cb1</uuid>
          <filterref filter='no-mac-spoofing'/>
          <filterref filter='no-ip-spoofing'/>
          <filterref filter='allow-incoming-ipv4'/>
          <filterref filter='no-arp-spoofing'/>
          <filterref filter='no-other-l2-traffic'/>
          <filterref filter='qemu-announce-self'/>
        </filter>

    Before passing this XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initialize the NetworkFIlter module."""

        # TODO(dbite): Re-think the conn object.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    def create(self, xml_desc):
        """Define a new NWFilter."""

        return self.conn.nwFilterDefineXML(xml_desc)

    def destroy(self, **kwargs):
        """Destroy an existing NWFilter."""

        vnwobj = self._get_vnwobj(**kwargs)

        return vnwobj.undefine()

    def get_name(self, **kwargs):

        vnwobj = self._get_vnwobj(**kwargs)

        return vnwobj.name()

    def _get_vnwobj(self, **kwargs):
        """Helper function to get virNWFilter object.

        Accepts the following arguments, but only uses one (random).
        {
            name: <Name of NWFilter>,
            uuid: <uuid of the NWFilter>,
            uuid_str: <uuid in string format of the network>
        }
        """

        lookup_table = {
            'name': self.conn.nwfilterLookUpByName,
            'uuid': self.conn.nwfilterLookUpByUUID,
            'uuid_str': self.conn.nwfilterLookUpByUUIDString
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)
