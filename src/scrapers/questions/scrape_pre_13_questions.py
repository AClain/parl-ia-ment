import logging
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from pydantic import ValidationError
from models.Question import Question


class ScrapePre13Questions:
    """
    Scraping functions to retrieve questions metadata starting from
    the XIIIth term of office.

    Attributes
    ----------
    data: Question
        Metadata of the question.
    question_data: List[Question]
        List of questions.
    """

    def __init__(self):
        self.data = {}
        self.data["questions"] = []
        self.question_data = {}

    def question_scraper(self, url: str, question_id: str) -> None:
        """
        Iterate over a question sections.

        Parameters
        ----------
        url: str
            URL to the question content.
        question_id: str
            ID of the question.
        """
        response = requests.get(
            url,
            headers={
                "user-agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) "
                    "Gecko/20100101 Firefox/126.0"
                )
            }
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.find('div', id="printtop"):
                logging.error(f"weird old format for url : {url} skip to the next page")
            else :
                table = soup.find("table")
                if (type(table) is not NavigableString) and (table is not None):
                    rows = table.find_all("tr")  # type: ignore

                    for row in rows:
                        col = row.find("td")
                        self.get_content_td(col, question_id)
                        self.check_all_key()
                    # try:
                    #     self.data["questions"].append(self.question_data)
                    # except ValidationError:
                    #     logging.error(f"Validation error occurred with question : {question_id}.")
                    #     raise ValueError("Wrong question metadata")
                else:
                    logging.error(
                        f"Scraped page for URL : '{url}' does not match the expected format."
                    )
        else:
            logging.error(
                f"HTTP query failed with error : {response.text},"
                f" for URL : {url}."
            )
            raise requests.HTTPError(f"Requesting for question with ID {question_id} failed.")

    def get_content_td(self, col: Tag, question_id: str) -> None:
        """
        Retrieve the questions metadata.

        Parameters
        ----------
        col: Tag
            Content of the question.
        question_id: str
            ID of the question.
        """
        try:
            text = col.get_text(strip=True)
            try:
                if "Question N" in text:
                    try:
                        self.question_data["id"] = question_id
                        congressman = col.find_next_sibling("td")\
                        .get_text(strip=True)
                        self.question_data["congressman"] = self\
                            .name_congressman_cleaner(congressman)
                    except:
                        self.question_data["congressman"] = None
                elif re.search(r"Minist.{1,2}re interrog.", text):
                    try:
                        q_ministry = col.find_next_sibling("td")\
                            .get_text(strip=True)
                        self.question_data["questioned_ministry"] = q_ministry
                    except:
                        self.question_data["questioned_ministry"] = None
                elif re.search(r"Minist.{1,2}re attributaire", text):
                    try:
                        r_ministry = col.find_next_sibling("td")\
                            .get_text(strip=True)
                        self.question_data["responsible_ministry"] = r_ministry
                    except:
                        self.question_data["responsible_ministry"] = None
                elif re.search(
                    r"Question publi.{1,2}e au",
                    col.find_next_sibling("td").get_text(strip=True)
                ):
                    try:
                        question_date = col.find_next_sibling("td")\
                            .get_text(strip=True)
                        self.question_data["question_date"] = self.date_cleaner(
                            question_date
                        )
                    except:
                        self.question_data["question_date"] = None
                elif  re.search(
                    r"R.{1,2}ponse publi.{1,2}e au",
                    col.find_next_sibling("td").get_text(strip=True)):
                    try:
                        response_date = col.find_next_sibling("td")\
                            .get_text(strip=True)
                        self.question_data["response_date"] = self.date_cleaner(
                            response_date
                        )
                    except:
                        self.question_data["response_date"] = None
                elif "Rubrique" in text:
                    try:
                        theme = col.find_next_sibling("td").get_text(strip=True)
                        self.question_data["theme"] = theme
                    except:
                        self.question_data["theme"] = None
                elif re.search(r"T.{1,2}te d'analyse", text):
                    try:
                        sub_theme = col.find_next_sibling("td")\
                            .get_text(strip=True)
                        self.question_data["sub_theme"] = sub_theme
                    except:
                        self.question_data["sub_theme"] = None
                elif "Analyse :" in text:
                    try:
                        analysis = col.find_next_sibling('td').get_text(strip=True)
                        self.question_data["analysis"] = analysis
                    except:
                        self.question_data["analysis"] = None
                elif "Texte de la QUESTION" in text:
                    try:
                        question_text = col.find_next_sibling('td')\
                            .get_text(strip=True)
                        self.question_data["question_text"] = question_text
                    except:
                        self.question_data["question_text"] = None
                elif "Texte de la REPONSE" in text:
                    try:
                        response_text = col.find_next_sibling('td')\
                            .get_text(strip=True)
                        self.question_data["response_text"] = response_text
                    except:
                        self.question_data["response_text"] = None
                elif "DEBAT" in text:
                    try:
                        debat_text = col.find_next_sibling('td')\
                            .get_text(strip=True)
                        self.question_data["question_text"] = debat_text
                        self.question_data["response_text"] = None
                    except:
                        self.question_data["question_text"] = None
                        self.question_data["response_text"] = None
            except:
                pass
        except AttributeError:
            logging.error(
                f"Error happened when parsing question with ID {question_id}."
            )

    def check_all_key(self) -> None:
        """
        Check each question metadata values.
        """
        data = self.question_data
        if "id" not in data:
            self.question_data["id"] = None
        elif "congressman" not in data:
            self.question_data["congressman"] = None
        elif "questioned_ministry" not in data:
            self.question_data["questioned_ministry"] = None
        elif "responsible_ministry" not in data:
            self.question_data["responsible_ministry"] = None
        elif "question_date" not in data:
            self.question_data["question_date"] = None
        elif "response_date" not in data:
            self.question_data["response_date"] = None
        elif "theme" not in data:
            self.question_data["theme"] = None
        elif "sub_theme" not in data:
            self.question_data["sub_theme"] = None
        elif "analysis" not in data:
            self.question_data["analysis"] = None
        elif "question_text" not in data:
            self.question_data["question_text"] = None
        elif "response_text" not in data:
            self.question_data["response_text"] = None

    def name_congressman_cleaner(self, name: str) -> str | None:
        """
        Cleans the congressman metadata from the question content.

        Parameters
        ----------
        name: str
            Name of the congressman in the question metadata.

        Returns
        -------
        str | None
            If found, returns the question congressman metadata.
        """
        cleaned_name = re.search(r'^(de)?(.+)(\(.+\)?)', name)
        if cleaned_name:
            cleaned_name = cleaned_name.group(2)
        return cleaned_name

    def date_cleaner(self, date) -> str | None:
        """
        Cleans the date metadata from the question content.

        Parameters
        ----------
        date: str
            Date in the question metadata.

        Returns
        -------
        str | None
            If found, returns the question date metadata.
        """
        match = re.search(r'\d{2}/\d{2}/\d{4}', date)
        if match:
            date = match.group(0)
            return date
