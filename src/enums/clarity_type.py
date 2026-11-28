from enum import Enum


class ClarityType(str, Enum):
    # Diamond clarity
    FL = "FL"
    IF = "IF"
    VVS1 = "VVS1"
    VVS2 = "VVS2"
    VS1 = "VS1"
    VS2 = "VS2"
    SI1 = "SI1"
    SI2 = "SI2"
    I1 = "I1"
    I2 = "I2"
    I3 = "I3"

    # Colored gemstone clarity
    VVS = "VVS"
    VS = "VS"

    # Visual clarity
    EYE_CLEAN = "eye_clean"
    SLIGHTLY_INCLUDED = "slightly_included"
    MODERATELY_INCLUDED = "moderately_included"
    HEAVILY_INCLUDED = "heavily_included"
