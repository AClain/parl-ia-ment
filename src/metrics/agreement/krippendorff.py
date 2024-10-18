from typing import Dict, List
from krippendorff_alpha import krippendorff_alpha
from utils.database import (
    prompt_results_from_run_id,
    themes_list_from_run_id,
)


def _build_krippendorff_table(run_ids: List[str]) -> List[Dict[str, str]]:
    """
    Given several prompt runs IDs, build the Krippendorff table in order to
    compute the Krippendorff's alpha measure.

    Parameters
    ----------
    run_ids: List[str]
        A list of prompt runs IDs.

    Returns
    -------
    List[Dict[str, str]]
        A dataframe-like object that has the following shape :
        [
            {question_id: predicted_label, ...},  # LLM 1
            {question_id: predicted_label, ...},  # LLM 2
            ...
        ]
    """
    data = []
    for run_id in run_ids:
        results = {}
        prompt_results = prompt_results_from_run_id(run_id)
        for prompt_result in prompt_results:
            results[prompt_result["question_id"]] = prompt_result[
                "final_answer"
            ].strip()
        data.append(results)

    return data


def compute_krippendorff_alpha(run_ids: List[str]) -> float:
    """
    Compute the Krippendorff's alpha metric. The alpha value will range between -1 and 1:

        1 - indicates perfect agreement between raters.
        0 - indicates no agreement beyond what would be expected by chance.
        Negative values indicate less agreement than would be expected by chance.

    Parameters
    ----------
    urn_ids: List[str]
        A list of prompt runs IDs.

    Returns
    -------
    float
        The Krippendorff's alpha metric.
    """
    krippendorff_table = _build_krippendorff_table(run_ids)  # type: ignore
    themes_list = themes_list_from_run_id(run_ids[0])

    return krippendorff_alpha(
        krippendorff_table,
        convert_items=lambda x: float(themes_list.index(x.strip())),  # type: ignore
    )
