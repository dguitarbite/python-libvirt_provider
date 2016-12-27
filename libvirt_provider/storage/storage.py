class Storage(object):
    """Storage class manages storage pool & vol related tasks of libvirt.

    Higher level tasks like creation, deletion are implemented as per the
    life-cycle of the lower level definitions. These tasks are bound to the
    libvirt.conn object and usually deal with certain type of tasks like
    creation, deletion, searching etc.

    The finer details for storage pool are fetched from the higher level
    methods which provide the virStoragePool object and they enable more
    possibilities in managing the storage pool, and its underlying resources
    (storage volumes).

    Various properties and flags which define the interaction of storage pools
    and the underlying volumes are concerned with various tasks like active,
    inactive, autostart, list volumes, create, destroy etc. for both the
    given storage pool and the underlying volumes.

    Example XML snippet (Storage Pool):
        <pool type="dir">
          <name>virtimages</name>
          <target>
            <path>/var/lib/virt/images</path>
          </target>
        </pool>

    Example XML snippet(Storage Volume):
        <volume>
          <name>sparse.img</name>
          <allocation>0</allocation>
          <capacity unit="T">1</capacity>
          <target>
            <path>/var/lib/virt/images/sparse.img</path>
            <permissions>
              <owner>107</owner>
              <group>107</group>
              <mode>0744</mode>
              <label>virt_image_t</label>
            </permissions>
          </target>
        </volume>



    Before passing the XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initializing the StoragePool module.

    Libvirt connection object or libvirt connection URI is required to connect
    to libvirt on the host.

    Description of various values, properties and flags could be passed as
    optional variables. These variables should be used, and override defaults
    unless explicitly overridden.
    """

        # TODO(dbite): Rethink the libvirt.conn object handling and it's scope.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    ###########################################################################
    #   Storage Pool
    ###########################################################################

    def create_pool(self, xml_desc, flags=0):
        """Define new storage pool."""
        # TODO(dbite): Figure out a nice way to handle the flags.

        return self.conn.storagePoolDefineXML(xml_desc, flags)

    def destroy_pool(self, **kwargs):
        """Undefine an existing storage domain by name, uuid or uuidstr."""

        vspobj = self._get_vspobj(**kwargs)

        return vspobj.undefine()

    def start_pool(self, xml_desc, flags=0):
        """Create a storage pool.

        Starts an existing storage pool. Creates a non-persistent domain if
        not existing.
        """

        return self.conn.storagePoolCreateXML(xml_desc, flags)

    def stop_pool(self, **kwargs):
        """Destroy an existing storage pool domain."""

        vspobj = self._get_vspobj(**kwargs)

        return vspobj.destroy()

    def _get_vspobj(self, **kwargs):
        """Helper function to get virStoragePool object.

        Accepts the following arguments, but only uses one (random).
        {
            name: <name of the storage pool>,
            uuid: <uuid of the storage pool>,
            uuid_str: <uuid in string format of the storage pool>
        }
        """

        lookup_table = {
            'name': self.conn.storagePoolLookupByName,
            'uuid': self.conn.storagePoolLookupByUUID,
            'uuid_str': self.conn.storagePoolLookupByUUIDString,
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)

    ###########################################################################
    #   Storage Volume
    ###########################################################################

    def create_vol(self, xml_desc, flags=0, **kwargs):
        """Defines a new persistent storage volume."""

        vspobj = self._get_vspobj(**kwargs)

        return vspobj.createXML(xml_desc, flags)

    def clone_vol(self, xml_desc, clonevol, flags=0, **kwargs):
        """Create a new volume by copying an existing volume (clone)."""

        vspobj = self._get_vspobj(**kwargs)

        return vspobj.createXMLFrom(xml_desc, clonevol, flags=0)

    def destroy_vol(self, vspobj=None, **kwargs):
        """Undefine an existing storage domain by name, uuid or uuidstr."""

        vsvobj = self._get_vsvobj(vspobj, **kwargs)

        return vsvobj.delete()

    def _get_vsvobj(self, vspobj=None, **kwargs):
        """Helper function to get virStorageVol object.

        Accepts the following arguments, but only uses one (random).
        {
            'name': <lookup by name, must provide vspobj>,
            'key': <globally unique key>,
            'path': <path of the storage volume>,
        }
        """

        if 'name' in kwargs and not vspobj:
            raise  # Custom exception, needs vspobj to lookup by name!

        lookup_table = {
            'name': vspobj.storageVolLookupByName,
            'key': self.conn.storageVolLookupByKey,
            'path': self.conn.storageVolLookupByPath,
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)
