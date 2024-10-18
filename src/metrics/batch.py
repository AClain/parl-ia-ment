from utils.database import (
    batch_from_batch_id,
    questions_from_question_ids,
    parent_theme_from_child_theme_name,
)
from errors.WrongBatchIdProvided import WrongBatchIdProvided


def compute_batch_theme_counts(batch_id: str, level: int):
    batch = batch_from_batch_id(batch_id)
    if batch is None:
        raise WrongBatchIdProvided()

    questions = questions_from_question_ids(batch["question_ids"])

    theme_counts = {}
    total_count = 0
    for question in questions:
        parent_theme = dict(
            parent_theme_from_child_theme_name(question["theme"], level, 0)
        )

        if parent_theme["name"] not in theme_counts.keys():
            theme_counts[parent_theme["name"]] = 0

        theme_counts[parent_theme["name"]] += 1
        total_count += 1

    theme_counts["total_count"] = total_count

    return theme_counts
