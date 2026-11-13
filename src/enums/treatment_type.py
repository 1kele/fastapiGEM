from enum import Enum


class TreatmentType(str, Enum):
    UNHEATED = "unheated"
    HEATING = "heating"
    OILING = "oiling"
    IRRADIATION = "irradiation"
    BLEACHING = "bleaching"
    WAXING = "waxing"
    FRACTURE_FILLING = "fracture_filling"
    GLASS_FILLING = "glass_filling"
    DYEING = "dyeing"
    DIFFUSION = "diffusion"
    HPHT = "hpht"
    LASER_DRILLING = "laser_drilling"
    UNKNOWN = "unknown"
