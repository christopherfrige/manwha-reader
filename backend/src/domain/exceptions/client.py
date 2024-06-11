from src.domain.exceptions import DefaultException


class BadRequestException(DefaultException):
    ...


class ConflictException(DefaultException):
    ...
