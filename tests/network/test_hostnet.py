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


def _get_netxml(name='test_provider', ip_addr='10.7.5.0'):

    network_xml = '''
    <network>
        <name>'''+name+'''</name>
        <uuid></uuid>
        <forward mode='nat'>
            <nat>
                <port start='1024' end='65535'/>
            </nat>
        </forward>
        <ip address="'''+ip_addr+'''" netmask="255.255.255.0"/>
    </network>
    '''

    return network_xml


def test_network_create(vnetobj):

    net_xml = _get_netxml(name='testcreate')
    result = vnetobj.create(net_xml)
    vnetobj.destroy(name='testcreate')
    assert result


def test_network_destroy(vnetobj):

    net_xml = _get_netxml(name='testdestroy')
    vnetobj.create(net_xml)
    result = vnetobj.destroy(name='testdestroy')
    assert result == 0


def test_network_start(vnetobj):

    net_xml = _get_netxml(name='teststart')
    result = vnetobj.start(net_xml)
    vnetobj.stop(name='teststart')
    assert result is None


def test_network_stop(vnetobj):

    net_xml = _get_netxml(name='teststop')
    vnetobj.start(net_xml)
    result = vnetobj.stop(name='teststop')
    assert result == 0
