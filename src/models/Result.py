from typing import List, TypedDict
from pydantic import BaseModel
from models.Prompt import Prompt


class CustomRunResult(BaseModel):
    prompt_id: str
    run_id: str
    predicted_label: str
    gold_label: str
    prompt: str


class QuestionResult(BaseModel):
    question_id: str
    question_text: str
    database_label: str
    results: List[CustomRunResult]

    def __eq__(self, other):
        return self.question_id == other.question_id

    def __hash__(self):
        return hash(
            ('question_id', self.question_id,
            'question_text', self.question_text,
            'database_label', self.database_label)
        )

class ResultAndConfidence(TypedDict):
    question_id: str
    confidence: float
    predicted_label: str
    gold_label: str


class RunData(TypedDict):
    prompts: List[Prompt]
    name: str
    run_id: str
