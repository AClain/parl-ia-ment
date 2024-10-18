from models.Question import Question


def test_question_congressman_validator(question_example_as_dict):
    result = Question(**question_example_as_dict)
    assert result.congressman == "Sébastien Nadot"
