from src.domain.exceptions import DefaultException


class BadRequestException(DefaultException):
    ...


class NotFoundException(DefaultException):
    ...


class ConflictException(DefaultException):
    ...
