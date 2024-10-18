import pytest
from models.Question import Question, QuestionType


def test_extract_question_ecrite_from_question_id():
    expected = QuestionType.QUESTION_ECRITE
    result = Question.extract_question_type("12-1234QE")
    assert result == expected

def test_extract_question_gouvernement_from_question_id():
    expected = QuestionType.QUESTION_AU_GOUVERNEMENT
    result = Question.extract_question_type("10-20QG")
    assert result == expected

def test_extract_question_orale_from_question_id():
    expected = QuestionType.QUESTION_ORALE_SANS_DEBAT
    result = Question.extract_question_type("8-45890QOSD")
    assert result == expected

def test_extract_error_from_question_id():
    expected = "Question ID does not have the right format"
    with pytest.raises(ValueError, match=expected):
        Question.extract_question_type("4-10QOG")
