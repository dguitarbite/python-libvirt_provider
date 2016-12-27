"""
test_node_device
----------------------------------

Tests for `libvirt_provider.node_device` module.

"""


import libvirt
import pytest

from libvirt_provider.node_device.node_device import NodeDevice


@pytest.fixture
def vnodedobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield NodeDevice(libvirt_conn)
    libvirt_conn.close()


def test_create_destroy_node_device(vnodedobj):

    pass


def test_attach_dettach_node_device(vnodedobj):

    pass
