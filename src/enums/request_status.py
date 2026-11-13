from enum import Enum


class RequestStatus(str, Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
