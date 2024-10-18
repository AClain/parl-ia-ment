import logging
import re
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from errors.NotATagException import NotATagException
from models.Question import Question
from scrapers.questions.scrape_post_13_questions import ScrapePost13Questions
from scrapers.questions.scrape_pre_13_questions import ScrapePre13Questions
from scrapers.questions.scrape_post_16_questions import ScrapePost16Questions


class ScrapeSearchTool:
    @staticmethod
    def for_question_links(response: BeautifulSoup) -> List[str]:
        """
        Scrape question links.

        Parameters
        ----------
        response: BeautifulSoup
            HTML parsed content.

        Returns
        -------
        List[str]
            List of question links.
        """
        regex = re.compile(
            (
                r"^https://questions\.assemblee-nationale\.fr"
                r"/q\d{1,2}/\d{1,2}-\d{1,}QE|QG|QOSD\.htm|html$"
            )
        )
        question_links = [
            match["href"] for match in response.find_all("a", href=regex)
        ]
        return question_links

    @staticmethod
    def extract_question_id(url: str) -> str | None:
        """
        Extracts the question ID from the question URL.

        Parameters
        ----------
        url: str
            The question URL.

        Returns
        -------
        str | None
            If matched, returns the question ID.
        """
        regex = re.compile(r"(\d{1,2}-\d{1,}(QE|QG|QOSD))\.htm|html$")
        result = re.search(regex, url)
        if result:
            return result.group(1)
        else:
            logging.error("Could not retrieve the question ID.")

    @staticmethod
    def for_question_content(
        question_link: str,
        question_id: str,
        legislature: int
    ) -> Question | None:
        """
        Scrape question content from a given question HTML page.

        Parameters
        ----------
        question_link: str
            Link to the question HTML page.
        question_id: str
            ID of the question.
        legislature: int
            The 'legislature' number.

        Returns
        -------
        Question | None
            A question metadata.
        """
        if legislature <= 13:
            scraper = ScrapePre13Questions()
            try:
                scraper.question_scraper(question_link, question_id)
                if scraper.question_data != {}:
                    return Question(**scraper.question_data)
                else: 
                    logging.error(f"data could not be parsed for question : {question_id}")
            except requests.HTTPError:
                return
        elif legislature <= 15:
            scraper = ScrapePost13Questions()
            try:
                scraper.question_scraper(question_link, question_id)
                return Question(**scraper.question_data)
            except requests.HTTPError:
                return
        else:
            scraper = ScrapePost16Questions()
            try:
                scraper.question_scraper(question_link, question_id)
                return Question(**scraper.question_data)
            except requests.HTTPError:
                return
            

    @staticmethod
    def for_next_button(
        response: BeautifulSoup,
        legislature: int,
        questions_per_page: int
    ) -> str | None:
        """
        Scrape next button to gather

        Parameters
        ----------
        response: BeautifulSoup
            Parsed HTML content.
        legislature: int
            Number of the 'legislature'.
        questions_per_page: int
            Number of questions displayed per result page.

        Returns
        -------
        str | None
            The URL of the next page. Returns None if the current page was the
            last page.

        Raises
        ------
        NotATagException
            If the 'Next' button is not present on the page.
        """
        regex = re.compile(rf"/recherche/resultats_questions/{legislature}/\(offset\)(.+)?")
        prefix = ("https://www2.assemblee-nationale.fr")
        regex_replace_offset = re.compile(r"\(offset\)\/(\d+)\/\(query\)")
        print(re.search(regex, str(response)))
        print(response.find_all("a", attrs={"href": "/recheche/resultats_questions"}))
        next_page = response.find("a", attrs={"href": regex})
        if next_page is None:
            raise ValueError("The 'Next' button could not be retrieved.")
        next_page_suffix = regex_replace_offset.sub(
            r"(offset)/{}/(query)".format(questions_per_page),
            next_page.get("href")  # type: ignore
        )
        if type(next_page) is Tag:
            return f"{prefix}{next_page_suffix}"
        else:
            raise NotATagException(tag=next_page)  # type: ignore
