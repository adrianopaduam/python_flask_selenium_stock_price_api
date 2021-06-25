""" API known exceptions module """


class InternalError(Exception):
    pass


class UserError(Exception):
    pass


class LogFileCreationError(InternalError):
    pass


class DriverGenerationError(InternalError):
    pass


class ElementNotFoundError(InternalError):
    pass


class InexistentRegionError(UserError):
    pass
