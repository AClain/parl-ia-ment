from scrapers.questions.scrape_old_questions import ScrapeOldQuestions


def test_scrape_question_8():
    url = "https://questions.assemblee-nationale.fr/q8/8-53QG.htm"
    scraper = ScrapeOldQuestions()
    scraper.question_scraper(url, "8-53QG")
    result = scraper.question_data
    expected = {
        "id": "8-53QG",
        "congressman": "M.Hannoun Michel",
        "questioned_ministry": "industrie,  PTT et tourisme",
        "responsible_ministry": "industrie,  PTT et tourisme",
        "question_date": "08/05/1986",
        "response_date": "08/05/1986",
        "theme": "Electricite et gaz",
        "sub_theme": "Centrales d'EDF",
        "analysis": "Centrales nucleaires; securite des installations et de leur exploitation; URSS; centrale de Tchernobyl; accident; consequences",
        "question_text": "",
        "response_text": ""
    }

    assert result == expected
