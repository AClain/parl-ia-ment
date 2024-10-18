import logging
import requests
from bs4 import BeautifulSoup


def query_search_tool(
    url: str = (
        "https://www2.assemblee-nationale.fr"
        "/recherche/resultats_questions"
    ),
    body: str | None = None,
    questions_per_page: int = 100,
    legislature: int = 16,
    next_page_query: bool = False
) -> BeautifulSoup:
    """
    Queries the Assemblée nationale 'Questions au gouvernement' search tool.

    Parameters
    ----------
    url: str, default="https://www2.assemblee-nationale.fr/recherche/resultats_question" # noqa
        URL of the query search tool.
    body: str, default=None
        Body of the HTTP request.
    legislature: int, default=16
        The 'legislature' number.
    next_page_query: bool, default=False
        Defines if the query is initiated by clicking on the button 'Suivant'.

    Returns
    -------
    BeautifulSoup
        Parsed content of the response web page.
    """
    if body is None:
        body = (
            f"legislature={legislature}&ssTypeDocument%5B%5D=qe"
            "&ssTypeDocument%5B%5D=qg&"
            "ssTypeDocument%5B%5D=qosd&replies%5B%5D=ar"
            "&replies%5B%5D=sr&removed%5B%5D=0&"
            "removed%5B%5D=1&q=&q_in=0&id_auteur=&departement=&"
            "groupePolitique=&rubrique=&"
            "ministereInterroge=&ministereAttributaire=&causeCloture=&"
            "numDocument=&typeDate=&"
            "typeDate_start=&typeDate_end=&typeDate_exact=&"
            "criteres%5B0%5D%5Bfield%5D=&"
            "criteres%5B0%5D%5Bvalue%5D=&criteres%5B1%5D%5Bfield%5D=&"
            "criteres%5B1%5D%5Bvalue%5D=&"
            "criteres%5B2%5D%5Bfield%5D=&criteres%5B2%5D%5Bvalue%5D=&"
            f"sort_by=ssTypeDocument&sort_order=asc&limit={questions_per_page}"
        )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    if next_page_query:
        r = requests.get(url, headers=headers)
    else:
        r = requests.post(
            url,
            data=body,
            headers=headers
        )

    logging.info(f"Querying search tool with URL : {url}.")
    soup = BeautifulSoup(r.text, "html.parser")

    if type(soup) is BeautifulSoup:
        return soup
    else:
        raise ValueError("HTML page content returned is not parsed correctly.")
