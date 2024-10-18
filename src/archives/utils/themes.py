from typing import List, Tuple, Dict
from databases.connector import Connector
from models.ExportFormat import ExportFormat


connector = Connector(ExportFormat.JSON)


def convert_selector_to_theme(letter: str, themes_list: List[str]) -> str:
    """
    Convert a letter-based selector to its corresponding theme.

    Parameters
    ----------
    letter : str
        The letter representing a theme (e.g., 'A', 'B', etc.).
    themes_list : List[str]
        The list of themes where each theme is mapped to a letter sequentially.

    Returns
    -------
    str
        The theme corresponding to the input letter.

    Example
    -------
    >>> convert_selector_to_theme("A", ["Theme 1", "Theme 2"])
    'Theme 1'
    """

    a_to_z = [chr(i) for i in range(ord("A"), ord("["))]
    return themes_list[a_to_z.index(letter)]


def convert_theme_to_selector(theme: str, themes_list: List[str]) -> str:
    """
    Convert a theme to its corresponding letter-based selector.

    Parameters
    ----------
    theme : str
        The theme name to convert to a letter-based selector.
    themes_list : List[str]
        The list of themes where each theme is mapped to a letter sequentially.

    Returns
    -------
    str
        The letter corresponding to the input theme.

    Example
    -------
    >>> convert_theme_to_selector("Theme 1", ["Theme 1", "Theme 2"])
    'A'
    """

    a_to_z = [chr(i) for i in range(ord("A"), ord("["))]
    return a_to_z[themes_list.index(theme)]


def convert_theme_list_to_letter_range(themes_list: List[str]) -> List[str]:
    """
    Generate a list of letter-based selectors for a given list of themes.

    Parameters
    ----------
    themes_list : List[str]
        The list of themes for which to generate letter-based selectors.

    Returns
    -------
    List[str]
        A list of letters corresponding to the input themes.

    Example
    -------
    >>> convert_theme_list_to_letter_range(["Theme 1", "Theme 2"])
    ['A', 'B']
    """

    a_to_z = [chr(i) for i in range(ord("A"), ord("["))]
    return a_to_z[0 : len(themes_list)]


def randomize_themes_list_order(themes_list: List[str]) -> Tuple[List[str], List[str]]:
    """
    Randomly shuffle the order of themes and their corresponding letter-based selectors.

    Parameters
    ----------
    themes_list : List[str]
        The list of themes to shuffle.

    Returns
    -------
    Tuple[List[str], List[str]]
        A tuple containing two lists: shuffled letter-based selectors and the shuffled themes list.

    Example
    -------
    >>> randomize_themes_list_order(["Theme 1", "Theme 2"])
    (['B', 'A'], ['Theme 2', 'Theme 1'])
    """

    a_to_z = [chr(i) for i in range(ord("A"), ord("["))]
    shuffled = list(zip(a_to_z, themes_list))
    a_to_z, themes_list = zip(*shuffled)
    return a_to_z, themes_list


def retrieve_theme_from_selector(
    llm_response: str, themes_list: List[str], theme_level: int
) -> str:
    """
    Retrieves the theme associated with a given proxy selector.

    Parameters
    ----------
    llm_response: str
        The LLM response.
    themes_list: List[str]
        A list of themes.
    theme_level: int
        The aggregation level where to stop in the database.

    Returns
    -------
    str
        The theme associated to the proxy selector.
    """

    a_to_z = [chr(i) for i in range(ord("A"), ord("["))]

    association_table = {}

    for i, theme in enumerate(themes_list):
        association_table[a_to_z[i]] = theme["name"]

    return association_table[llm_response.strip()]


def runs_predicted_labels(run_ids: List[str]) -> Dict[str, List[str]]:
    """
    Retrieve the predicted labels for a set of runs and organize them by run ID.

    Parameters
    ----------
    run_ids : List[str]
        A list of run IDs for which to retrieve predicted labels.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary where each key is a run ID and each value is a list of predicted labels
        corresponding to that run ID.

    Example
    -------
    >>> runs_predicted_labels(["run_1", "run_2"])
    {
        'run_1': ['label 1', 'label 2'],
        'run_2': ['label 3', 'label 4']
    }
    """

    prompt_results = connector.client.get_prompt_results({"run_id": {"$in": run_ids}})
    prompt_results = list(prompt_results)

    predicted_labels_for_each_question = {}
    for prompt_result in prompt_results:
        if (
            prompt_result["question_id"]
            not in predicted_labels_for_each_question.keys()
        ):
            predicted_labels_for_each_question[prompt_result["question_id"]] = []

        predicted_labels_for_each_question[prompt_result["question_id"]].append(
            prompt_result["final_answer"]
        )

    table = {run_id: [] for run_id in run_ids}

    for question_id, predicted_labels in predicted_labels_for_each_question.items():
        if len(predicted_labels) < len(run_ids):
            continue

        for i, run_id in enumerate(run_ids):
            table[run_id].append(predicted_labels[i])

    return table
