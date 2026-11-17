from enum import Enum


class QuantityType(str, Enum):
    SINGLE = "single stone"
    PAIR = "pair"
    LAYOUT = "layout"
    PARCEL = "parcel"
