import os
import pytest
from typing import Dict
from bs4 import BeautifulSoup


@pytest.fixture
def question_16_qe_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question écrite' (QE) for the XVIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_16_qe.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_16_qosd_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question orale sans débat' (QOSD) for the XVIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_16_qosd.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_16_qg_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question au gouvernement' (QG) for the XVIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_16_qg.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_14_qe_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question écrite' (QE) for the XIVth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_14_qe.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_14_qosd_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question orale sans débat' (QOSD) for the XIVth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_14_qosd.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_14_qg_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question au gouvernement' (QG) for the XIVth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_14_qg.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_11_qg_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question au gouvernement' (QG) for the XIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_11_qg.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_11_qosd_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question orale sans débat' (QOSD) for the XIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_11_qosd.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_11_qe_html() -> BeautifulSoup:
    """
    A parsed HTML page containing a question content for a given
    'question écrite' (QE) for the XIth legislature HTML page.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    with open("tests/fixtures/html_pages/html_11_qe.html", "r") as html:
        question = html.read()
        return BeautifulSoup(question, "html.parser")


@pytest.fixture
def question_example_as_dict() -> Dict:
    """
    A question example returned as a dictionary.

    Returns
    -------
    Dict
        A question with associated metadata.
    """
    return {
        "id": "15-45664QE",
        "congressman": "M. Sébastien Nadot",
        "questioned_ministry": "Europe et affaires étrangères",
        "responsible_ministry": "Europe et affaires étrangères",
        "question_date": "21/06/2022",
        "response_date": "21/06/2022",
        "theme": "politique extérieure",
        "sub_theme": "Reconnaissance de l'État de Palestine par la France, pourquoi attendre encore ?",
        "analysis": "",
        "question_text": """M. Sébastien Nadot interroge Mme la ministre de l'Europe et des affaires étrangères sur l'État d'Israël qui continue d'expulser des familles palestiniennes pour assoir et élargir l'occupation de la Palestine. Face aux infractions répétées d'Israël au droit international et au non-respect des accords entérinés sous l'égide des Nations unies, la France n'a de cesse de répéter qu'elle continuera d'apporter son plein soutien à « la création de deux États, vivant en paix et en sécurité, à l'intérieur de frontières sûres et reconnues sur la base des lignes de 1967, ayant tous deux Jérusalem pour capitale. » Face à l'occupation israélienne, la France rappelle ainsi à juste titre le droit international. L'année 2023 marquera le 75e anniversaire de l'adoption de la résolution 181 des Nations unies sur le partage de la Palestine et la création de l'État d'Israël. Pourtant, la Palestine reste sous occupation israélienne. La bande de Gaza est assiégée et subit un blocus avec des conséquences graves sur la situation humanitaire, Jérusalem-Est et les villages palestiniens de sa périphérie sont annexés illégalement depuis 1967 et l'empiètement d'Israël sur les territoires palestiniens de Cisjordanie se poursuivent, au point que la viabilité d'un futur État de Palestine interroge, tout cela en violation flagrante de la 4e convention de Genève et du droit international coutumier. Lorsque la Russie a agressé l'Ukraine et envahi ses territoires, la France a participé pleinement aux sanctions économiques contre la Russie. Il s'agit d'un outil du droit international parmi d'autres que la France n'a pas jusqu'à présent choisi. Concernant Israël, la France s'ingénie à discourir sans jamais agir. 130 pays ont déjà choisi une reconnaissance pleine et entière de la Palestine. Pour sortir des discours de bonnes intentions à répétition, il lui demande si elle peut indiquer quand la France engagera concrètement et officiellement la reconnaissance de l'État palestinien, en accord avec les prises de position des deux chambres du Parlement ; car enfin, comment peut-on prétendre défendre incessamment une solution à deux États en n'en reconnaissant qu'un seul des deux ? Il lui demande sa position sur ce sujet.""",
        "response_text": ""
    }
