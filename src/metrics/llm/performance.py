import pandas as pd
from utils.helpers import sort_list
from typing import List
from errors.WrongRunIdProvided import WrongRunIdProvided
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    precision_recall_fscore_support,
)
from tqdm import tqdm
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from utils.database import (
    prompt_results_from_run_ids,
    prompt_run_from_run_id,
)
from models.Metrics import (
    PrecisionComputed,
    RecallComputed,
    FScoreComputed,
    SupportComputed,
)
from models.Metrics import AverageMetricEnum

connector = Connector(ExportFormat.JSON)

def compute_precision_to_df_from_run_ids(run_ids: List[str]) -> pd.DataFrame:
    """
    Compute precision scores for each theme across multiple prompt runs and return the results as a DataFrame.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs from which to compute precision scores.

    Raises:
    ------
    WrongRunIdProvided
        If any of the provided run_ids is invalid or does not match a prompt run.

    Returns
    -------
    pd.DataFrame
        A DataFrame where each row represents a prompt run and each column represents a theme.
        The values are the precision scores for each theme across the specified runs.
    """
    runs = [prompt_run_from_run_id(run_id) for run_id in run_ids]
    if len(runs) < len(run_ids):
        raise WrongRunIdProvided()

    precision_list = {}

    run_names = [run["name"] for run in runs]
    run_ids = [str(run["_id"]) for run in runs]
    for run_id in run_ids:
        themes_precision = compute_precision(run_id)

        for i, theme in enumerate(themes_precision["themes"]):
            if theme not in precision_list:
                precision_list[theme] = []

            precision_list[theme].append(themes_precision["precisions"][i])

    precisions_df = pd.DataFrame(precision_list)
    precisions_df.index = run_names

    return precisions_df


def compute_recall_to_df_from_run_ids(run_ids: List[str]) -> pd.DataFrame:
    """
    Compute recall scores for each theme across multiple prompt runs and return the results as a DataFrame.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs from which to compute recall scores.

    Raises:
    ------
    WrongRunIdProvided
        If any of the provided run_ids is invalid or does not match a prompt run.

    Returns
    -------
    pd.DataFrame
        A DataFrame where each row represents a prompt run and each column represents a theme.
        The values are the recall scores for each theme across the specified runs.
    """
    runs = [prompt_run_from_run_id(run_id) for run_id in run_ids]
    if len(runs) < len(run_ids):
        raise WrongRunIdProvided()

    recalls_list = {}

    run_names = [run["name"] for run in runs]
    run_ids = [str(run["_id"]) for run in runs]
    for run_id in run_ids:
        themes_recall = compute_recall(run_id)

        for i, theme in enumerate(themes_recall["themes"]):
            if theme not in recalls_list:
                recalls_list[theme] = []

            recalls_list[theme].append(themes_recall["recalls"][i])

    recalls_df = pd.DataFrame(recalls_list)
    recalls_df.index = run_names

    return recalls_df


def compute_fscore_to_df_from_run_ids(run_ids: List[str]) -> pd.DataFrame:
    """
    Compute F1 scores for each theme across multiple prompt runs and return the results as a DataFrame.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs from which to compute F1 scores.

    Raises:
    ------
    WrongRunIdProvided
        If any of the provided run_ids is invalid or does not match a prompt run.

    Returns
    -------
    pd.DataFrame
        A DataFrame where each row represents a prompt run and each column represents a theme.
        The values are the F1 scores for each theme across the specified runs.
    """
    runs = [prompt_run_from_run_id(run_id) for run_id in run_ids]
    if len(runs) < len(run_ids):
        raise WrongRunIdProvided()

    fscores_list = {}

    run_names = [run["name"] for run in runs]
    run_ids = [str(run["_id"]) for run in runs]
    for run_id in run_ids:
        themes_fscore = compute_f1_score(run_id)

        for i, theme in enumerate(themes_fscore["themes"]):
            if theme not in fscores_list:
                fscores_list[theme] = []

            fscores_list[theme].append(themes_fscore["fscores"][i])

    fscores_df = pd.DataFrame(fscores_list)
    fscores_df.index = run_names

    return fscores_df


def compute_precision(run_id: str) -> PrecisionComputed:
    """
    Compute the precision scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.

    Returns
    -------
    PrecisionComputed
        A dictionary containing the list of themes and their corresponding precision scores.
    """

    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    prompt_results = prompt_results_from_run_ids([run_id])

    unique_labels = set([x["gold_label"] for x in prompt_results])
    unique_labels_sorted_list = sort_list(list(unique_labels))

    precision = precision_score(
        [x["gold_label"] for x in prompt_results],
        [x["final_answer"].strip() for x in prompt_results],
        labels=unique_labels_sorted_list,
        average=None,
        zero_division=0,
    )

    themes = unique_labels_sorted_list
    precisions = precision

    return {"themes": themes, "precisions": precisions}


def compute_average_precision(
    run_ids: List[str], average: AverageMetricEnum = AverageMetricEnum.Weighted
):
    run_names = []
    average_precisions = []
    for run_id in run_ids:
        run = prompt_run_from_run_id(run_id)
        if run is None:
            raise WrongRunIdProvided()

        prompt_results = prompt_results_from_run_ids([run_id])

        precision = precision_score(
            y_true=[x["gold_label"] for x in prompt_results],
            y_pred=[x["final_answer"].strip() for x in prompt_results],
            average=average.value,
            zero_division=0,
        )

        run_names.append(run["name"])
        average_precisions.append(precision)

    return {"run_names": run_names, "precisions": average_precisions}


def compute_recall(run_id: str) -> RecallComputed:
    """
    Compute the recall scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.

    Returns
    -------
    RecallComputed
        A dictionary containing the list of themes and their corresponding recall scores.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    prompt_results = prompt_results_from_run_ids([run_id])

    unique_labels = set([x["gold_label"] for x in prompt_results])
    unique_labels_sorted_list = sort_list(list(unique_labels))

    recall = recall_score(
        y_true=[x["gold_label"] for x in prompt_results],
        y_pred=[x["final_answer"].strip() for x in prompt_results],
        labels=unique_labels_sorted_list,
        average=None,
        zero_division=0,
    )

    themes = unique_labels_sorted_list
    recalls = recall

    return {"themes": themes, "recalls": recalls}


def compute_average_recall(
    run_ids: List[str], average: AverageMetricEnum = AverageMetricEnum.Weighted
):
    run_names = []
    average_recalls = []
    for run_id in run_ids:
        run = prompt_run_from_run_id(run_id)
        if run is None:
            raise WrongRunIdProvided()

        prompt_results = prompt_results_from_run_ids([run_id])

        recall = recall_score(
            y_true=[x["gold_label"] for x in prompt_results],
            y_pred=[x["final_answer"].strip() for x in prompt_results],
            average=average.value,
            zero_division=0,
        )

        run_names.append(run["name"])
        average_recalls.append(recall)

    return {"run_names": run_names, "recalls": average_recalls}


def compute_f1_score(run_id: str) -> FScoreComputed:
    """
    Compute the F1 scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.

    Returns
    -------
    FScoreComputed
        A dictionary containing the list of themes and their corresponding F1 scores.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    prompt_results = prompt_results_from_run_ids([run_id])

    unique_labels = set([x["gold_label"] for x in prompt_results])
    unique_labels_sorted_list = sort_list(list(unique_labels))

    fscore = f1_score(
        [x["gold_label"] for x in prompt_results],
        [x["final_answer"].strip() for x in prompt_results],
        labels=unique_labels_sorted_list,
        average=None,
        zero_division=0,
    )

    themes = unique_labels_sorted_list
    fscores = fscore

    return {"themes": themes, "fscores": fscores}


def compute_average_f1_score(
    run_ids: List[str], average: AverageMetricEnum = AverageMetricEnum.Weighted
):
    run_names = []
    average_fscores = []
    for run_id in run_ids:
        run = prompt_run_from_run_id(run_id)
        if run is None:
            raise WrongRunIdProvided()

        prompt_results = prompt_results_from_run_ids([run_id])

        fscore = f1_score(
            y_true=[x["gold_label"] for x in prompt_results],
            y_pred=[x["final_answer"].strip() for x in prompt_results],
            average=average.value,
            zero_division=0,
        )

        run_names.append(run["name"])
        average_fscores.append(fscore)

    return {"run_names": run_names, "fscores": average_fscores}


def compute_support_count(run_id: str) -> SupportComputed:
    """
    Compute the support count for a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.

    Returns
    -------
    SupportComputed
        A dictionary containing the list of themes and their corresponding support count.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    prompt_results = prompt_results_from_run_ids([run_id])

    unique_labels = set([x["gold_label"] for x in prompt_results])
    unique_labels_sorted_list = sort_list(list(unique_labels))

    _, _, _, support = precision_recall_fscore_support(
        [x["gold_label"] for x in prompt_results],
        [x["final_answer"] for x in prompt_results],
        labels=unique_labels_sorted_list,
        zero_division=0,
    )

    themes = unique_labels_sorted_list
    support_count = support

    return {
        "themes": themes,
        "support_count": support_count,
        "batch_id": run["batch_id"],
    }

def _sklearn_metrics_table(run_id: str, sort_by_metric: str):
    prompt_results = connector.client.get_prompt_results({"run_id": run_id})
    prompt_results = list(prompt_results)

    y_true = [result["gold_label"] for result in prompt_results]
    y_pred = [result["final_answer"] for result in prompt_results]

    precision, recall, fscore, support = precision_recall_fscore_support(
        y_true, y_pred, average=None
    )

    labels = sorted(set(y_true))

    metrics_table = {}

    for i, label in enumerate(tqdm(labels)):
        metrics_table[label] = {
            "precision": precision[i],
            "recall": recall[i],
            "fscore": fscore[i],
            "support": support[i],
        }

    sorted_metrics = dict(
        sorted(
            metrics_table.items(),
            key=lambda item: item[1][sort_by_metric],
            reverse=True,
        )
    )

    return sorted_metrics

def get_metric(run_id: str, metric: str):
    metric_table = _sklearn_metrics_table(run_id, metric)
    matrix_data = {
        "themes": [],
        "metrics": [],
    }

    for theme_name, theme_metrics in metric_table.items():
        matrix_data["themes"].append(theme_name)
        matrix_data["metrics"].append(float(theme_metrics[metric]))
    return matrix_data
