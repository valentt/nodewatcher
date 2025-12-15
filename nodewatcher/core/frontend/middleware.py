class ClientNodeMiddleware:
    """
    Adds ``node`` attribute to ``request`` with the node the client is connected to.

    Set to ``None`` if client is not coming from the network.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: Implement
        request.node = None
        return self.get_response(request)
