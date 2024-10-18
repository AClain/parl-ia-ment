import os

os.sys.path.append(os.path.join(os.getcwd(), "src"))
import json
import argparse
from typing import List
from normalize_themes import remove_special_chars


def sort_themes_list(themes: List) -> List:
    return sorted(themes, key=lambda s: remove_special_chars(s.lower()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-file", help="path to the file .json containing the list to sort"
    )
    args = parser.parse_args()
    filename = os.path.basename(args.file)
    folder = os.path.dirname(args.file)

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("JSON file should contain a list")

    sorted_list = sort_themes_list(data)

    with open(folder + "/sorted_" + filename, "w", encoding="utf-8") as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)

    print("Sorted list saved in file :", folder + "/sorted_" + filename)
