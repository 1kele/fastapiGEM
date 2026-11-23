from enum import Enum


class RequestStatus(str, Enum):
    CREATED = "created"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
