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

    net_xml = _get_netxml(name='testpncreatedestroy')
    netptr = vnetobj.create(net_xml)
    assert netptr
    assert netptr.isPersistent()
    assert netptr.isActive() is 0
    assert vnetobj.destroy(name='testpncreatedestroy') is 0


def test_persistent_network_start_stop(vnetobj):

    net_xml = _get_netxml(name='testpnstartstop')
    netptr = vnetobj.create(net_xml)
    assert netptr.create() is 0
    assert netptr.isActive()
    assert netptr.destroy() is 0
    assert vnetobj.destroy(name='testpnstartstop') is 0


def test_persistent_network_undefine_when_active(vnetobj):

    net_xml = _get_netxml(name='testpnundefineactive')
    netptr = vnetobj.create(net_xml)
    assert netptr.create() is 0
    assert netptr.isPersistent()
    assert netptr.isActive()
    assert vnetobj.destroy(name='testpnundefineactive') is 0
    assert netptr.isPersistent() is 0
    assert netptr.isActive()
    assert netptr.destroy() is 0


def test_non_persistent_network_start_stop(vnetobj):

    net_xml = _get_netxml(name='testnpstartstop')
    netptr = vnetobj.start(net_xml)
    assert netptr.isActive()
    assert netptr.isPersistent() is 0
    assert vnetobj.stop(name='testnpstartstop') is 0


def test_list_networks(vnetobj):

    libvirt_conn = libvirt.open('qemu:///system')
    expected_result = libvirt_conn.listNetworks()
    libvirt_conn.close()
    actual_result = vnetobj.list()
    assert actual_result.sort() == expected_result.sort()


def test_list_network(vnetobj):

    net_xml = _get_netxml(name='testlistnet')
    vnetobj.create(net_xml)
    libvirt_conn = libvirt.open('qemu:///system')
    expected_result = libvirt_conn.networkLookupByName('testlistnet').XMLDesc()
    libvirt_conn.close()
    actual_result = vnetobj.list(name='testlistnet')
    vnetobj.destroy(name='testlistnet')
    assert actual_result == expected_result


def test_update_config(vnetobj):
    # Test first, last, delete
    # TODO(dbite): Add a test case for modify.

    # Create test network.
    net_xml = _get_netxml(name='testupdateconfig')
    vnetobj.create(net_xml)
    flags = 'config'

    # Delete.
    xml_snippet = "<range start='10.7.5.5' end='10.7.5.25'></range>"
    actual_result = vnetobj.update('testupdateconfig',
                                   xml_snippet,
                                   command='delete',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    actual_result = vnetobj.update('testupdateconfig',
                                   xml_snippet,
                                   command='first',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    actual_result = vnetobj.update('testupdateconfig',
                                   xml_snippet,
                                   command='last',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

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
    actual_result = vnetobj.update('testupdateall',
                                   xml_snippet,
                                   command='delete',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    actual_result = vnetobj.update('testupdateall',
                                   xml_snippet,
                                   command='first',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    actual_result = vnetobj.update('testupdateall',
                                   xml_snippet,
                                   command='last',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

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
    actual_result = vnetobj.update('testupdatelive',
                                   xml_snippet,
                                   command='delete',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # First.
    xml_snippet = "<range start='10.7.5.115' end='10.7.5.155'></range>"
    actual_result = vnetobj.update('testupdatelive',
                                   xml_snippet,
                                   command='first',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # Last.
    xml_snippet = "<range start='10.7.5.15' end='10.7.5.55'></range>"
    actual_result = vnetobj.update('testupdatelive',
                                   xml_snippet,
                                   command='last',
                                   section='ip_dhcp_range',
                                   parent_index=0,
                                   flags=flags)
    assert actual_result is 0

    # Destroy test network.
    vnetobj.stop(name='testupdatelive')
