from typing import List
from models.Result import RunData
from errors.WrongRunIdProvided import WrongRunIdProvided
from utils.database import prompt_run_from_run_id, prompt_from_unique_identifier


def gather_data_for_run_ids(run_ids: List[str]) -> List[RunData]:
    """
    Gather data for multiple prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs for which data needs to be gathered.

    Returns
    -------
    List[RunData]
        A list of RunData objects, each containing data for the corresponding run in the provided list of run IDs.
    """
    runs_data = []

    for run_id in run_ids:
        runs_data.append(gather_data_for_run_id(run_id))

    return runs_data


def gather_data_for_run_id(run_id: str) -> RunData:
    """
    Gather data for a prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        A unique identifiers for the prompt run for which data needs to be gathered.

    Returns
    -------
    List[RunData]
        A RunData object, containing data for the corresponding run ID.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided(run_id)

    prompt = prompt_from_unique_identifier(run["prompt_id"])

    return {"prompts": prompt.prompts, "name": run["name"], "run_id": run_id}
    return {"name": run["name"], "run_id": run_id}
