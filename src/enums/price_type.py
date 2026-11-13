from enum import Enum


class PriceType(str, Enum):
    CARAT = "price_per_carat"
    TOTAL = "total_price"
