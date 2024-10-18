import os
import re
import json
import locale
import hashlib
from hashlib import sha256
from collections import OrderedDict
from models.Prompt import PromptText
from typing import List, Dict, Any, Generator


def rgb_to_hex(rgb: List[float]) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


def rgbs_to_hexes(rgbs: List[List[float]]) -> List[str]:
    hexes = [rgb_to_hex(color) for color in rgbs]

    return hexes


def find_src_directory() -> str:
    """
    Find the 'src' directory in the current or any parent directory.

    This function searches for a directory named 'src' starting from the current working
    directory and moving up through parent directories until it finds the 'src' folder
    or reaches the root directory. If no 'src' directory is found, a `FileNotFoundError`
    is raised.

    Returns
    -------
    str
        The path to the 'src' directory if found.

    Raises
    ------
    FileNotFoundError
        If the 'src' directory is not found in the current or any parent directory.
    """
    current_directory = os.getcwd()

    while True:
        if "src" in os.listdir(current_directory):
            return os.path.join(current_directory, "src")

        parent_directory = os.path.dirname(current_directory)

        if current_directory == parent_directory:
            raise FileNotFoundError(
                "Could not find 'src' directory in any parent folder."
            )

        current_directory = parent_directory


def flatten_list(json_data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """
    Flattens a list of nested dictionaries by removing a specified key that contains nested elements.

    Parameters
        json_data (List[Dict[str, Any]]): The input list of dictionaries to flatten.
        key (str): The key in each dictionary that contains nested dictionaries.

    Returns
        List[Dict[str, Any]]: A flattened list of dictionaries, with all nested elements merged at the top level.
    """
    flat_list = []

    def flatten(item: Dict[str, Any]) -> None:
        """
        Recursively flattens a dictionary by removing the specified key and appending its content
        to the flat_list.

        Parameters
            item (Dict[str, Any]): The dictionary to flatten.
        """
        item_copy = {k: v for k, v in item.items() if k != key}
        flat_list.append(item_copy)

        if key in item:
            for child in item[key]:
                flatten(child)

    for entry in json_data:
        flatten(entry)

    return flat_list


def get_unique_dicts_by_key(dict_list: List[Dict], key: str) -> List[Dict]:
    """
    Retrieve unique dictionaries from a list based on a specified key.

    Parameters
    ----------
    dict_list : List[Dict]
        A list of dictionaries from which to extract unique entries.
    key : str
        The key used to determine uniqueness. Dictionaries with the same value for this key are considered duplicates.

    Returns
    -------
    List[Dict]
        A list of dictionaries that are unique based on the specified key.
    """
    seen_keys = set()
    unique_dicts = []

    for d in dict_list:
        key_value = d.get(key)
        if key_value not in seen_keys:
            seen_keys.add(key_value)
            unique_dicts.append(d)

    return unique_dicts


def hash_list(list: List[Any]):
    """
    Generate a SHA-256 hash for a given list.

    This function serializes the input list into a JSON string (with keys sorted), then
    computes and returns its SHA-256 hash.

    Parameters
    ----------
    list: List[Any]
        The list to be hashed. The elements in the list must be serializable to JSON format.

    Returns
    -------
    str
        The SHA-256 hash of the serialized list as a hexadecimal string.
    """
    list_str = json.dumps(list, sort_keys=True)

    hashed_list = hashlib.sha256(list_str.encode())

    return hashed_list.hexdigest()


def print_prompts(prompts: List[PromptText]) -> None:
    """
    Print the content of a list of prompts with their respective roles.

    Parameters
    ----------
    prompts : List[PromptText]
        A list of PromptText objects, each containing a role and content.
    """
    for prompt in prompts:
        print(f"{prompt.role.value}: {prompt.content}\n")


def save_chart(
    plot, image_name: str, save_folder: str = "images", dpi: int = 300
) -> None:
    """
    Save a given chart or plot as an image file.

    Parameters
    ----------
    plot : matplotlib.figure.Figure or matplotlib.axes._subplots.AxesSubplot
        The plot to save.
    image_name : str
        The name of the image file (without file extension).
    save_folder : str, default="images"
        The folder in which to save the image. It will be created if it does not exist.
    dpi : int, default=300
        The resolution of the saved image in dots per inch (DPI).
    """
    save_dir = f"{find_src_directory()}/{save_folder}"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image_name = image_name.replace("/", "")

    plot.savefig(
        f"{save_dir}/{image_name}.png",
        dpi=dpi,
    )


def remove_frame(plot) -> None:
    plot.rcParams["axes.spines.left"] = False
    plot.rcParams["axes.spines.right"] = False
    plot.rcParams["axes.spines.top"] = False
    plot.rcParams["axes.spines.bottom"] = False


def sort_list(list: List[Any]) -> List[Any]:
    """
    Sort a list of items using locale-aware string comparison.

    Parameters
    ----------
    list : List[Any]
        A list of items to be sorted.

    Returns
    -------
    List[Any]
        The input list sorted in a locale-aware manner using the "fr_FR.UTF-8" locale for string comparison.
    """
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

    return sorted(list, key=locale.strxfrm)


def retrieve_theme_from_cot_response(llm_response: str) -> str:
    """
    Extract the theme label from a Chain-of-Thought (CoT) response generated by an LLM.

    Parameters
    ----------
    llm_response : str
        The full response from the LLM containing the CoT explanation and the final theme label.

    Returns
    -------
    str
        The extracted theme label if found in the LLM response, otherwise an empty string.

    Example
    -------
    >>> retrieve_theme_from_cot_response("Some explanation... label: Theme 1")
    'theme 1'
    """

    pattern = r"(?s).*:\s*(.*)$"

    match = re.search(pattern, llm_response, re.IGNORECASE)

    if match:
        return match.group(1).strip().lower().replace("**", "").replace(".", "")

    return ""


def generate_theme_unique_identifier(theme_name: str, theme_level: int) -> str:
    """
    Generate a unique identifier for a theme.

    Parameters
    ----------
    theme_name: str
        Name of the theme.
    theme_level: int
        Level in the theme hierarchy mapping.

    Returns
    -------
    str
        A unique identifier for the provided theme.
    """
    unique_identifier = sha256(
        bytes(theme_name + str(theme_level), "utf-8")
    ).hexdigest()

    return unique_identifier


def write_roman(num: int) -> str:
    """
    Convert an integer to its Roman numeral representation.

    Parameters
    ----------
    num : int
        The integer value to convert to a Roman numeral. Must be a positive integer.

    Returns
    -------
    str
        The Roman numeral representation of the input integer.

    Example
    -------
    >>> write_roman(1990)
    'MCMXC'
    >>> write_roman(2023)
    'MMXXIII'
    """

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num: int) -> Generator[str, None, None]:
        """
        Helper generator function that yields Roman numeral segments for a given integer.

        Parameters
        ----------
        num : int
            The integer value to convert into Roman numeral segments.

        Yields
        ------
        str
            The Roman numeral segment corresponding to a part of the input integer.
        """

        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= r * x
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])
