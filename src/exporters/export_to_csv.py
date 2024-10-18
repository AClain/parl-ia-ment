from pandas import DataFrame
from models.Question import Question


def export_to_csv(question: Question, filename: str) -> None:
    """
    Export a question metadata to a CSV file.

    Parameters
    ----------
    question: Question
        The question and its associated metadata.
    filename: str
        Path to the CSV file.
    """
    with open(filename, "a") as file:
        table = DataFrame(question.model_dump())
        file.write(table.to_string())
