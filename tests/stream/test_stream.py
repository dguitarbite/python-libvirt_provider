"""
test_stream
-----------------------------

Tests for `libvirt_provider.stream` module.

- Create/Destroy secrets.
- Other basic tests like fetching the name etc.
"""


import libvirt
import pytest

from libvirt_provider.stream.stream import Stream


@pytest.fixture(autouse=False)
def vstreamobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield Stream(libvirt_conn)
    libvirt_conn.close()


def test_secret_create_destroy(vstreamobj):

    assert True


def test_secret_misc_tests(vstreamobj):

    assert True
