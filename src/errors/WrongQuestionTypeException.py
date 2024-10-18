class WrongQuestionTypeException(Exception):
    """
    Exception raised when the 'Suivant' button is a not a BeautifulSoup
    Tag element.
    """

    def __init__(self, msg: str | None = None):
        if not msg:
            self.msg = "An error occurred with building the question type."
            super().__init__(self.msg)
