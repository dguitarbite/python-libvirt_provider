"""
test_network
----------------------------------

Tests for `libvirt_provider.network` module.

- Create a network.
- Start the network.
- Other tests (ping etc.)
- Stop the network.
- Destroy the network.
- Check if the network exists.
- Check other properties of the network.
"""


import libvirt
import pytest

from libvirt_provider.network.hostnet import HostNet


@pytest.fixture
def vnetobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield HostNet(libvirt_conn)
    libvirt_conn.close()


def _get_netxml(name='test_provider', ip_addr='10.7.5.0',
                dhcp_range=['10.7.5.5', '10.7.5.25']):

    network_xml = '''
    <network>
        <name>'''+name+'''</name>
        <uuid></uuid>
        <forward mode='nat'>
            <nat>
                <port start='5555' end='5560'/>
            </nat>
        </forward>
        <ip address="'''+ip_addr+'''" netmask="255.255.255.0">
            <dhcp>
            <range start="'''+dhcp_range[0]+'''" end="'''+dhcp_range[1]+'''"/>
            </dhcp>
        </ip>
    </network>
    '''

    return network_xml


def test_persistent_network_create_destroy(vnetobj):

    net_xml = _get_netxml(name='testcreatedestroy')
    netptr = vnetobj.create(net_xml)
    assert netptr
    assert netptr.isPersistent()
    assert netptr.isActive() is 0
    result = vnetobj.destroy(name='testcreatedestroy')
    assert result == 0


def test_start_stop_inactive_networks(vnetobj):

    net_xml = _get_netxml(name='teststartstop')
    netptr = vnetobj.create(net_xml)
    assert netptr.create() is 0
    assert netptr.isActive()
    assert netptr.destroy() is 0
    vnetobj.destroy(name='teststartstop')


def test_network_start_stop(vnetobj):

    net_xml = _get_netxml(name='teststart')
    netptr = vnetobj.start(net_xml)
    assert netptr.isActive()
    assert netptr.isPersistent() is 0
    vnetobj.stop(name='teststart')


def test_network_stop(vnetobj):

    net_xml = _get_netxml(name='teststop')
    vnetobj.start(net_xml)
    result = vnetobj.stop(name='teststop')
    assert result == 0


def test_list_networks(vnetobj):

    libvirt_conn = libvirt.open('qemu:///system')
    expected_result = libvirt_conn.listNetworks()
    libvirt_conn.close()
    result = vnetobj.list()
    assert result == expected_result


def test_list_network(vnetobj):

    net_xml = _get_netxml(name='testlistnet')
    vnetobj.create(net_xml)
    libvirt_conn = libvirt.open('qemu:///system')
    expected_result = libvirt_conn.networkLookupByName('testlistnet').XMLDesc()
    libvirt_conn.close()
    result = vnetobj.list(name='testlistnet')
    vnetobj.destroy(name='testlistnet')
    assert result == expected_result


def test_update_config(vnetobj):
    # Test first, last, delete
    # TODO(dbite): Add a test case for modify.

    # Create test network.
    net_xml = _get_netxml(name='testupdateconfig')
    vnetobj.create(net_xml)
    flags = 'config'

    # Delete.
    xml_snippet = "<range start='10.7.5.5' end='10.7.5.25'></range>"
    result = vnetobj.update('testupdateconfig', 'delete', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    result = vnetobj.update('testupdateconfig', 'first', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    result = vnetobj.update('testupdateconfig', 'last', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Destroy test network.
    vnetobj.destroy(name='testupdateconfig')


def test_update_all(vnetobj):
    # Test first, last, delete
    # TODO(dbite): Add a test case for modify.

    # Create test network.
    net_xml = _get_netxml(name='testupdateall')
    netptr = vnetobj.create(net_xml)
    netptr.create()
    flags = 'current'

    # Delete.
    xml_snippet = "<range start='10.7.5.5' end='10.7.5.25'></range>"
    result = vnetobj.update('testupdateall', 'delete', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    result = vnetobj.update('testupdateall', 'first', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    result = vnetobj.update('testupdateall', 'last', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Destroy test network.
    netptr.destroy()
    vnetobj.destroy(name='testupdateall')


def test_update_live(vnetobj):
    # Test first, last, delete
    # TODO(dbite): Add a test case for modify.

    # Create test network.
    net_xml = _get_netxml(name='testupdatelive')
    vnetobj.start(net_xml)
    flags = 'live'

    # Delete.
    xml_snippet = "<range start='10.7.5.5' end='10.7.5.25'></range>"
    result = vnetobj.update('testupdatelive', 'delete', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    result = vnetobj.update('testupdatelive', 'first', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    result = vnetobj.update('testupdatelive', 'last', 'ip_dhcp_range', 0,
                            xml_snippet, flags)
    assert result == 0

    # Destroy test network.
    vnetobj.stop(name='testupdatelive')
