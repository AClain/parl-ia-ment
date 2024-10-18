from models.Question import Question
from databases.mongo_connector import Mongo


def export_to_mongo(
    question: Question,
) -> None:
    """
    Export questions metadata to JSON file.

    Parameters
    ----------
    question: Question
        The question and its associated metadata.
    """
    mongo = Mongo()
    mongo.upsert_question(question)
    mongo.client.close()
