import itertools
from typing import List, Dict, Tuple
from sklearn.metrics import cohen_kappa_score
from utils.database import prompt_results_from_run_ids, prompt_runs_from_ids


def compute_cohen_kappa(run_ids: List[str]) -> Dict[Tuple[str, str], float]:
    """
    Compute Cohen's Kappa scores for pairwise comparisons of prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs to be compared.

    Returns
    -------
    Dict[Tuple[str, str], float]
        A dictionary where the keys are tuples of two run names, and the values are the corresponding Cohen's Kappa scores.
        The score indicates the inter-rater agreement between the two runs based on their predicted labels.
    """
    kappa_scores = {}
    runs = prompt_runs_from_ids(run_ids)
    prompt_results = prompt_results_from_run_ids(run_ids)
    question_ids = list(
        set([prompt_result["question_id"] for prompt_result in prompt_results])
    )

    for run_1_id, run_2_id in itertools.combinations(run_ids, 2):
        run_1_predicted_labels = []
        run_2_predicted_labels = []
        for question_id in question_ids:
            run_1_predicted_labels.append(
                next(
                    (
                        prompt_result["final_answer"].strip()
                        for prompt_result in prompt_results
                        if prompt_result["run_id"] == run_1_id
                        and prompt_result["question_id"] == question_id
                    ),
                    "",
                )
            )
            run_2_predicted_labels.append(
                next(
                    (
                        prompt_result["final_answer"].strip()
                        for prompt_result in prompt_results
                        if prompt_result["run_id"] == run_2_id
                        and prompt_result["question_id"] == question_id
                    ),
                    "",
                )
            )

        run_1_name = next(
            (run["name"] for run in runs if str(run["_id"]) == run_1_id), ""
        )
        run_2_name = next(
            (run["name"] for run in runs if str(run["_id"]) == run_2_id), ""
        )

        kappa_scores[(run_1_name, run_2_name)] = cohen_kappa_score(
            run_1_predicted_labels, run_2_predicted_labels
        )

    return kappa_scores
