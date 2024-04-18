class PollError(Exception):
    """Custom error for issues related to poll creation or processing."""
    pass

class CommunicationError(Exception):
    """Custom error for issues with sending messages or communicating with groups."""
    pass
