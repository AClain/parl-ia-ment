import logging
import re
import requests
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag


class ScrapePost13Questions:

    def __init__(self) -> None:
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
                f"HTTP query failed with error : {response.text},"
                f" for URL : {url}."
            )

    def data_formater(self, soup: BeautifulSoup, question_id: str) -> None:
        """
        Retrieve each question metadata piece.

        Parameters
        ----------
        soup: BeautifulSoup
            Parsed HTML page.
        question_id: str
            ID of the question.
        """
        question_headers = soup\
            .find("section", class_="question_header")
        if question_headers is None:
            logging.error(
                f"Page for question ID '{question_id}' did not match the expected format."
            )
            return
        question_ministery = soup\
            .find("section", class_="question_info")\
            .find("div", class_="ministere")\
            .find_all("div")  # type: ignore
        question_text = soup\
            .find("section", class_="question_answer")\
            .find_all("div")  # type: ignore
        question_infos = soup\
            .find("section", class_="question_info")\
            .find("div", class_="analyse_header")\
            .find_all('div')  # type: ignore
        question_dates = soup\
            .find("div", class_="question_publish_date")\
            .find_all("div")  # type: ignore
        self.question_data["id"] = question_id
        self.question_data["congressman"] = question_headers\
            .find("span")\
            .find("a")\
            .get_text(strip=True)  # type: ignore
        self.question_data["questioned_ministry"] = self.string_cleaner(
            question_ministery[0].get_text(strip=True)
        )
        self.question_data["responsible_ministry"] = self.string_cleaner(
            question_ministery[1].get_text(strip=True)
        )
        self.question_data["question_date"] = self.filter_question_date(
            question_dates
        )
        self.question_data["response_date"] = self.filter_response_date(
            question_dates
        )
        self.question_data["theme"] = self.string_cleaner(
            question_infos[0].find("p").get_text(strip=True)
        )
        self.question_data["sub_theme"] = self.string_cleaner(
            question_infos[1].find("p").get_text(strip=True)
        )
        try:
            self.question_data["analysis"] = self.string_cleaner(
                question_infos[2].find("p").get_text(strip=True)
            )
        except IndexError:
            self.question_data["analysis"] = ""
        self.question_data["question_text"] = question_text[0]\
            .find("p")\
            .get_text(strip=True)
        self.question_data["response_text"] = question_text[1]\
            .find("div", class_="reponse_contenu")\
            .get_text(strip=True)

    @staticmethod
    def filter_response_date(date_divs: List[Tag]) -> str:
        """
        Filters out the response date.

        Parameters
        ----------
        date_divs: List[Tag]
            List of tags pre-filtered, containing question dates.

        Returns
        -------
        str
            Returns a Tag if the pattern associated to the response
            date.
        """
        for div in date_divs:
            if "Réponse publiée au JO" in div.get_text(strip=True):
                response_div = div.find("span", class_="question_big_content")
                if response_div:
                    return response_div.get_text(strip=True)
        return ""

    @staticmethod
    def filter_question_date(date_divs: List[Tag]) -> str:
        """
        Filters out the question date.

        Parameters
        ----------
        date_divs: List[Tag]
            List of tags pre-filtered, containing question dates.

        Returns
        -------
        str
            Returns a Tag if the pattern associated to the question
            date.
        """
        for div in date_divs:
            if "Question publiée au JO" in div.get_text(strip=True):
                question_div = div.find("span", class_="question_big_content")
                if question_div:
                    return question_div.get_text(strip=True)
        return ""

    @staticmethod
    def string_cleaner(string: str) -> str:
        """
        Removes unwanted characters.

        Parameters
        ----------
        string: str
            String to be cleaned.

        Returns
        -------
        str
            String cleaned.
        """
        cleaning_string = re.sub(r".*>", "", string)
        return cleaning_string
