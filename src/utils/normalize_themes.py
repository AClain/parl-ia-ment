import os
import re
import json
import argparse
import unicodedata
from typing import Dict


def remove_special_chars(theme: str) -> str:
    """
    Remove special char to a theme such as accent or ç cedille🇫🇷.

    Parameters
    ----------
    theme: str
            A theme to remove special chars to
    """
    nfkd_form = unicodedata.normalize("NFKD", theme)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def remove_special_chars_list(themes: object) -> Dict[str, int]:
    """
    Remove special char to all key of themes.

    Parameters
    ----------
    themes: Dict[str, int]
            Dict of all themes and their occurence in the db
    """

    unique_themes_dict = {}
    unique_list = []
    for _, (theme, value) in enumerate(themes.items()):
        clean_theme = remove_special_chars(theme)
        if clean_theme in unique_list:
            unique_themes_dict[clean_theme] += value
        else:
            unique_list.append(clean_theme)
            unique_themes_dict[clean_theme] = value
    return unique_themes_dict


def to_lower_list(themes: Dict[str, int]) -> Dict[str, int]:
    """
        Apply lower to all key of themes.

    Parameters
    ----------
    themes: Dict[str, int]
            Dict of all themes and their occurence in the db
    """
    unique_themes_dict = {}
    unique_list = []
    for _, (theme, value) in enumerate(themes.items()):
        clean_theme = theme.lower()
        if clean_theme in unique_list:
            unique_themes_dict[clean_theme] += value
        else:
            unique_list.append(clean_theme)
            unique_themes_dict[clean_theme] = value
    return unique_themes_dict


def uniformize_space_before(themes: Dict[str, int]) -> Dict[str, int]:
    """
    Remove space before colon to uniformize.

    Parameters
    ----------
    themes: Dict[str, int]
            Dict of all themes and their occurence in the db
    """
    unique_themes_dict = {}
    unique_list = []
    for _, (theme, value) in enumerate(themes.items()):
        clean_theme = re.sub(r"((?<=\w)\:)", " :", theme)
        if clean_theme in unique_list:
            unique_themes_dict[clean_theme] += value
        else:
            unique_list.append(clean_theme)
            unique_themes_dict[clean_theme] = value
    return unique_themes_dict


def open_normalize_and_save(path: str, action: str) -> str:
    """
    Function which open a file with the given path
    and normalize the data in it given the
    the "normalize" function

    Parameters
    ----------
    path: str
            Path of the file to normalize
    action: str
            Name of the normalization function to use
    """
    folder = os.path.dirname(path)
    print(folder)
    if folder != "./prompting/normalized_themes_questions":
        folder += "/normalized_themes_questions"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        print("JSON file should contain a list")

    sorted_list = normalize_function(data, action)

    new_file_path = f"{folder}/{action}_all_themes_questions.json"
    with open(new_file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)

    return new_file_path


def normalize_function(data: Dict[str, int], action: str) -> Dict[str, int]:
    """
    Give the normalize function to apply given the action

    Parameters
    ----------
    data: dict[str, int]
            Dict of all themes and their occurence in the db
    action: str
            Name of the normalization function to use
    """
    if action == "clean_special_chars":
        return remove_special_chars_list(data)
    elif action == "to_lower":
        return to_lower_list(data)
    elif action == "uniformize_space_colon":
        return uniformize_space_before(data)


def normalize_all_themes(path: str) -> None:
    """
    Executes a chain of function to standardize themes
    and accumulate duplicate values

    Parameters
    ----------
    path: str
            Path of the original file containing the themes
    """

    clean_special_chars_path = open_normalize_and_save(path, "clean_special_chars")
    to_lower_path = open_normalize_and_save(clean_special_chars_path, "to_lower")
    open_normalize_and_save(to_lower_path, "uniformize_space_colon")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-file", help="path to the file .json containing the list to normalize"
    )
    args = parser.parse_args()
    normalize_all_themes(args.file)
