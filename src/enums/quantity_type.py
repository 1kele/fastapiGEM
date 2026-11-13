from enum import Enum


class TypeQuantity(str, Enum):
    SINGLE = "single stone"
    PAIR = "pair"
    LAYOUT = "layout"
    PARCEL = "parcel"
