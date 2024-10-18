import logging
import re
import requests
from typing import Tuple
from lxml import etree
from bs4 import BeautifulSoup
from models.Question import Question, QuestionType


class ScrapePost16Questions:

    def __init__(self):
        self.data = {}
        self.data["questions"] = []
        self.question_data = {}

    def question_scraper(self, url: str, question_id: str) -> None:
        """
        Scrape a given question metadata.

        Parameters
        ----------
        url: str
            URL of the question.
        question_id: str
            ID of the question.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            self.data_formater(soup, question_id)
        else:
            logging.error(
                f"HTTP query failed with error: {response.text},"
                f" for URL : {url}."
            )

    def data_formater(self, soup: BeautifulSoup, question_id: str) -> None:
        self.question_data["congressman"] = self.retrieve_congressman_name(soup)
        self.question_data["question_date"] = self.retrieve_question_date(
            soup, Question.extract_question_type(question_id)
        )
        self.question_data["response_date"] = self.retrieve_response_date(
            soup, Question.extract_question_type(question_id)
        )
        self.question_data["theme"] = self.retrieve_rubrique(soup)
        self.question_data["responsible_ministry"] = self.retrieve_ministere_res(soup)
        self.question_data["questioned_ministry"] = self.retrieve_ministere_int(soup)

    def retrieve_rubrique(self, soup: BeautifulSoup) -> str:
        """
        Retrieve the 'rubrique' content.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns    
        -------
        str
            The 'rubrique' content.
        """
        dom = etree.HTML(str(soup))
        cap = dom.xpath("//p[contains(text(), 'Rubrique :')]/span")
        return cap[0].text

    def retrieve_ministere_int(self, soup: BeautifulSoup) -> str:
        """
        Retrieve the questionned ministry.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        str
            The questionned ministry.
        """
        dom = etree.HTML(str(soup))
        cap = dom.xpath("//p[contains(text(), 'Ministère interrogé :')]/span")
        return cap[0].text

    def retrieve_ministere_res(self, soup: BeautifulSoup) -> str:
        """
        Retrieve the responding ministry.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        str
            The responding ministry.
        """

        res = soup.find("p", attrs={"id": "blocMinistereAttributaire"}).find("span")  # type: ignore
        if res is None:
            raise ValueError("Unexpected format for 'Ministère répondant'.")
        else:
            return res.get_text(strip=True)

    def retrieve_question_date(
        self,
        soup: BeautifulSoup,
        question_type: QuestionType
    ) -> str:
        """
        Retrieve the question date.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        str
            The question date.

        Raises
        ------
        ValueError
            If the question type or the question date could not be retrieved
            properly.
        """
        if question_type == QuestionType.QUESTION_ECRITE:
            dom = etree.HTML(str(soup))
            cap = dom.xpath("//span[contains(text(), 'Question publiée le')]/a")
            return cap[0].text
        elif question_type == QuestionType.QUESTION_AU_GOUVERNEMENT \
            or question_type == QuestionType.QUESTION_ORALE_SANS_DEBAT:
            regex = re.compile(r"(\d{1,} .+ \d{4}$)")
            dom = etree.HTML(str(soup))
            cap = dom.xpath("//p[contains(text(), 'Date de la séance :')]/span")
            cap = re.search(regex, cap[0].text)
            if cap is not None:
                return cap.group(1)
            else:
                raise ValueError("Question date could not be retrieved properly.")
        else:
            raise ValueError("Unexpected question type.")


    def retrieve_response_date(
        self,
        soup: BeautifulSoup,
        question_type: QuestionType
    ) -> str:
        """
        Retrieve the response date.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        str
            The response date.
        """
        if question_type == QuestionType.QUESTION_ECRITE:
            dom = etree.HTML(str(soup))
            cap = dom.xpath("//span[contains(text(), 'Réponse publiée le')]")
            return cap[0].text
        elif question_type == QuestionType.QUESTION_AU_GOUVERNEMENT \
            or question_type == QuestionType.QUESTION_ORALE_SANS_DEBAT:
            regex = re.compile(r"(\d{1,} .+ \d{4}$)")
            dom = etree.HTML(str(soup))
            cap = dom.xpath("//p[contains(text(), 'Date de la séance :')]/span")
            cap = re.search(regex, cap[0].text)
            if cap is not None:
                return cap.group(1)
            else:
                raise ValueError("Question date could not be retrieved properly.")
        else:
            raise ValueError("Unexpected question type.")

    def retrieve_congressman_name(self, soup: BeautifulSoup) -> str:
        """
        Retrieve the congressman name.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        str
            The congressman name.

        Raises
        ------    
        ValueError
            If the congressman name could not be retrieved properly.
        """
        regex = re.compile(
            r"^https://www.assemblee-nationale.fr/dyn/deputes/PA\d{1,}$"
        )
        res = soup.find("a", attrs={"href": regex})
        if res is None:
            raise ValueError("Congressman name could not be retrieved properly.")

        clean_regex = re.compile(r"(.+) \(.+\)")
        cap = re.search(clean_regex, res.get_text(strip=True))
        if cap is not None:
            return cap.group(1)
        else:
            raise ValueError("Congressman name could not be retrieved properly.")

    def retrieve_question_text_and_response_text(
        self,
        soup: BeautifulSoup
    ) -> Tuple[str, str]:
        """
        Retrive the question and response text content.

        Parameters
        ----------
        soup: BeautifulSoup
            The parsed web page.

        Returns
        -------
        Tuple[str, str]
            The question and response text content :
            - The question text as the first element of the tuple
            - The response text as the second element of the tuple
        """
        qar = soup.find_all("p", attrs={"class": "_pa-small"})
        return (
            qar[1].get_text(strip=True),
            qar[0].get_text(strip=True)
        )
