from scrapers.questions.scrape_post_16_questions import ScrapePost16Questions


def test_qe_metadata_formatter(question_16_qe_html):
    scraper = ScrapePost16Questions()
    scraper.data_formater(question_16_qe_html, "16-200QE")
    result = scraper.question_data
    expected = {
        "congressman": "Mme Marie-Pierre Rixain",
        "question_date": "26/07/2022",
        "response_date": "27/09/2022",
        "theme": "Agriculture",
        "questioned_ministry": "Agriculture",
        "responsible_ministry": "Agriculture et souveraineté alimentaire",
    }
    assert result == expected
