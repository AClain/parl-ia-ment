import numpy as np
from tqdm import tqdm
from typing import List
from collections import Counter
from models.Prompt import PromptResult
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from sklearn.metrics import precision_recall_fscore_support
from sklearn.calibration import calibration_curve
from metrics.softmax import softmax

connector = Connector(ExportFormat.JSON)


def compute_prompt_run_average_logprob_confidence(prompt_run_id: str) -> float:
    prompt_results = connector.client.get_prompt_results({"run_id": prompt_run_id})
    prompt_results = [PromptResult(**pr) for pr in prompt_results]
    return compute_average_logprob_confidence(prompt_results)


def compute_average_logprob_confidence(prompt_results: List[PromptResult]) -> float:
    confidences = []
    for prompt_result in prompt_results:
        all_logprobs = []
        for logprob in prompt_result.logprobs:
            logprob_array = [x["logprob"] for x in logprob["top_logprobs"]]
            all_logprobs.append(softmax(np.array(logprob_array)))

        logprobs_prod = np.array(all_logprobs).transpose()[0].prod()

        confidence = np.power(logprobs_prod, 1 / len(all_logprobs))
        confidences.append(float(confidence))

    return round(np.array(confidences).mean(), 3)


def generate_metrics_table(prompt_results: List[PromptResult], sort_by: str = "fscore"):
    """
    Generate the metrics for each theme present in a batch of prompt results.

    Metrics:
    - True positives, false positives, false negatives, true negatives
    - Precision, recall, F1-score, accuracy
    - Average confidence score for predictions

    :param prompt_results: List of results from prompt evaluations
    :param sort_by: Metric to sort the final output by (default: fscore)
    :param stop_at_level: Maximum hierarchy level to consider for themes
    :return: Sorted dictionary of themes with their corresponding metrics
    """
    themes_precision_table = {
        x["final_answer"]: {
            "true_positive": 0,
            "false_positive": 0,
            "false_negative": 0,
            "true_negative": 0,
            "retrieved": 0,
            "total": 0,
            "average_confidence": 0,
        }
        for x in prompt_results
    }

    print("Pre-generating metrics table...")
    for prompt_result in tqdm(prompt_results):
        response_theme = prompt_result["final_answer"]

        question_theme = prompt_result["gold_label"]

        if question_theme not in themes_precision_table.keys():
            continue

        themes_precision_table[response_theme]["average_confidence"] += prompt_result[
            "confidence"
        ]
        themes_precision_table[question_theme]["total"] += 1
        themes_precision_table[response_theme]["retrieved"] += 1

        if response_theme == question_theme:
            themes_precision_table[response_theme]["true_positive"] += 1
        else:
            themes_precision_table[response_theme]["false_positive"] += 1
            themes_precision_table[question_theme]["false_negative"] += 1

    print("Generating metrics table...")
    for theme, stats in tqdm(themes_precision_table.items()):
        retrieved = stats["retrieved"]
        total = stats["total"]

        stats["true_negative"] = total - (
            stats["true_positive"] + stats["false_negative"]
        )

        precision = round(stats["true_positive"] / retrieved, 2)

        recall = round(stats["true_positive"] / total, 2)

        fscore = 2 * ((precision * recall) / (precision + recall))

        average_confidence = round(stats["average_confidence"] / retrieved, 2)

        accuracy = round((stats["true_positive"] + stats["true_negative"]) / total, 2)

        stats["average_confidence"] = average_confidence
        stats["precision"] = precision
        stats["recall"] = recall
        stats["fscore"] = fscore
        stats["accuracy"] = accuracy

    sorted_themes_precision_table = dict(
        sorted(
            themes_precision_table.items(),
            key=lambda item: item[1][sort_by],
            reverse=True,
        )
    )

    return sorted_themes_precision_table


def sklearn_metrics_table(prompt_results: List[PromptResult], sort_by: str = "fscore"):
    y_true = [result["gold_label"] for result in prompt_results]
    y_pred = [result["final_answer"] for result in prompt_results]

    precision, recall, fscore, support = precision_recall_fscore_support(
        y_true, y_pred, average=None
    )

    labels = sorted(set(y_true))

    metrics_table = {}

    print("Generating metrics table...")
    for i, label in tqdm(enumerate(labels)):
        metrics_table[label] = {
            "precision": precision[i],
            "recall": recall[i],
            "fscore": fscore[i],
            "support": support[i],
        }

    sorted_metrics = dict(
        sorted(metrics_table.items(), key=lambda item: item[1][sort_by], reverse=True)
    )

    fscore_metrics = sklearn_fscore_metrics(prompt_results)

    sorted_metrics.update()

    sorted_metrics["weighted_fscore"] = fscore_metrics["weighted"]
    sorted_metrics["micro_fscore"] = fscore_metrics["micro"]
    sorted_metrics["macro_fscore"] = fscore_metrics["macro"]

    return sorted_metrics


def sklearn_fscore_metrics(prompt_results: List[PromptResult]):
    y_true = [result["gold_label"] for result in prompt_results]
    y_pred = [result["final_answer"] for result in prompt_results]

    fscore_metrics = {}
    metric_types = ["weighted", "micro", "macro"]
    for metric_type in metric_types:
        fscore_metrics[metric_type] = precision_recall_fscore_support(
            y_true, y_pred, average=metric_type
        )[2]

    return fscore_metrics


def as_matrix(metrics_table):
    """
    Takes a metrics dictionary and generates the right output for Matplotlib

    {
        "themes": ["theme_1", "theme_2", "theme_3", ...],
        "precisions": [0.497, 0.497, 0.497, ...],
        "recalls": [0.497, 0.497, 0.497, ...],
        "fscores": [0.497, 0.497, 0.497, ...],
    }
    """
    matrix_data = {
        "themes": [],
        "precisions": [],
        "recalls": [],
        "fscores": [],
        "weighted_fscore": 0.0,
        "macro_fscore": 0.0,
        "micro_fscore": 0.0,
    }

    matrix_data["weighted_fscore"] = metrics_table["weighted_fscore"]
    del metrics_table["weighted_fscore"]
    matrix_data["micro_fscore"] = metrics_table["micro_fscore"]
    del metrics_table["micro_fscore"]
    matrix_data["macro_fscore"] = metrics_table["macro_fscore"]
    del metrics_table["macro_fscore"]

    themes = []
    precisions = []
    recalls = []
    fscores = []

    print("Shapping table to matrices...")
    for theme_name, theme_metrics in tqdm(metrics_table.items()):
        themes.append(theme_name)
        precisions.append(theme_metrics["precision"])
        recalls.append(theme_metrics["recall"])
        fscores.append(theme_metrics["fscore"])

    matrix_data["themes"] = themes
    matrix_data["precisions"] = precisions
    matrix_data["recalls"] = recalls
    matrix_data["fscores"] = fscores

    return matrix_data


def get_run_support_count(run_id: str):
    prompt_results = connector.client.get_prompt_results({"run_id": run_id})

    supports = Counter([x["gold_label"] for x in prompt_results])

    return dict(supports.most_common())


def get_wrongly_guessed_questions_from_run(run_id: str, stop_at_level: int = 3):
    """
    Identify questions that were wrongly predicted in a specific run.

    :param run_id: ID of the run
    :param stop_at_level: Maximum hierarchy level
    :return: List of questions with wrong predictions
    """

    results = connector.client.get_prompt_results({"run_id": run_id})
    results = list(results)
    wrong_questions = []
    question_cache = {}

    question_ids = [result["question_id"] for result in results]

    questions = connector.client.get_questions({"id": {"$in": question_ids}})
    question_list = list(questions)
    question_cache.update({q["id"]: q for q in question_list})

    for result in results:
        response_theme = result["final_answer"]
        prompt_result_question = question_cache[result["question_id"]]
        question_theme = result["gold_label"]

        if response_theme == question_theme:
            wrong_questions.append(
                {
                    "question_id": result["question_id"],
                    "question_text": prompt_result_question["question_text"],
                    "predicted": response_theme,
                    f"question_level_{stop_at_level}_theme": question_theme,
                    "confidence": result["confidence"],
                    "logprobs": result["logprobs"],
                }
            )

    return wrong_questions


def sklearn_calibration_error_curve(confidences_mapping):
    y_true = confidences_mapping["is_prediction_correct"]
    y_prob = confidences_mapping["confidence"]

    calibration_error_curve = calibration_curve(y_true=y_true, y_prob=y_prob, n_bins=10)

    return calibration_error_curve
