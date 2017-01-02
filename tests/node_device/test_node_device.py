"""
test_node_device
----------------------------------

Tests for `libvirt_provider.node_device` module.

"""


import libvirt
import pytest

from libvirt_provider.node_device.node_device import NodeDevice


@pytest.fixture
def vnodedevobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield NodeDevice(libvirt_conn)
    libvirt_conn.close()


def _get_nodedev_xml(cap, name="tnodedev"):

    pass


def test_all_node_devices(vnodedevobj):

    assert vnodedevobj.list_all_node_devices(flags=['all'])
    assert vnodedevobj.list_all_node_devices(
        flags=['Network device', 'PCI device'])


def test_num_of_devices(vnodedevobj):

    expected_result = vnodedevobj.list_all_node_devices(flags=['all'])
    actual_result = vnodedevobj.list_no_of_node_devices()
    assert len(expected_result) == actual_result


def test_create_destroy_node_device(vnodedevobj):

    # Note(dbite): To be implemented later.
    # Most probably this makes sense as a part of integration test case.
    assert True


def test_attach_dettach_node_device(vnodedevobj):

    # Note(dbite): To be implemented later, need a valid domain (VM) to be
    #              present.
    # Most probably makes sense as a part of integration test case.
    assert True
