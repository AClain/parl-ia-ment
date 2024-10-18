from typing import Any


class NoIdInQuestionException(Exception):
    """
    Exception raised when a metadata retrieved from
    a question did not contain the question ID.
    """

    def __init__(
        self,
        question_data: Any,
        msg: str | None = None
    ) -> None:
        if not msg:
            self.msg = (
                "The following question data does not contain"
                " a question ID. Question data content :\n"
                f"{question_data}\n"
            )
            super().__init__(self.msg)
