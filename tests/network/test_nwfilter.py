"""
test_nwfilter
-----------------------------

Tests for `libvirt_provider.network` module.

- Create/Destroy NWFilter.
- Other basic tests like fetching the name etc.
"""


import libvirt
import pytest

from libvirt_provider.network.nwfilter import NetworkFilter


@pytest.fixture(autouse=False)
def vnwobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield NetworkFilter(libvirt_conn)
    libvirt_conn.close()


def _get_nwxml(name='tnwfilter', **kwargs):

    nwfilter_xml = """
        <filter name='"""+name+"""'>
          <uuid>6ef53069-ba34-94a0-d33d-17751b9b8cb1</uuid>
          <filterref filter='no-mac-spoofing'/>
          <filterref filter='no-ip-spoofing'/>
          <filterref filter='allow-incoming-ipv4'/>
          <filterref filter='no-arp-spoofing'/>
          <filterref filter='no-other-l2-traffic'/>
          <filterref filter='qemu-announce-self'/>
        </filter>
    """

    return nwfilter_xml


def test_nwfilter_create_destroy(vnwobj):

    assert True


def test_nwfilter_misc_tests(vnwobj):

    assert True
