import os

os.sys.path.append(os.path.join(os.getcwd(), "src"))

from dotenv import load_dotenv
from databases.connector import Connector
from models.ExportFormat import ExportFormat
import json
from models.Theme import Theme
from utils.helpers import generate_theme_unique_identifier

load_dotenv()


def insert_themes(themes, parent_identifier=None):
    connector = Connector(ExportFormat.JSON)
    for theme in themes:
        processed.append(theme["name"])
        unique_identifier = generate_theme_unique_identifier(
            theme["name"], theme["level"]
        )

        theme_doc = Theme(
            name=theme["name"],
            parent_theme_identifier=parent_identifier,
            unique_identifier=unique_identifier,
            level=theme["level"],
            total=theme["total"],
        )

        connector.client.upsert_theme(theme_doc)

        if "children" in theme:
            insert_themes(theme["children"], unique_identifier)


if __name__ == "__main__":
    with open("src/data/hierarchy.json") as f:
        hierarchy = json.load(f)

    processed = []

    insert_themes(hierarchy)

    print(len(processed))
