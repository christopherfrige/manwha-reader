from src.domain.exceptions import DefaultException


class BadRequestException(DefaultException):
    ...


class NotFoundException(DefaultException):
    ...


class NotAcceptableException(DefaultException):
    ...


class ConflictException(DefaultException):
    ...
