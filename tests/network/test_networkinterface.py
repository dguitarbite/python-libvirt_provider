"""
test_networkinterface
_-------------------------------

Tests for `libvirt_provider.network` module.

- Create/Destroy a network interface.
- Start/Stop a network interface.
- Other tests (...)
- Check list, exists?, etc.
- Check changeBegin/Commit/Rollback.
"""


import libvirt
import pytest

from libvirt_provider.network.networkinterface import NetworkInterface


@pytest.fixture(autouse=False)
def vnetintobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield NetworkInterface(libvirt_conn)
    libvirt_conn.close()


def _get_netintxml(name='tnetint', ip_addr='10.0.0.0'):

    networkint_xml = """
        <interface type='bridge' name='br0'>
          <start mode='onboot'/>
          <protocol family='ipv4'>
            <ip address='""" + ip_addr + """' prefix='16'/>
            <route gateway='10.160.255.254'/>
          </protocol>
          <bridge stp='off' delay='0.00'>
            <interface type='ethernet' name='em1'>
              <mac address='34:17:eb:bb:27:2a'/>
            </interface>
          </bridge>
        </interface>
    """

    return networkint_xml


def test_netint_create_destroy(vnetintobj):

    assert True


def test_netint_start_stop(vnetintobj):

    assert True


def test_netint_list(vnetintobj):

    assert True


def test_netint_change(vnetintobj):

    assert True
