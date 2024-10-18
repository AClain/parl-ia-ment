class ThemesListTooLongException(Exception):
    """
    Exception raised when the themes list provided in the LLM
    prompt is too long.
    """

    def __init__(self, msg: str | None = None):
        if not msg:
            self.msg = (
                "The themes list provided is too long."
                " It should not exceed 24 themes if used with proxy selectors :"
                " selectors span from the letter 'A' to 'Z' only."
            )
            super().__init__(msg)
