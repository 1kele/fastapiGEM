from enum import Enum


class RequestSortField(str, Enum):
    PRICE = "price"
    WEIGHT = "weight"
