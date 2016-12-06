class HostNet(object):
    """Network class carries out host side networking tasks of libvirt.

    Higher level tasks like creation, deletion are implemented as per
    the life-cycle of the lower level definitions. These tasks are
    simply assemble the methods which implement the finer details.
    The finder details are abstracted based on similarities like
    properties and definitions of the given network related topic.

    The finer implementation details like: network protocols (DHCP),
    types of networks (NAT, routed, isolated, bridged etc.) are
    abstracted to only think about the given abstraction and provide
    XML snippets like:
        <forward mode='nat'>
          <nat>
            <address start='1.2.3.4' end='1.2.3.10'/>
          </nat>
        </forward>

    Properties defines the way these networks interact with the host
    and the guests. They are concerned with tasks like DHCP lease,
    active/non-active, persistent, autostart and similar networking
    related topics.

    The end result would look similar to the below given XML snippet.
        <network>
          <name>ovs-net</name>
          <forward mode='bridge'/>
          <bridge name='ovsbr0'/>
          <virtualport type='openvswitch'>
            <parameters interfaceid='09b11c53-8b5c-4eeb-8f00-d84eaa0aaa4f'/>
          </virtualport>
          <vlan trunk='yes'>
            <tag id='42' nativeMode='untagged'/>
            <tag id='47'/>
          </vlan>
          <portgroup name='dontpanic'>
            <vlan>
              <tag id='42'/>
            </vlan>
          </portgroup>
        </network>

    Before passing this XML snippet to libvirt, XML Overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initializing the Network module.

    Libvirt connection object or libvirt connection URI required to
    connect to libvirt on the host.

    Description of various values, properties and flags. These could
    be passed as optional variables. These variables should be used,
    and override defaults unless explicitly overridden.
        {
        name: <str> <network name>,
        uuid: <uuid> <network_uuid>, (RFC 4122)
        ipv6: <bool> <yes,no>,
        }
    """

        # TODO(dbite): Figure out the scope of the virNetwork conn. obj.
        # check the start & stop unit tests.
        # Is the instance of this class bound to the life of one network obj or
        # to the entire life of the conn object and dynamically rebinds
        # to new vnobj.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    def create(self, xml_desc, **kwargs):
        """Define a new network domain."""

        return self.conn.networkDefineXML(xml_desc)

    def destroy(self, **kwargs):
        """Undefine an existing network domain by name, uuid or uuidstr."""

        vnetobj = self._get_vnetobj(**kwargs)

        return vnetobj.undefine()

    def start(self, xml_desc):
        """Create an existing network domain."""

        vnetobj = self.conn.networkCreateXML(xml_desc)

        return vnetobj

    def stop(self, **kwargs):
        """Destroy an existing network domain."""

        vnetobj = self._get_vnetobj(**kwargs)

        return vnetobj.destroy()

    def update(self, net_name, command, section, parent_index, net_xml, flags):
        """Update a given network domain.

        These parameters are deciding specifics for updating the network.

            - command: 'none', 'first', 'last', 'delete', 'modify'
                By default it modifies the existing network.
            - section: 'none', 'bridge', 'ip', 'dns_host', 'dns_srv',
                To update a given section, by default it is none
            - flags: Edit the 'config', 'current', 'live' net domain.
        """

        import libvirt  # TODO(dbite): Pass these params on init instead.
        vnetobj = self._get_vnetobj(name=net_name)

        vircommand = {
            'none': libvirt.VIR_NETWORK_UPDATE_COMMAND_NONE,
            'first': libvirt.VIR_NETWORK_UPDATE_COMMAND_ADD_FIRST,
            'last': libvirt.VIR_NETWORK_UPDATE_COMMAND_ADD_LAST,
            'delete': libvirt.VIR_NETWORK_UPDATE_COMMAND_DELETE,
            'modify': libvirt.VIR_NETWORK_UPDATE_COMMAND_MODIFY,
        }

        virflags = {
            'config': libvirt.VIR_NETWORK_UPDATE_AFFECT_CONFIG,
            'current': libvirt.VIR_NETWORK_UPDATE_AFFECT_CURRENT,
            'live': libvirt.VIR_NETWORK_UPDATE_AFFECT_LIVE,
        }

        virnetworksection = {
            'bridge': libvirt.VIR_NETWORK_SECTION_BRIDGE,
            'dns_host': libvirt.VIR_NETWORK_SECTION_DNS_HOST,
            'dns_srv': libvirt.VIR_NETWORK_SECTION_DNS_SRV,
            'dns_txt': libvirt.VIR_NETWORK_SECTION_DNS_TXT,
            'domain': libvirt.VIR_NETWORK_SECTION_DOMAIN,
            'forward': libvirt.VIR_NETWORK_SECTION_FORWARD,
            'forward_interface':
                libvirt.VIR_NETWORK_SECTION_FORWARD_INTERFACE,
            'forward_pf': libvirt.VIR_NETWORK_SECTION_FORWARD_PF,
            'ip': libvirt.VIR_NETWORK_SECTION_IP,
            'ip_dhcp_host': libvirt.VIR_NETWORK_SECTION_IP_DHCP_HOST,
            'ip_dhcp_range': libvirt.VIR_NETWORK_SECTION_IP_DHCP_RANGE,
            'none': libvirt.VIR_NETWORK_SECTION_NONE,
            'portgroup': libvirt.VIR_NETWORK_SECTION_PORTGROUP,
        }

        command = vircommand[command]
        section = virnetworksection[section]
        flags = virflags[flags]

        return vnetobj.update(command, section, parent_index, net_xml,
                              flags=flags)

    def list(self, name=None):
        """List existing networks or details (XML) of the given network."""

        if name:
            return self._get_vnetobj(name=name).XMLDesc()
        else:
            return self.conn.listNetworks()

    def _get_vnetobj(self, **kwargs):
        """Helper function to get virNetwork object.

        Accepts the following arguments, but only uses one (random).
        {
            name: <name of the network>,
            uuid: <uuid of the network>,
            uuid_str: <uuid in string format>,
        }
        """

        lookup_table = {
            'name': self.conn.networkLookupByName,
            'uuid': self.conn.networkLookupByUUID,
            'uuid_str': self.conn.networkLookupByUUIDString,
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)

    def bridge_conn(self):

        pass

    def domain(self):
        """DNS stuff."""

        pass

    def forwarding(self):
        """NAT, route, open, bridge, private, vepa, passthrough, hostdev."""

        pass

    def quality_of_service(self):
        """Average, peak, burst, floor."""

        pass

    def port_groups(self):
        """Port groups provides easy classification of networks."""

        pass

    def static_routes(self):

        pass

    def addressing(self):
        """Network addresses for isolated networks

        Valid only for isolated networks with no forward statement.
        mac, dns (forwarder, txt, host, srv),
        ip (tftp, dhcp(range, host, bootp))
        """

        pass
