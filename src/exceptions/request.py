from src.exceptions.base import AppError


class InvalidStatusTransitionError(AppError):
    pass


class BusinessValidationError(Exception):
    pass


class InvalidWeightRangeError(BusinessValidationError):
    pass
