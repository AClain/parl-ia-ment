import json
import re
from typing import List
from pathlib import Path
from configs.env import get_src_path
from difflib import SequenceMatcher


def question_processing(question: str, masks: List[str] | None = None) -> str:
    from copy import deepcopy
    question_copy = deepcopy(question)
    input_size = len(question)
    if masks is None:
        ministries = f"{get_src_path(Path(__file__))}/data/positions.json"
        with open(ministries, "r", encoding="utf-8") as file:
            masks = json.load(file)

    if masks is None:
        raise ValueError(
            "No ministries pattern provided. Make you sure you either "
            "provide a positions.json file with existing ministries patterns "
            "or a list of masks to apply."
        )

    output_size = 0
    selected_mask = ""
    for mask in masks:
        if mask in question.lower():
            question = re.sub(rf"(?<=ministre) (d[u|e]s?\s){mask}", "", question)
            if len(question) < input_size:
                selected_mask = mask
                output_size = len(question)
                break

    # Remove 4 because the pattern introducing the ministry is included
    # in the regex (line 29)
    if input_size - len(selected_mask) - 4 != output_size:
        raise ValueError(
            "An error occurred when applying the ministries mask. "
            "Another part of the question was propably croped."
        )

    return question

def save_government_positions(filename: str):
    results = []
    filename = f"{get_src_path(Path(__file__))}/data/governments.json"
    with open(filename, "r", encoding="utf-8") as file:
        government_data = json.load(file)
        for minister in government_data["ministers"]:
            minister_positions = minister["positions"]
            for position in minister_positions:
                ministry = position_processing(position["position"])
                if ministry and (ministry.lower() not in results):
                    results.append(ministry.lower())
    results = sorted(results, key=len, reverse=True)
    with open(filename, "w") as f:
        json.dump(results, f)

def position_processing(position: str) -> str | None:
    position = re.sub(
        r"(Ministre d[u|e]s?|Secrétaire d'Etat) (d[u|e]s?|à|aux?|pour|chargée?)?",
        "", 
        position
    )
    if "ministre" not in position.lower() and "secrétaire" not in position.lower():
        return position

