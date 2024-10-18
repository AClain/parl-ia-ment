from enum import Enum
from pydantic import BaseModel, field_serializer
from typing import Any, Optional, List


class WrapperEnum(str, Enum):
    OpenAI = "openai"
    Anthropic = "anthropic"
    Google = "google"
    Mistral = "mistral"


class RoleEnum(str, Enum):
    System = "system"
    Assistant = "assistant"
    User = "user"
    Model = "model"


class PromptLanguage(Enum):
    French = "fr"
    English = "en"


class PromptType(str, Enum):
    ZeroShot = "zero-shot"
    OneShot = "one-shot"
    FewShot = "few-shot"
    ChainOfThought = "chain-of-thought"
    SelfCalibration = "self-calibration"
    VerbalizedConfidence = "verbalized confidence"


class CotExplanation(BaseModel):
    question_id: str
    legislature: int
    label: str
    question_text: str
    explanation: str


class PromptText(BaseModel):
    role: RoleEnum
    content: str


class Prompt(BaseModel):
    unique_identifier: str
    prompts: List[PromptText]


class PromptRunParameters(BaseModel):
    temperature: float
    model: str
    types: List[PromptType]
    theme_hierarchy_level: int
    wrapper: WrapperEnum

    @field_serializer("wrapper")
    def export_wrapper_as_string(self, value: WrapperEnum):
        return value.value


class PromptRun(BaseModel):
    parameters: PromptRunParameters
    prompt_id: str
    batch_id: str
    timestamp: int
    themes_list: List[str]
    description: str | None = None
    name: str


class PromptResult(BaseModel):
    question_id: str
    response: str
    final_answer: str
    prompt_id: str
    batch_id: str
    run_id: str
    response_tokens: int
    prompt_tokens: int
    legislature: int
    logprobs: Optional[List[Any]] = None
    question_theme: str
    gold_label: str


class FailedGenerations(BaseModel):
    question_id: str


class PromptRunInfo(BaseModel):
    run_id: str
    prompts: List[PromptText]
    prompt_run: PromptRun
