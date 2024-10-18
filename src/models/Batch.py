from typing import List
from pydantic import BaseModel


class Batch(BaseModel):
    question_ids: List[str]
    size: int
    comment: str | None = None
