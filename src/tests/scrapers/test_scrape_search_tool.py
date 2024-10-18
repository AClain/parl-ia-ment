from scrapers.scrape_search_tool import ScrapeSearchTool


def test_scrape_search_tool_next_legislature_13(
    search_tool_next_html
):
    result = ScrapeSearchTool.for_next_button(
        search_tool_next_html["html"],
        legislature=13
    )
    expected = search_tool_next_html["href"]

    assert result == expected


def test_scrape_search_tool_question_links(search_tool_question_links_html):
    result = ScrapeSearchTool.for_question_links(
        search_tool_question_links_html
    )
    expected = [
        "https://questions.assemblee-nationale.fr/q15/15-45416QE.htm",
        "https://questions.assemblee-nationale.fr/q15/15-45392QE.htm"
    ]

    assert result == expected
