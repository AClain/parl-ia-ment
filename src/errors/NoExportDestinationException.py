class NoExportDestinationException(Exception):
    """
    Exception raised when the export mode required an export
    destination which was not provided.
    """

    def __init__(self, msg: str | None = None) -> None:
        if not msg:
            self.msg = "No export destination path provided."
            super().__init__(self.msg)
