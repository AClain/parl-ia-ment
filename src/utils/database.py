from typing import List
from bson import ObjectId
from pymongo.results import InsertOneResult
from tqdm import tqdm
from models.Batch import Batch
from models.Theme import Theme
from models.Question import Question
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from models.Prompt import PromptResult, PromptRun, Prompt
from errors.WrongBatchIdProvided import WrongBatchIdProvided

connector = Connector(ExportFormat.JSON)


def prompt_runs_from_ids(run_ids: str) -> List[PromptRun]:
    prompt_runs = connector.client.get_prompt_runs(
        {"_id": {"$in": [ObjectId(run_id) for run_id in run_ids]}}
    )

    return list(prompt_runs)


def prompt_run_from_run_id(run_id: str) -> PromptRun:
    return connector.client.get_prompt_run({"_id": ObjectId(run_id)})


def batch_from_batch_id(batch_id: str) -> Batch:
    return connector.client.get_batch({"_id": ObjectId(batch_id)})


def prompt_results_from_run_id(run_id: str) -> List[PromptResult]:
    """
    Retrieve prompt results from the database based on a list of run IDs.

    Parameters
    ----------
    run_ids: List[str]
        A list of run IDs for which to fetch the corresponding prompt results.

    Returns
    -------
    List[PromptResult]
        A list of `PromptResult` objects that match the given run IDs.
    """
    prompt_results = connector.client.get_prompt_results({"run_id": run_id})

    return list(prompt_results)


def prompt_results_from_run_ids(run_ids: List[str]) -> List[PromptResult]:
    """
    Retrieve prompt results from the database based on a list of run IDs.

    Parameters
    ----------
    run_ids: List[str]
        A list of run IDs for which to fetch the corresponding prompt results.

    Returns
    -------
    List[PromptResult]
        A list of `PromptResult` objects that match the given run IDs.
    """
    prompt_results = connector.client.get_prompt_results({"run_id": {"$in": run_ids}})

    return list(prompt_results)


def themes_list_from_run_id(run_id: str) -> List[str]:
    run = connector.client.get_prompt_run({"_id": ObjectId(run_id)})

    return run["themes_list"]


def batch_from_id(batch_id: str) -> Batch:
    batch = connector.client.get_batch({"_id": ObjectId(batch_id)})

    return batch


def batches_from_batch_ids(batch_ids: List[str]) -> List[Batch]:
    batch_ids = [ObjectId(batch_id) for batch_id in batch_ids]
    batches = connector.client.get_batches({"_id": {"$in": batch_ids}})

    return list(batches)


def questions_from_question_ids(question_ids: List[str]) -> List[Question]:
    questions = connector.client.get_questions({"id": {"$in": question_ids}})

    return list(questions)


def themes_from_names(
    theme_names: List[str], themes_hierarchy_level: int = 0
) -> List[Theme]:
    themes = connector.client.get_themes(
        {"name": {"$in": theme_names}, "level": themes_hierarchy_level}
    )

    return list(themes)


def themes_from_identifiers(theme_identifiers: List[str]) -> List[Theme]:
    themes = connector.client.get_themes(
        {"unique_identifier": {"$in": theme_identifiers}}
    )

    return list(themes)


def prompt_from_unique_identifier(unique_identifier: str) -> Prompt:
    prompt = connector.client.get_prompt({"unique_identifier": unique_identifier})

    return prompt


def parent_theme_from_child_theme_name(
    child_theme_name: str, stop_at_level: int = 3, base_theme_level: int = 0
) -> Theme:
    parent_theme = connector.client.get_parent_theme_from_child_theme_name(
        child_theme_name, stop_at_level=stop_at_level, base_theme_level=base_theme_level
    )

    return parent_theme


def add_question_ids_to_batch(question_ids: List[str], batch_id: ObjectId):
    batch = batch_from_batch_id(batch_id)
    if batch is None:
        raise WrongBatchIdProvided()

    connector.client.add_question_ids_to_batch(question_ids, batch_id)


def stratified_sample(
    n: int,
    legislature: int,
    themes_list: List[str],
    level: int
) -> List[Question]:
    """
    Build a stratified sampled batch.

    Parameters
    ----------
    n: int
        Total size of the batch.
    legislature: int
        Number of the parliamentary term.
    themes_list: List[str]
        List of high-level themes name.
    level: int
        Level at which to stop to match high-level themes name.

    Returns
    -------
    List[Question]
        A list of questions stratified for each theme.
    """
    questions = []
    all_accepted_themes = []

    stratified_samples_size = n // len(themes_list)

    for theme_name in tqdm(themes_list):
        theme = connector.client.get_theme(
            {"name": theme_name, "level": level}
        )
        theme = dict(theme)  # type: ignore

        accepted_themes_for_questions = []
        sub_themes = connector.client.get_sub_themes_list_from_theme(
            theme["unique_identifier"],  # type: ignore
            flatten=True
        )

        for sub_theme in sub_themes:
            if sub_theme["name"] not in accepted_themes_for_questions:
                accepted_themes_for_questions.append(sub_theme["name"])

        all_accepted_themes += accepted_themes_for_questions

        random_questions = connector.client.get_random_questions(
            number_of_questions=stratified_samples_size,
            accepted_themes=accepted_themes_for_questions,
            legislature=legislature
        )
        random_questions = list(random_questions)
        questions += random_questions

    if len(questions) < n:
        rest = n - len(questions)
        random_questions = connector.client.get_random_questions(
            number_of_questions=rest,
            legislature=legislature,
            accepted_themes=all_accepted_themes,
        )
        random_questions = list(random_questions)
        questions += random_questions

    return [Question(**q) for q in questions]


def add_batch_to_database(
    questions: List[Question],
    legislature: int,
    comment: str | None,
) -> InsertOneResult:
    """
    Add a given batch to the database.

    Parameters
    ----------
    questions: List[Question]
        A list of questions.
    legislature: int
        The parliamentary term number.
    comment: str | None
        A comment to describe the inserted batch.
    level: int
        Level of the high-level themes list names.

    Returns
    -------
    InsertOneResult
        PyMongo metadata regarding the insertion operation.
    """
    question_ids = [question.id for question in questions]
    if comment is None:
        comment = f"sample batch for legislature {legislature}"
 
    batch = Batch(
        question_ids=question_ids,
        size=len(question_ids),
        comment=comment,
    )
    inserted_batch = connector.client.add_batch(batch)
    return inserted_batch
