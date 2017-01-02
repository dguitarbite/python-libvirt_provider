class Secrets(object):
    """Secret module defines the secrets managed by libvirt.

    The XML snippet should look like:

        <secret ephemeral='no' private='yes'>
          <description>Super secret name of my first puppy</description>
          <uuid>0a81f5b2-8403-7b23-c8d6-21ccc2f80d6f</uuid>
          <usage type='volume'>
            <volume>/var/lib/libvirt/images/puppyname.img</volume>
          </usage>
        </secret>

    Before passing this XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initialize the Secrets module."""

        # TODO(dbite): Re-think the conn object.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    def list_no_of_secrets(self):

        return self.conn.numOfSecrets()

    def list_all_secrets(self, flags=0):

        return self.conn.listAllSecrets(flags=flags)

    def list_secrets(self):

        return self.conn.listSecrets()

    def create(self, xml_desc, flags=0):
        """Define a new Secret."""

        return self.conn.secretDefineXML(xml_desc, flags=flags)

    def destroy(self, **kwargs):
        """Destroy an existing virSecret."""

        vsecretobj = self._get_vsecretobj(**kwargs)

        return vsecretobj.undefine()

    def set_value(self, value, flags=0, **kwargs):

        vsecretobj = self._get_vsecretwobj(**kwargs)

        return vsecretobj.setValue(value, flags=flags)

    def get_usage_id(self, **kwargs):

        vsecretobj = self._get_vsecretobj(**kwargs)

        return vsecretobj.usageID()

    def get_usage_type(self, **kwargs):

        vsecretobj = self._get_vnwobj(**kwargs)

        return vsecretobj.usageType()

    def get_value(self, flags=0, **kwargs):

        vsecretobj = self._get_vnwobj(**kwargs)

        return vsecretobj.value(flags=flags)

    def _get_vsecretobj(self, **kwargs):
        """Helper function to get virSecret object.

        Accepts the following arguments, but only uses one (random).
        {
            usage: <Name by usageType, usageID>,
            uuid: <uuid of the NWFilter>,
            uuid_str: <uuid in string format of the network>
        }
        """

        lookup_table = {
            'name': self.conn.secretLookUpByUsage,
            'uuid': self.conn.secretLookUpByUUID,
            'uuid_str': self.conn.secretLookUpByUUIDString
        }

        key, value = kwargs.popitem()

        return lookup_table[key](value)
