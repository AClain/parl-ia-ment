import pytest
from typing import List
from models.Result import ResultAndConfidence


@pytest.fixture
def confidence_data() -> List[ResultAndConfidence]:
    data = [
        {
            "question_id": "A",
            "confidence": 0.78,
            "predicted_label": "0",
            "gold_label": "0"
        },
        {
            "question_id": "B",
            "confidence": 0.64,
            "predicted_label": "1",
            "gold_label": "1"
        },
        {
            "question_id": "C",
            "confidence": 0.92,
            "predicted_label": "1",
            "gold_label": "0"
        },
        {
            "question_id": "D",
            "confidence": 0.58,
            "predicted_label": "0",
            "gold_label": "0"
        },
        {
            "question_id": "E",
            "confidence": 0.51,
            "predicted_label": "1",
            "gold_label": "0"
        },
        {
            "question_id": "F",
            "confidence": 0.85,
            "predicted_label": "0",
            "gold_label": "0"
        },
        {
            "question_id": "G",
            "confidence": 0.70,
            "predicted_label": "1",
            "gold_label": "1"
        },
        {
            "question_id": "H",
            "confidence": 0.63,
            "predicted_label": "0",
            "gold_label": "1"
        },
        {
            "question_id": "I",
            "confidence": 0.83,
            "predicted_label": "1",
            "gold_label": "1"
        }
    ]
    return [ResultAndConfidence(d) for d in data]  # type: ignore
