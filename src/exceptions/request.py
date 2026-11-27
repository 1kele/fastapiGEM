from src.exceptions.base import BusinessValidationError

class InvalidStatusTransitionError(BusinessValidationError):
    pass

class InvalidWeightRangeError(BusinessValidationError):
    pass
