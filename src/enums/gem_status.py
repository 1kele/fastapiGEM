from enum import Enum


class GemStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESERVED = "reserved"
    SOLD = "sold"
    ARCHIVED = "archived"
