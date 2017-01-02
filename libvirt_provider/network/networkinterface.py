class NetworkInterface(object):
    """Network interface module defines guest side networking definitions.

    Higher level tasks like creation, deletion are implemented as per the
    life-cycle of the lower level definitions. These tasks are bound to the
    libvirt.conn object which defines certain actions. Further, the
    virInterface object is defining specific tasks for the given network
    interface.

    The final XML snippet should look like:
        <interface type='bridge' name='br0'>
          <start mode='onboot'/>
          <protocol family='ipv4'>
            <ip address='10.0.0.1' prefix='16'/>
            <route gateway='10.160.255.254'/>
          </protocol>
          <bridge stp='off' delay='0.00'>
            <interface type='ethernet' name='em1'>
              <mac address='34:17:eb:bb:27:2a'/>
            </interface>
          </bridge>
        </interface>

    Before passing this XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initializing the NetworkInterface module.

    Libvirt connection object or libvirt connection URI is required to
    connect to libvirt on the host.

    Description of various values, properties and flags. These could
    be passed as optional variables. These variables should be used,
    and override defaults unless explicitly overridden.
        {
        name: <str> <network name>,
        uuid: <uuid> <network_uuid>, (RFC 4122)
        ipv6: <bool> <yes,no>,
        }
    """

        # TODO(dbite): Figure out a better way to handle the libvirt.conn
        #              object. Similar to other modules.
        if conn:
            self.conn = conn
        else:
            raise

        self.kwargs = kwargs

    def create(self):

        pass

    def destroy(self):

        pass

    def start(self):

        pass

    def stop(self):

        pass

    def _get_vnetintobj(self):

        pass

    def change_begin(self):

        pass

    def change_commit(self):

        pass

    def change_rollback(self):

        pass
