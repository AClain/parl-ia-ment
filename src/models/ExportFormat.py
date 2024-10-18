from enum import Enum


class ExportFormat(str, Enum):
    MONGO = "mongo"
    JSON = "json"
    CSV = "csv"
