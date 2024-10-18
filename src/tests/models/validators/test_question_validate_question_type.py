from models.Question import Question, QuestionType


def test_question_type_validator(question_example_as_dict):
    result = Question(**question_example_as_dict)
    expected = QuestionType.QUESTION_ECRITE
    assert result.question_type == expected
