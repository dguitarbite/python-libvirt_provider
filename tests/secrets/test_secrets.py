"""
test_stream
-----------------------------

Tests for `libvirt_provider.secrets` module.

- Create/Destroy secrets.
- Other basic tests like fetching the name etc.
"""


import libvirt
import pytest

from libvirt_provider.secrets.secrets import Secrets


@pytest.fixture(autouse=False)
def vsecretobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield Secrets(libvirt_conn)
    libvirt_conn.close()


def _get_secret_xml(name='tsecret', **kwargs):

    secret_xml = """
        <secret ephemeral='no' private='yes'>
          <description>Super secret name of my first puppy</description>
          <uuid>0a81f5b2-8403-7b23-c8d6-21ccc2f80d6f</uuid>
          <usage type='volume'>
            <volume>/var/lib/libvirt/images/puppyname.img</volume>
          </usage>
        </secret>
    """

    return secret_xml


def test_secret_create_destroy(vsecretobj):

    assert True


def test_secret_misc_tests(vsecretobj):

    assert True
