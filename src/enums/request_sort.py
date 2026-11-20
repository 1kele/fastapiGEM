from enum import Enum


class RequestSortField(str, Enum):
    PRICE = "price_total"
    WEIGHT = "weight"
