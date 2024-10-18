import os

os.sys.path.append(os.path.join(os.getcwd(), "src"))

from dotenv import load_dotenv
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from models.Theme import Theme

load_dotenv()


def aggregate_total_by_level(theme_level):
    return connector.client.aggregate_themes(
        [
            {"$match": {"level": theme_level}},
            {
                "$group": {
                    "_id": "$parent_theme_identifier",
                    "total_sum": {"$sum": "$total"},
                }
            },
        ]
    )


if __name__ == "__main__":
    connector = Connector(ExportFormat.JSON)
    themes_step_0 = connector.client.get_themes_by_level(0)

    for theme in themes_step_0:
        questions = connector.client.get_questions({"theme": theme["name"]})
        theme["total"] = len(list(questions))
        connector.client.upsert_theme(Theme.parse_obj(theme))

    themes_step_1 = aggregate_total_by_level(0)

    for theme in themes_step_1:
        parent_theme = connector.client.get_theme({"unique_identifier": theme["_id"]})
        if parent_theme is not None:
            parent_theme["total"] = theme["total_sum"]
            connector.client.upsert_theme(Theme.parse_obj(parent_theme))

    themes_step_2 = aggregate_total_by_level(1)

    for theme in themes_step_2:
        parent_theme = connector.client.get_theme({"unique_identifier": theme["_id"]})
        if parent_theme is not None:
            parent_theme["total"] = theme["total_sum"]
            connector.client.upsert_theme(Theme.parse_obj(parent_theme))

    themes_step_3 = aggregate_total_by_level(2)

    for theme in themes_step_3:
        parent_theme = connector.client.get_theme({"unique_identifier": theme["_id"]})
        if parent_theme is not None:
            parent_theme["total"] = theme["total_sum"]
            connector.client.upsert_theme(Theme.parse_obj(parent_theme))
