import json
from models.Question import Question


def export_to_json(
    question: Question,
    destination: str = "question"
) -> None:
    """
    Export questions metadata to JSON file.

    Parameters
    ----------
    question: Question
        The question and its associated metadata.
    destination: str, default="questions"
        Path to JSON file export.
    """
    with open(f"data/{destination}_{question.id}.json", "w") as file:
        json_data = json.dumps(question.model_dump(), indent=2)
        file.write(json_data)
