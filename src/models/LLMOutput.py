from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class LogProb(BaseModel):
    token: str
    bytes: Optional[List[int]] = None
    logprob: float


class TokenMetrics(BaseModel):
    token: str
    bytes: Optional[List[int]] = None
    logprob: float
    top_logprobs: List[LogProb]


class ConfidenceType(str, Enum):
    Verbalized = "verbalized"
    Logprobs = "logprobs"
    SelfCalibration = "self-calibration"
    SelfConsistency = "self-consistency"


class WrapperOutput(BaseModel):
    raw_response: str
    prompt_tokens: int
    response_tokens: int
    predicted_label: str
    logprobs: Optional[List[TokenMetrics]] = None
