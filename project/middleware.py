"""Web server middleware."""


class ConnectionManager:
    """Create a scoped session for every request."""

    def __init__(self, sess):
        self.sess = sess

    def process_resource(self, req, *_):
        """
        save db sess for further usage
        """
        req.context["sess"] = self.sess

    def process_response(self, *_):
        """
        release connection and back to pool for other process to use
        """
        self.sess.remove()
