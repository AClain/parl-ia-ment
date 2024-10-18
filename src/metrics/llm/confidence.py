import re
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from metrics.softmax import softmax
from databases.connector import Connector
from typing import Any, Dict, List, Tuple
from models.ExportFormat import ExportFormat
from models.Result import ResultAndConfidence
from models.LLMOutput import ConfidenceType, TokenMetrics
from errors.WrongConfidenceTypeException import WrongConfidenceTypeException


def _build_results_and_confidence(
    run_ids: List[str] | str, confidence_type: ConfidenceType
) -> List[ResultAndConfidence]:
    """
    Retrieve all prompt results corresponding to the given run IDs and build
    a list of result sets that associates the question ID, the predicted label,
    the gold label, and the confidence of the LLM prediction.

    Parameters
    ----------
    run_ids: List[str] | str
        The run IDs.
    confidence_type: ConfidenceType
        The type of confidence measure.

    Returns
    -------
    List[ResultAndConfidence]
        A list of result sets that associates :
        - The question ID
        - The predicted label
        - The gold label
        - The confidence measure
    """
    connector = Connector(ExportFormat.JSON)
    if type(run_ids) is str:
        run_ids = [run_ids]

    prompt_results = connector.client.get_prompt_results({"run_id": {"$in": run_ids}})
    prompt_results = list(prompt_results)

    results_and_confidence = []
    match confidence_type:
        case ConfidenceType.Logprobs:
            for result in tqdm(prompt_results):
                results_and_confidence.append(
                    ResultAndConfidence(  # type: ignore
                        question_id=result["question_id"],
                        predicted_label=result["final_answer"],
                        gold_label=result["gold_label"],
                        confidence=_compute_logprobs_confidence(result["logprobs"]),
                    )
                )
        case ConfidenceType.Verbalized:
            for result in tqdm(prompt_results):
                results_and_confidence.append(
                    ResultAndConfidence(  # type: ignore
                        question_id=result["question_id"],
                        predicted_label=result["final_answer"],
                        gold_label=result["gold_label"],
                        confidence=_compute_verbalized_confidence(result["response"]),
                    )
                )
        case ConfidenceType.SelfCalibration:
            results_and_confidence += _compute_self_calibration_confidence(
                run_ids,
                prompt_results,  # type: ignore
            )
        case ConfidenceType.SelfConsistency:
            results_and_confidence += _compute_self_consistency_confidence(
                prompt_results
            )
        case _:
            raise WrongConfidenceTypeException(confidence_type)

    return results_and_confidence


def _compute_self_consistency_confidence(
    prompt_results: List[Dict[str, Any]],
) -> List[ResultAndConfidence]:
    """
    Compute self-consistency confidence for a list of prompt results.

    Parameters
    ----------
    prompt_results : List[Dict[str, Any]]
        A list of dictionaries where each dictionary represents a prompt result.

    Returns
    -------
    List[ResultAndConfidence]
        A list of ResultAndConfidence objects containing the question ID, the most consistently predicted label,
        the gold label, and the confidence score, which represents the proportion of runs that predicted the same label.
    """
    results_and_confidence = []

    run_ids = list(set([prompt_result["run_id"] for prompt_result in prompt_results]))
    question_ids = list(
        set([prompt_result["question_id"] for prompt_result in prompt_results])
    )

    for question_id in question_ids:
        predicted_labels_for_question = []
        for run_id in run_ids:
            selected_prompt_result = next(
                (
                    prompt_result
                    for prompt_result in prompt_results
                    if prompt_result["run_id"] == run_id
                    and prompt_result["question_id"] == question_id
                )
            )
            predicted_labels_for_question.append(selected_prompt_result["final_answer"])

        counts = Counter(predicted_labels_for_question)

        most_predicted = max(counts.values())
        most_predicted_labels = [
            key for key, count in counts.items() if count == most_predicted
        ]
        most_predicted_label = random.choice(most_predicted_labels)

        results_and_confidence.append(
            ResultAndConfidence(
                question_id=question_id,
                predicted_label=most_predicted_label,
                gold_label=selected_prompt_result["gold_label"],
                confidence=most_predicted / len(predicted_labels_for_question),
            )
        )

    return results_and_confidence


def _compute_self_calibration_confidence(
    run_ids: List[str], prompt_results: List[Dict[str, Any]]
) -> List[ResultAndConfidence]:
    """
    Compute self-calibration confidence of an LLM prediction. This requires that the
    LLM prompt run was run in a self-calibration setting.

    Parameters
    ----------
    run_ids: List[str]
        The list of run IDs.
    prompt_results: List[Dict[str, Any]]
        The list of prompt results.

    Returns
    -------
        A list of results with associated confidence.
    """
    connector = Connector(ExportFormat.JSON)
    results_and_confidence = []
    calib_run_ids = []
    # Start by collecting associated self-calibration runs
    for run_id in run_ids:
        prompt_run = connector.client.get_prompt_run(
            {"name": f"Self-Calibration #{run_id}"}
        )
        if prompt_run is None:
            raise WrongConfidenceTypeException(ConfidenceType.SelfCalibration)
        calib_run_ids.append(str(prompt_run["_id"]))  # type: ignore

    calib_results = connector.client.get_prompt_results(
        {"run_id": {"$in": calib_run_ids}}
    )
    calib_results = list(calib_results)

    for result in tqdm(prompt_results):
        for calib in calib_results:
            if result["question_id"] == calib["question_id"]:
                results_and_confidence.append(
                    ResultAndConfidence(  # type: ignore
                        question_id=result["question_id"],
                        predicted_label=result["final_answer"],
                        gold_label=result["gold_label"],
                        confidence=_compute_logprobs_confidence(calib["logprobs"]),
                    )
                )
                break

    return results_and_confidence


def _compute_verbalized_confidence(llm_raw_response: str) -> float:
    """
    Compute verbalized confidence of an LLM prediction. This requires that the
    LLM response is outputed in the following format :
        [EN]
        Theme: str
        Probability: float
            -----------
        [FR]
        Thème: str
        Probabilité: float

    Parameters
    ----------
    llm_raw_response: str
        The LLM raw response.

    Returns
    -------
    float
        The verbalized confidence associated with the LLM response.
    """
    regex = re.compile(r"(Probabilit[é|y]:) ([\d|\.]+)")
    capture = re.search(regex, llm_raw_response)
    if capture is None:
        raise WrongConfidenceTypeException(ConfidenceType.Verbalized)
    return float(capture.group(2).strip())


def _compute_logprobs_confidence(tokens_metrics: List[TokenMetrics]) -> float:
    """
    Compute logprobs confidence of an LLM prediction.

    Parameters
    ----------
    List[TokenMetrics]
        The list of token metrics prediction and associated logprobs.

    Returns
    -------
    float
        The confidence measure of the predicted tokens.
    """
    all_logprobs = []
    for token_metrics in tokens_metrics:
        logprob_array = [x["logprob"] for x in token_metrics["top_logprobs"]]  # type: ignore
        all_logprobs.append(softmax(np.array(logprob_array)))

    logprobs_prod = np.array(all_logprobs).transpose()[0].prod()

    confidence = np.power(logprobs_prod, 1 / len(all_logprobs))

    return round(float(confidence), 3)


def _accuracy_in_bin(data: pd.DataFrame, bot: float, top: float) -> float:
    """
    Measures the accuracy in a given bin.

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe containing both predicted labels, gold labels and confidence
        measures.
    bot: float
        The lower bin value.
    top: float
        The upper bin value.

    Returns
    -------
    float
        The accuracy measure in the given bin.
    """
    s_in_bin = _samples_in_bin(data, bot, top)
    trues = s_in_bin[
        s_in_bin["predicted_label"] == s_in_bin["gold_label"]  # type: ignore
    ]

    try:
        return float(len(trues) / len(s_in_bin))  # type: ignore
    except ZeroDivisionError:
        return 0.0


def _confidence_in_bin(data: pd.DataFrame, bot: float, top: float) -> float:
    """
    Measures the confidence in a given bin.

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe containing both predicted labels, gold labels and confidence
        measures.
    bot: float
        The lower bin value.
    top: float
        The upper bin value.

    Returns
    -------
    float
        The confidence measure in the given bin.
    """
    s_in_bin = _samples_in_bin(data, bot, top)
    confidences = s_in_bin["confidence"].sum()

    if len(s_in_bin) == 0:
        return 0.0
    return float(confidences / len(s_in_bin))


def _samples_in_bin(data: pd.DataFrame, bot: float, top: float) -> pd.DataFrame:
    """
    Measures the number of samples represented in a given bin.

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe containing both predicted labels, gold labels and confidence
        measures.
    bot: float
        The lower bin value.
    top: float
        The upper bin value.

    Returns
    -------
    float
        The number of samples from accuracy and confidence measures were made for
        a given bin.
    """
    s_in_bin = data[(data["confidence"] > bot) & (data["confidence"] <= top)]
    return s_in_bin  # type: ignore


def _compute_ece_from_data(data: pd.DataFrame, num_of_bins: int = 10) -> float:
    """
    Compute the expected calibration error (ECE) for a given number of prompt runs.

    Parameters
    ----------
    data: pd.DataFrame
        The input data containing confidence measures and results.
    num_of_bins: int, default=10
        Defines the number of bins in the final ECE computation.

    Returns
    -------
    float
        The ECE value.
    """
    bin_boundaries = np.linspace(0, 1, num_of_bins + 1)
    top = bin_boundaries[1:]
    bot = bin_boundaries[:-1]

    result = 0
    for bot, top in zip(bot, top):
        s_in_bin = _samples_in_bin(data, bot, top)
        confidences = _confidence_in_bin(data, bot, top)
        accuracies = _accuracy_in_bin(data, bot, top)
        try:
            bm_n = len(s_in_bin) / len(data)
        except ZeroDivisionError:
            bm_n = 0
        ece = bm_n * abs(accuracies - confidences)
        result += ece

    return result


def compute_ece(
    run_ids: List[str] | str,
    confidence_type: ConfidenceType,
    num_of_bins: int = 10,
    with_data: bool = False,
) -> float | Tuple[float, pd.DataFrame]:
    """
    Compute the expected calibration error (ECE) for a given number of
    prompt runs.

    Parameters
    ----------
    run_ids: List[str] | str
        The run IDs.
    confidence_type: ConfidenceType
        The type of confidence measure.
    num_of_bins: int, default=10
        Defines the number of bins in the final ECE computation.
    with_data: bool, default=False
        Defines if the output should also provide the detailed results associating
        confidences, questions IDs, predicted labels and gold labels.

    Returns
    -------
    float | Tuple[pd.DataFrame, float]
        The ECE value. If `with_data` is `True`, returns also the detailed results
        of the prompt run.
    """
    data = pd.DataFrame(_build_results_and_confidence(run_ids, confidence_type))
    result = _compute_ece_from_data(data, num_of_bins)

    if with_data:
        return result, data

    return result


def compute_ice(run_ids: List[str] | str, confidence_type: ConfidenceType) -> float:
    """
    Compute the instance-level calibration error (ICE). This is inspired from
    the metric described by Chenglei Si, Chen Zhao, Sewon Min & Jordan Boyd-Graber,
    "Revisiting calibration for question answering" (2022).

    Parameters
    ----------
    run_ids: List[str] | str
        The list of run IDs.
    confidence_type: ConfidenceType
        The type of confidence to measure.

    Returns
    -------
    float
        The ICE measure.
    """
    data = pd.DataFrame(_build_results_and_confidence(run_ids, confidence_type))

    results = []
    for _, row in data.iterrows():
        if row["predicted_label"] == row["gold_label"]:
            results.append(abs(1 - row["confidence"]))
        else:
            results.append(abs(0 - row["confidence"]))

    return float(np.array(results).mean())


def compute_macroce(run_ids: List[str] | str, confidence_type: ConfidenceType):
    """
    Compute the macro calibration error (MacroCE). This is inspired from
    the metric described by Chenglei Si, Chen Zhao, Sewon Min & Jordan Boyd-Graber,
    "Revisiting calibration for question answering" (2022).

    Parameters
    ----------
    run_ids: List[str] | str
        The list of run IDs.
    confidence_type: ConfidenceType
        The type of confidence to measure.

    Returns
    -------
    float
        The MacroCE measure.
    """
    data = pd.DataFrame(_build_results_and_confidence(run_ids, confidence_type))

    ice_pos = []
    ice_neg = []
    for _, row in data.iterrows():
        if row["predicted_label"] == row["gold_label"]:
            ice_pos.append(1 - row["confidence"])
        else:
            ice_neg.append(row["confidence"] - 0)
    ice_pos = np.array(ice_pos).mean() if ice_pos else 0
    ice_neg = np.array(ice_neg).mean() if ice_neg else 0

    return 1 / 2 * (float(ice_pos) + float(ice_neg))
