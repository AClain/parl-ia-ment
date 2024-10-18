import logging
import requests
from bs4 import BeautifulSoup
from lxml import etree
from models.Question import QuestionsByTheme


def questions_by_theme(
    theme: str,
    question_per_legislature: int = 3,
    questions_per_page: int = 25,
) -> QuestionsByTheme:
    """
    Retrieve a given number of questions par thème.

    Parameters
    ----------
    theme: str
        The given theme.
    question_per_legislature: int, default=3
        The number of question per legislature.
    questions_per_page: int, default=25
        The number of questions per page.

    Returns
    -------
    QuestionsByTheme
        The theme with all its associated questions.
    """
    questions_url = "https://www2.assemblee-nationale.fr/recherche/resultats_questions"
    number_questions = 0
    in_legislatures = []
    questions = []

    for legislature_number in range(7, 16):
        form_data = {
            'legislature': legislature_number,
            'ssTypeDocument[]': ['qe', 'qg', 'qosd'],
            'replies[]': ['ar', 'sr'],
            'removed[]': ['0', '1'],
            'q': '',
            'q_in': '0',
            'id_auteur': '',
            'departement': '',
            'groupePolitique': '',
            'rubrique': theme,
            'ministereInterroge': '',
            'ministereAttributaire': '',
            'causeCloture': '',
            'numDocument': '',
            'typeDate': '',
            'typeDate_start': '',
            'typeDate_end': '',
            'typeDate_exact': '',
            'criteres[0][field]': '',
            'criteres[0][value]': '',
            'criteres[1][field]': '',
            'criteres[1][value]': '',
            'criteres[2][field]': '',
            'criteres[2][value]': '',
            'sort_by': 'ssTypeDocument',
            'sort_order': 'asc',
            'limit': questions_per_page
        }

        res = requests.post(questions_url, data=form_data)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            number_results_container = soup.select_one("#resultats-questions > p > strong")
            if number_results_container is not None:
                in_legislatures.append(legislature_number)
                printed_questions = 0
                for tr in soup.select("#resultats-questions > table > tbody > tr"):
                    question = tr.select_one("td:nth-child(1) > a")["href"]  # type: ignore
                    if not is_empty_question(question):  # type: ignore
                        questions.append(question)
                    printed_questions += 1
                    if printed_questions >= question_per_legislature:
                        break
                number_questions += int(number_results_container.text)
        else:
            logging.error("A network issue occurred.")

    return QuestionsByTheme(**{
        "legislature": in_legislatures,
        "theme": theme,
        "total_number_of_questions": number_questions,
        "urls": questions
    })


def is_empty_question(
    question_url: str,
    empty_response: bool = False
) -> bool:
    """
    Parameters
    ----------
    question_url: str
        The URL to the question page.
    empty_response: bool, default=False
        Include the question if it has no question text but has a
        response text.

    Returns
    -------
    bool
        True if there is no question texte.

    Raises
    ------
    requests.HTTPError
        If the question page could not be retrieved.
    """
    r = requests.get(question_url)
    if r.status_code == 200:
        dom = etree.HTML(r.text)
        cap = dom.xpath(
            "//tr[./td//u[contains(text(), 'Texte de la QUESTION')]]/td/quest"
        )
        if len(cap[0].text) > 1:
            if empty_response:
                cap_response = dom.xpath(
                    "//tr[./td//u[contains(text(), 'Texte de la REPONSE')]]/td/quest"
                )
                if len(cap_response[0].text) > 1:
                    return False
                else:
                    return True
            return False
        else:
            return True
    else:
        raise requests.HTTPError(f"Could not reach the page {question_url}.")
