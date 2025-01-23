class BaseApiException(Exception):
    pass


class NotFoundException(BaseApiException):
    pass


class ConflictException(BaseApiException):
    pass


class ServiceUnavailableException(BaseApiException):
    pass


class BadRequestException(BaseApiException):
    pass
