class WrongRunIdProvided(Exception):
    """
    Exception raised when a provided PromptRun ID
    does not match any record in the database.
    """

    def __init__(self, run_id: str, msg: str | None = None) -> None:
        if not msg:
            self.msg = "No records matched for the provided PromptRun ID."
