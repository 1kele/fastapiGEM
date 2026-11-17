class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class UniqueViolationError(AppError):
    pass
