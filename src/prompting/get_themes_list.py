from typing import Tuple, List
from databases.connector import Connector
from models.ExportFormat import ExportFormat

connector = Connector(ExportFormat.JSON)


def get_accepted_themes_list_from_themes_list(themes_list: List[str]) -> List[str]:
    accepted_themes_for_questions = []
    for theme in themes_list:
        sub_themes = connector.client.get_sub_themes_list_from_theme(
            theme["unique_identifier"], flatten=True
        )
        for sub_theme in sub_themes:
            if sub_theme["name"] not in accepted_themes_for_questions:
                accepted_themes_for_questions.append(sub_theme["name"])

    return accepted_themes_for_questions


def selected_level_1_themes_first_version(
    extended_themes_list: List[str] = [],
) -> Tuple[List[str], int]:
    themes_list = [
        "retraites",
        "ministères et secrétariats d'état",
        "handicapés",
        "enseignement",
        "politique extérieure",
        "agriculture",
        "logement",
        "anciens combattants et victimes de guerre",
        "énergie et carburants",
        "impôts et taxes",
        "sécurité sociale",
        "justice",
        "entreprises",
        "outre-mer",
        "déchets, pollution et nuisances",
        "communes",
        "commerce et artisanat",
        "sports",
        "consommation",
        "famille",
        "étrangers",
    ]
    themes_list.extend(extended_themes_list)
    theme_hierarchy_level = 1

    return (themes_list, theme_hierarchy_level)


def selected_level_1_themes_first_version_en() -> Tuple[List[str], int]:
    themes_list = [
        "retirement",
        "ministries and state secretariats",
        "disabled people",
        "education",
        "foreign policy",
        "agriculture",
        "housing",
        "veterans and war victims",
        "energy and fuels",
        "taxes and levies",
        "social security",
        "justice",
        "businesses",
        "overseas territories",
        "waste, pollution, and nuisances",
        "municipalities",
        "commerce and craftsmanship",
        "sports",
        "consumption",
        "family",
        "foreigners",
    ]

    theme_hierarchy_level = 1

    return (themes_list, theme_hierarchy_level)
