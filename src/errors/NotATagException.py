from bs4.element import NavigableString


class NotATagException(Exception):
    """
    Exception raised when the 'Suivant' button is a not a BeautifulSoup
    Tag element.
    """

    def __init__(self, tag: NavigableString | None, msg: str | None = None):
        if not msg:
            self.msg = f"The accessed tag '{tag}'" \
                + "is probably a NavigableString."
            super().__init__(self.msg)
