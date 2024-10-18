from models.LLMOutput import ConfidenceType


class WrongConfidenceTypeException(Exception):
    """
    Exception raised when the confidence type measure does not match
    the settings of the current prompt run.
    """
    
    def __init__(
        self,
        confidence_type: ConfidenceType,
        msg: str | None = None
    ) -> None:
        if not msg:
            self.msg = (
                "The settings of the current prompt run do not allow to run "
                f"a {confidence_type.value} confidence measure. "
                "Please check the settings of the prompt run to make sure "
                "they allow for the confidence type you want to measure."
            )
            super().__init__(self.msg)
