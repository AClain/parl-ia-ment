import os

os.sys.path.append(os.path.join(os.getcwd(), "src"))

import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from models.Colors import BColors
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from utils.normalize_themes import remove_special_chars

load_dotenv()


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def make_one_list():
    themes = set()
    for legislature_number in range(8, 17):
        get_themes_by_legislature(legislature_number)
        with open(
            f"src/themes/legislatures/{legislature_number}/themes.json"
        ) as json_file:
            themes.update(json.load(json_file))

    all_themes = sorted(list(themes), key=str.casefold)

    if os.path.exists("src/themes/all_themes.json"):
        os.remove("src/themes/all_themes.json")

    with open("src/themes/all_themes.json", "w") as file:
        json.dump(all_themes, file)


def get_theme_question_count():
    all_theme_file_path = "src/themes/all_themes.json"
    themes = read_json_file(all_theme_file_path)
    connector = Connector(ExportFormat.JSON)
    all_themes_questions = {}
    total_question = 0

    for theme in themes:
        theme_questions = connector.client.count_documents_by_theme(theme)
        if theme_questions > 0:
            total_question += theme_questions
            print(
                "number of questions for"
                + BColors.BOLD.value
                + f" '{theme}' : {theme_questions}"
                + BColors.ENDC.value
            )
            all_themes_questions[theme] = theme_questions
        else:
            print(
                "no question found for"
                + BColors.BOLD.value
                + f" '{theme}'"
                + BColors.ENDC.value
            )
            all_themes_questions[theme] = 0

    print(f"number of questions with theme : {total_question}")
    write_json_file(
        "src/themes/all_themes_question_count.json",
        dict(sorted(all_themes_questions.items(), key=lambda item: item[1])),
    )


def get_themes_by_legislature(legislature):
    print(f"getting themes for the {legislature}th legislature")
    url = f"https://www2.assemblee-nationale.fr/recherche/questions/{legislature}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.select('select[name="rubrique"] option')

    themes = []

    for element in elements:
        if len(element.text) > 0:
            themes.append(element.text)

    if not os.path.exists(f"src/themes/legislatures/{legislature}"):
        os.makedirs(f"src/themes/legislatures/{legislature}")

    if os.path.exists(f"src/themes/legislatures/{legislature}/themes.json"):
        os.remove(f"src/themes/legislatures/{legislature}/themes.json")

    with open(f"src/themes/legislatures/{legislature}/themes.json", "w") as file:
        json.dump(themes, file)


def normalize():
    theme_questions = read_json_file("src/themes/all_themes_question_count.json")
    new_theme_questions = dict()

    for nb_question, theme in enumerate(theme_questions):
        new_theme_name = remove_special_chars(theme)
        new_theme_name = new_theme_name.lower()
        new_theme_name = re.sub(r"((?<=\w)\:)", " :", new_theme_name)
        if new_theme_name in new_theme_questions:
            new_theme_questions[new_theme_name] += theme_questions[theme]
        else:
            new_theme_questions[new_theme_name] = theme_questions[theme]

    print(f"removed {len(theme_questions) - len(new_theme_questions)} themes")
    all_themes_normalized = dict(
        sorted(new_theme_questions.items(), key=lambda item: item[1])
    )
    write_json_file("src/themes/all_themes_normalized.json", all_themes_normalized)


if __name__ == "__main__":
    print("generating" + BColors.BOLD.value + " 'all_themes.json'" + BColors.ENDC.value)
    make_one_list()  # Generates all_themes.json
    print(
        "generating"
        + BColors.BOLD.value
        + " 'all_themes_question_count.json'"
        + BColors.ENDC.value
    )
    get_theme_question_count()  # Generates all_themes_question_count.json
    # Normalize
    print(
        "generating"
        + BColors.BOLD.value
        + " 'all_themes_normalized.json'"
        + BColors.ENDC.value
    )
    normalize()
