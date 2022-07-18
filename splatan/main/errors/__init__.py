class PlayerExistsError(ValueError):
    """Raised when a player tries to enroll with a name that is already taken"""


class EnrollmentNotOpenError(Exception):
    """Raised when a player tries to enroll before enrollment is open"""


class NotHostError(ValueError):
    """Raised when a player tries to do something only the host should do"""


class PlayerDoesNotExistError(ValueError):
    """Raised when a request comes from a player that never enrolled"""
