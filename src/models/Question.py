from __future__ import annotations
import re
from enum import Enum
from datetime import date, datetime
from typing import Any, Dict, List
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    field_serializer
)
from errors.NoIdInQuestionException import NoIdInQuestionException
from errors.WrongQuestionTypeException import WrongQuestionTypeException


class QuestionType(Enum):
    QUESTION_ORALE_SANS_DEBAT = "QOSD"
    QUESTION_ECRITE = "QE"
    QUESTION_AU_GOUVERNEMENT = "QG"


class QuestionsByTheme(BaseModel):
    """
    A given theme containing all the associated questions.
    """
    legislature: List[int]
    theme: str
    total_number_of_questions: int
    urls: List[str]


class Question(BaseModel):
    """
    Representation of a question.
    """
    id: str
    congressman: str
    questioned_ministry: str
    responsible_ministry: str
    question_date: date | None
    response_date: date | None
    theme: str
    sub_theme: str
    analysis: str | None
    question_text: str
    response_text: str | None
    question_type: QuestionType

    @staticmethod
    def extract_question_type(question_id: str) -> QuestionType:
        """
        Extract the question type from a given question ID.

        Parameters
        ----------
        question_id: str

        Returns
        -------
        QuestionType
            The question type.

        Raises
        ------
        ValueError
            If the question ID does not have the expected format.
        """
        regex = re.compile(r"^\d{1,}-\d{1,}(QE|QOSD|QG)")
        cap = re.search(regex, question_id)
        if cap is not None:
            return QuestionType(cap.group(1))
        else:
            raise ValueError("Question ID does not have the right format.")

    @field_serializer("question_date", "response_date")
    def export_date_as_string(self, value: datetime) -> str | None:
        if value:
            return value.isoformat()
        else:
            return None

    @field_serializer("question_type")
    def export_question_type_as_string(
        self,
        value: QuestionType
    ) -> str | None:
        return value.value

    @model_validator(mode="before")
    @classmethod
    def add_question_type(cls, data: Any) -> Dict:
        regex = re.compile(r"^\d{1,2}-\d{1,}(QE|QOSD|QG)$")
        try:
            captures = re.search(regex, data["id"])
            if captures.group(1) == "QE":  # type: ignore
                data["question_type"] = QuestionType.QUESTION_ECRITE
                return data
            elif captures.group(1) == "QOSD":  # type: ignore
                data["question_type"] = QuestionType.QUESTION_ORALE_SANS_DEBAT
                return data
            elif captures.group(1) == "QG":  # type: ignore
                data["question_type"] = QuestionType.QUESTION_AU_GOUVERNEMENT
                return data
            else:
                raise ValueError("Question type is not valid.")
        except KeyError:
            raise NoIdInQuestionException("No ID for question")
        except AttributeError:
            raise WrongQuestionTypeException(
                "Question type could not be retrieved from question"
                f" with ID : {data['id']}."
            )

    #@field_validator("id", mode="before"):
    #def add_question_type(cls, value: str):
    #    pass

    @field_validator("congressman")
    @classmethod
    def name_congressman_cleaner(cls, value: str) -> str | None:
        cleaned_name = re.search(r"^(de)?(M\.|Mme)(.+)", value)
        if cleaned_name:
            cleaned_name = cleaned_name.group(3)
        if cleaned_name:
            return cleaned_name.strip()
        else:
            return cleaned_name

    @field_validator("question_date", "response_date", mode="before")
    @classmethod
    def date_cleaner(cls, value: str) -> date | None:
        try:
            match = re.search(r'\d{2}/\d{2}/\d{4}', value)
            if match:
                date_str = match.group(0)
                return datetime.strptime(date_str, "%d/%m/%Y").date()
            else:
                return None
        except TypeError:
            return None

    @field_validator("response_text", mode="before")
    @classmethod
    def replace_empty_string_with_none(cls, value: str) -> None:
        if value == "":
            return None

    @field_validator("question_text", "response_text", mode="before")
    @classmethod
    def replace_special_spaces(cls, value: str) -> str | None:
        try:
            value = re.sub("\xa0", " ", value)
            value = re.sub(r"\s{2,}", " ", value)
            return value
        except TypeError:
            return None


QuestionAttributesPattern = {
    "id": {
        "pattern": "Question N° :"
    },
    "congressman": {
        "pattern": "Question N° :"
    },
    "questionned_ministry": {
        "pattern": "re interrogé"
    },
    "responsible_ministry": {
        "pattern": "re attributaire"
    },
    "question_date": {
        "pattern": "Question publiée au"
    },
    "response_date": {
        "pattern": "Réponse publiée au"
    },
    "theme": {
        "pattern": "Rubrique"
    },
    "sub_theme": {
        "pattern": "Tête d'analyse"
    },
    "analysis": {
        "pattern": "Analyse :"
    },
    "question_text": {
        "pattern": "Texte de la QUESTION"
    },
    "response_text": {
        "pattern": "Texte de la REPONSE"
    }
}
