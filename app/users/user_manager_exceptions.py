class UserManagerException(Exception):
    pass


class NotFoundException(UserManagerException):
    pass


class ConflictException(UserManagerException):
    pass


class ServiceUnavailableException(UserManagerException):
    pass


class BadRequestException(UserManagerException):
    pass
