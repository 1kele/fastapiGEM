class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass


class ConflictError(AppError):
    pass


class BusinessValidationError(AppError):
    pass


class UniqueViolationError(ConflictError):
    pass


class InvalidStatusTransitionError(ConflictError):
    pass