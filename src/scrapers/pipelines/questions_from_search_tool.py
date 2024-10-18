import logging
import re
from tqdm import tqdm
from models.ExportFormat import ExportFormat
from databases.connector import Connector
from exporters.export import export_question
from scrapers.queries.query_search_tool import query_search_tool
from scrapers.scrape_search_tool import ScrapeSearchTool


def questions_from_search_tool(
    legislature: int,
    export_format: ExportFormat,
    questions_per_page: int,
    log_question_ids: bool,
    url: str | None = None,
) -> None:
    """
    Retrieve questions metadata from the search tool.

    Parameters
    ----------
    legislature: int
        The 'legislature' number.
    export_format: ExportFormat
        Export format.
    question_per_page: int
        Number of question entries per page.
    log_question_ids: bool
        Log the ID of each question scraped.
    url: str | None, default=None
        The URL from which to start scraping.

    Raises
    ------
    ValueError
        If the URL is not properly formatted for the
        'https://question.assemblee-nationale.fr' website.
    """
    connector = Connector(export_format)
    if url is None:
        next_page = query_search_tool(
            legislature=legislature, questions_per_page=questions_per_page
        )
    else:
        next_page = query_search_tool(
            url=url, legislature=legislature, questions_per_page=questions_per_page
        )

    if url is None:
        question_offset = 0
    else:
        regex = re.compile(r"\(offset\)\/(\d+)\/\(query\)")
        cap = re.search(regex, url)
        if cap is not None:
            question_offset = int(cap.group(1))
        else:
            raise ValueError("URL is not properly formatted.")
    while next_page is not None:
        questions_url = ScrapeSearchTool.for_question_links(next_page)
        for url in tqdm(questions_url):
            question_id = ScrapeSearchTool.extract_question_id(url)
            if log_question_ids:
                logging.info(f"Scraping question with ID : {question_id}")
            if question_id and not connector.client.check_question(question_id):
                question = ScrapeSearchTool.for_question_content(
                    url, question_id, legislature
                )
                if question is not None:
                    export_question(question=question, export_format=export_format)
        question_offset += int(questions_per_page)
        next_page_link = ScrapeSearchTool.for_next_button(
            next_page, legislature=legislature, questions_per_page=question_offset
        )
        next_page = query_search_tool(
            url=next_page_link,  # type: ignore
            legislature=legislature,
            questions_per_page=questions_per_page,
            next_page_query=True,
        )
