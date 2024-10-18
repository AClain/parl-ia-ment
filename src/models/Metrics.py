from enum import Enum
from typing import List, TypedDict


class PrecisionComputed(TypedDict):
    themes: List[str]
    precisions: List[float]


class RecallComputed(TypedDict):
    themes: List[str]
    recalls: List[float]


class FScoreComputed(TypedDict):
    themes: List[str]
    fscores: List[float]


class SupportComputed(TypedDict):
    themes: List[str]
    support_count: List[int]
    batch_id: str


class AverageMetricEnum(str, Enum):
    Macro = "macro"
    Micro = "micro"
    Weighted = "weighted"
