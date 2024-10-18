from models.Question import Question


def test_question_date_serializer(question_example_as_dict):
    result = Question(**question_example_as_dict).model_dump()
    expected = "2022-06-21"
    assert result["question_date"] == expected


def test_question_type_serializer(question_example_as_dict):
    result = Question(**question_example_as_dict).model_dump()
    expected = "QE"
    assert result["question_type"] == expected
