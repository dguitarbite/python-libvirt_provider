class Stream(object):
    """Stream module opens or closes streams to domains.

    The XML snippet should look like:


    Before passing this XML snippet to libvirt, XML overlay mechanism should
    allow further customization for the same.
    """

    def __init__(self, conn, **kwargs):
        """Initialize the Stream module."""

        # TODO(dbite): Re-think the conn object.
        if conn:
            self.conn = conn
        else:
            raise   # Raise the correct exception here.

        self.kwargs = kwargs

    def create(self, flags=0):
        """Define a new Stream."""

        return self.conn.newStream(flags=flags)

    def destroy(self, vstreamobj):
        """Destroy an existing virStream."""

        return vstreamobj.abort()

    def event_add_callback(self, vstreamobj, events):
        """Add event callback."""

        return vstreamobj.eventAddCallback(vstreamobj, events)

    def event_remove_callback(self, vstreamobj):
        """Remove event callback."""

        return vstreamobj.eventRemoveCallBack()

    def event_update_callback(self, events, vstreamobj):
        """Update event callback."""

        return vstreamobj.eventUpdateCallback(events)

    def finish(self, vstreamobj):
        """Close the stream connection.

        For input stream this should be called once the virStreamRecv gives
        EOL.

        For output stream this should be called once all the data has been
        written.
        """

        return self.finish()

    def receive(self, vstreamobj, nbytes):
        """Opens a stream to receive data."""

        return self.vstreamobj.recv(nbytes)

    def receive_all(self, vstreamobj, stream, buf, opaque):
        """Recieve the entire data stream."""

        def handler(stream,  # virStream instance
                    buf,     # string containing received data.
                    opaque):  # extra data passed to recvAll as opaque.
            import os

            fd = opaque

            return os.write(fd, buf)

        return self.recieve_all(handler, opaque)
