"""
test_storage
----------------------------------

Tests for `libvirt_provider.storage` module.

- Create a volume.
- Destroy the volume.
- Check if the volume exists.
- Check other properties of the libvirt storage.
"""


import libvirt
import os
import pytest
import shutil

from libvirt_provider.storage.storage import Storage


STORAGE_POOLS = os.path.join(os.getcwd(), '.tlibvirtprov')


@pytest.fixture
def vsobj():

    libvirt_conn = libvirt.open('qemu:///system')
    yield Storage(libvirt_conn)
    libvirt_conn.close()
    print("Hmmm, tear down \n\n\n ... \n\n\n how many times?")
    _delete_storagepools()


def _setup_dir(name=".tlibvirtprov", path=None):
    """Create directory in the local filesystem for storage pool."""

    lib_dir = STORAGE_POOLS

    if not os.path.exists(lib_dir):
        os.mkdir(lib_dir)

    if not path:
        path = os.path.join(lib_dir, name)

    if not os.path.exists(path):
        path = os.path.abspath(path)
        os.mkdir(path)

    return path


def _delete_storagepools():
    """Delete directory and its content recursively."""

    # Warning: Please make sure that storagepool under libvirt
    #          is undefined before running this function.
    global STORAGE_POOLS

    shutil.rmtree(STORAGE_POOLS)


def _get_storagepoolxml(name='test_provider_pool', path=None):

    path = _setup_dir(name, path)

    pool_xml = """
    <pool type='dir'>
      <name>"""+name+"""</name>
      <uuid></uuid>
      <target>
        <path>"""+path+"""</path>
        <permissions>
          <mode>0755</mode>
          <owner>1000</owner>
          <group>100</group>
        </permissions>
      </target>
    </pool>
    """

    return pool_xml


def _get_storagevolxml(name='test_provider_vol'):

    vol_xml = """
    <volume type='file'>
      <name>"""+name+"""</name>
      <source>
      </source>
      <capacity unit='bytes'>1073741824</capacity>
      <allocation unit='bytes'>1073741824</allocation>
      <target>
        <format type='qcow2'/>
        <permissions>
          <mode>0600</mode>
          <owner>1000</owner>
          <group>10</group>
        </permissions>
      </target>
    </volume>
    """

    return vol_xml


###############################################################################
#   Storage Pools and Storage Volumes belonging to them.
###############################################################################


def test_persistent_storagepool_create_destroy(vsobj):

    sp_xml = _get_storagepoolxml(name='testcreatedestroy')
    spptr = vsobj.create_pool(sp_xml, flags=0)
    assert spptr
    assert spptr.isPersistent()
    assert spptr.isActive() == 0
    assert spptr.delete() == 0
    result = vsobj.destroy_pool(name='testcreatedestroy')
    assert result == 0


def test_persistent_storagepool_storagevol_create_destroy(vsobj):

    sp_xml = _get_storagepoolxml(name='testpStartStop')
    spptr = vsobj.create_pool(sp_xml, flags=0)
    assert spptr.create() == 0

    sv_xml = _get_storagevolxml(name='testpVol')
    svptr = vsobj.create_vol(sv_xml, flags=0, name='testpStartStop')
    assert svptr
    assert vsobj.destroy_vol(vspobj=spptr, name='testpVol') == 0
    assert spptr.destroy() == 0
    assert spptr.undefine() == 0


def test_non_persistent_storagepool_start_stop(vsobj):

    sp_xml = _get_storagepoolxml(name='testnpstartstop')
    spptr = vsobj.start_pool(sp_xml)
    assert spptr
    assert spptr.isPersistent() == 0
    assert spptr.isActive()
    assert vsobj.stop_pool(name='testnpstartstop') == 0


def test_non_persistent_storagepool_storagevol_start_stop(vsobj):

    sp_xml = _get_storagepoolxml(name='testnpStartStop')
    spptr = vsobj.start_pool(sp_xml, flags=0)
    assert spptr
    sv_xml = _get_storagevolxml(name='testnpVol')
    svptr = vsobj.create_vol(sv_xml, flags=0, name='testnpStartStop')
    assert svptr
    assert vsobj.destroy_vol(vspobj=spptr, name='testnpVol') == 0
    assert spptr.destroy() == 0


def test_persistent_storagepool_start_stop(vsobj):

    sp_xml = _get_storagepoolxml(name='testpstartstop')
    spptr = vsobj.create_pool(sp_xml, flags=0)
    assert spptr.isPersistent()
    assert spptr.isActive() == 0
    assert spptr.create() == 0
    assert spptr.isActive()

    with pytest.raises(libvirt.libvirtError):
        vsobj.destroy_pool(name='testpstartstop')

    assert spptr.destroy() == 0
    assert spptr.delete() == 0
    assert vsobj.destroy_pool(name='testpstartstop') == 0


# Helper function.
def _setup_pools(spptrs, vsobj):

    # Create 5 of each type of storage pools for testing purposes.
    for i in range(5):

        name = 'tListSPDefinedActive' + str(i)
        sp_xml = _get_storagepoolxml(name)
        spptr = vsobj.create_pool(sp_xml)
        spptr.create()
        spptrs['persistent'].append(spptr)
        spptrs['active'].append(spptr)

        name = 'tListSPActive' + str(i)
        sp_xml = _get_storagepoolxml(name)
        spptr = vsobj.start_pool(sp_xml)
        spptrs['active'].append(spptr)

        name = 'tListSPDefinedNotActive' + str(i)
        sp_xml = _get_storagepoolxml(name)
        spptr = vsobj.create_pool(sp_xml)
        spptrs['persistent'].append(spptr)

    return spptrs


# Helper function.
def _destroy_pools(spptrs, vsobj):

    # Cleanup: Delete created storage pools.
    for spptr in spptrs['active']:
        assert spptr.destroy() == 0
    for spptr in spptrs['persistent']:
        assert spptr.delete() == 0
        assert spptr.undefine() == 0


def test_list_pools(vsobj):

    spptrs = {
        'persistent': [],
        'active': []
    }

    # Create storage pools for improving the validity of this test case.
    _setup_pools(spptrs, vsobj)

    libvirt_conn = libvirt.open('qemu:///system')
    expected_result = [sp.name() for sp in libvirt_conn.listAllStoragePools()]
    actual_result = [sp.name() for sp in vsobj.conn.listAllStoragePools()]
    assert expected_result == actual_result
    expected_result = libvirt_conn.listStoragePools()
    actual_result = vsobj.conn.listStoragePools()
    assert expected_result == actual_result
    expected_result = libvirt_conn.listDefinedStoragePools()
    actual_result = vsobj.conn.listDefinedStoragePools()
    assert expected_result == actual_result


def test_clone_volume(vsobj):

    sp_xml = _get_storagepoolxml(name='testnpCloneVol')
    spptr = vsobj.start_pool(sp_xml, flags=0)
    assert spptr
    sv_xml1 = _get_storagevolxml(name='testExistingVol')
    sv_xml2 = _get_storagevolxml(name='testClonedVol')
    svptr1 = vsobj.create_vol(sv_xml1, flags=0, name='testnpCloneVol')
    assert svptr1
    svptr2 = vsobj.clone_vol(sv_xml2, svptr1, flags=0, name='testnpCloneVol')
    assert svptr2
    assert svptr1.delete() == 0
    assert svptr2.delete() == 0
    assert spptr.destroy() == 0
