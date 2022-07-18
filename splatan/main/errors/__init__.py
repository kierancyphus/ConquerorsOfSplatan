class PlayerExistsError(ValueError):
    """Raised when a player tries to enroll with a name that is already taken"""


class EnrollmentNotOpenError(Exception):
    """Raised when a player tries to enroll before enrollment is open"""
