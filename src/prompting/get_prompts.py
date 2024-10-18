import re
from typing import List
from guardrails import Guard
from guardrails.hub import ValidChoices, ValidRange
from models.Prompt import WrapperEnum
from models.Prompt import PromptText, PromptType, RoleEnum
from prompting.prompt_templates import (
    build_prompt_themes_list,
    build_random_few_shot_prompt,
)
from utils.helpers import print_prompts
from utils.helpers import retrieve_theme_from_cot_response


"""
ZERO-SHOT PROMPT BUILDERS
"""


def zero_shot_minimal(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Attribue un thème au document. Voici la liste des thèmes :"
        f"{themes_list_as_string}\n"
        "Ta réponse ne doit contenir que le thème correspondant "
        "(n'ajoute pas de mise en forme complémentaire, seulement le texte du thème). "
        "Seuls les thèmes de la liste sont valides. "
    )

    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.ZeroShot])


def zero_shot_vanilla(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député à l'Assemblée nationale "
        "française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit contenir une seule chose: le thème correspondant, "
        f"par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.ZeroShot])


#! TO UPDATE
def zero_shot_vanilla_en(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Your role is to assign a theme to a question asked by a "
        "member of the French National Assembly. "
        "The list of themes is as follows:"
        f"{themes_list_as_string}\n"
        "Your response should contain only one thing: the corresponding theme, "
        f"for example `{themes_list[0]}` or `{themes_list[1]}`. "
        "The assigned theme must be one of the themes from the provided list. "
        "Only the themes from the previous list are valid."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.ZeroShot])


def zero_shot_assistant_role(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Agis comme un assistant de recherche chargé d'annoter un corpus de données du "
        "parlement français constitué des questions au gouvernement. "
        "Ton rôle est d'attribuer un thème à une question posée par un député à "
        "l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit contenir une seule chose: le thème correspondant, "
        f"par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.ZeroShot])


def zero_shot_expert_role(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Agis comme un chercheur en sciences politiques, spécialiste des questions "
        "parlementaires françaises et annotateur expert sur le cas des questions au gouvernement. "
        "Ton rôle est d'attribuer un thème à une question posée par un député à l'Assemblée "
        "nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit contenir une seule chose: le thème correspondant, "
        f"par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.ZeroShot])


def zero_shot_proxy(themes_list: List[str], themes_hierarchy_level: int):
    a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

    def validation_func(response: str):
        a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]
        guard = Guard().use(ValidChoices, choices=a_to_z_selectors, on_fail="exception")
        guard.validate(response)

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list,
        theme_level=themes_hierarchy_level,
        with_selector=True,
        selectors=a_to_z_selectors,
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]
    selector_associations_table = built_themes_list["selector_associations_table"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        for theme_name, selector in selector_associations_table.items():
            if selector.lower() == llm_response.lower().strip():
                return theme_name

    system_prompt = (
        "Agis comme un assistant de recherche chargé d'annoter des documents. "
        "Ton rôle est d'attribuer un label sous la forme d'une lettre à une question "
        "posée par un député à l'Assemblée nationale française. "
        "Chaque thème est associé à une lettre de A à U. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse ne doit contenir qu'une seule chose : "
        "la lettre associée au thème correspondant. "
        f"Par exemple `{a_to_z_selectors[0]}` pour `{themes_list[0]}` "
        f"ou `{a_to_z_selectors[1]}` pour `{themes_list[1]}`."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.ZeroShot],
        validation_func,
        retrieve_theme_func,
    )


def zero_shot_cot_vanilla(themes_list: List[str], themes_hierarchy_level: int):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        return retrieve_theme_from_cot_response(llm_response)

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides. "
        "Réfléchis étape par étape."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.ZeroShot, PromptType.ChainOfThought],
        retrieve_theme_func,
    )


def zero_shot_cot_proxy(themes_list: List[str], themes_hierarchy_level: int):
    a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

    def validation_func(response: str):
        a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

        if response.endswith("."):
            response = response.rsplit(".", 1)[0]

        pattern = r"(\w)\."
        predicted_label = re.findall(pattern, response.strip())[-1]

        guard = Guard().use(ValidChoices, choices=a_to_z_selectors, on_fail="exception")
        guard.validate(predicted_label)

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list,
        theme_level=themes_hierarchy_level,
        with_selector=True,
        selectors=a_to_z_selectors,
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]
    selector_associations_table = built_themes_list["selector_associations_table"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        if llm_response.endswith("."):
            llm_response = llm_response.rsplit(".", 1)[0]

        pattern = r"(\w)\."
        predicted_label = re.findall(pattern, llm_response.strip())[-1]

        for theme_name, selector in selector_associations_table.items():
            if selector.lower() == predicted_label.lower():
                return theme_name

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides. "
        "Réfléchis étape par étape."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.ZeroShot],
        validation_func,
        retrieve_theme_func,
    )


def zero_shot_verbalized_confidence_vanilla(
    themes_list: List[str], themes_hierarchy_level: int
):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    def validation_func(response: str):
        regex = re.compile(r"^(Thème:) ([\w| |'|,|-]+)")
        capture = re.search(regex, response)
        guard = Guard().use(ValidChoices, choices=themes_list, on_fail="exception")
        guard.validate(capture.group(2).strip())  # type: ignore
        regex = re.compile(r"(Probabilité:) ([\d|\.]+)")
        capture = re.search(regex, response)
        guard = Guard().use(ValidRange(min=0.0, max=1.0, on_fail="exception"))  # type: ignore
        guard.validate(capture.group(2).strip())  # type: ignore

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )

    def retrieve_theme_func(
        themes_list: List[str], theme_level: int, llm_response: str
    ) -> str:
        regex = re.compile(r"^(Thème:) ([\w| |'|,]+)")
        capture = re.search(regex, llm_response)
        return capture.group(2).strip()  # type: ignore

    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit deux choses :\n"
        "- Le thème correspondant, par exemple `retraites` ou `ministères et secrétariats d'état`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides.\n"
        "- La probabilité que le thème choisi soit adéquat (entre 0.0 et 1.0)\n"
        "Ne fournis que ces deux éléments, aucune autre explication ou mot complémentaire.\n"
        "Par exemple: \n\n"
        "Thème: <le thème le plus adéquat pour annoter la question choisi parmi la liste fournie>\n"
        "Probabilité: <la probabilité comprise entre 0.0 and 1.0>"
    )

    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.ZeroShot, PromptType.ChainOfThought],
        validation_func,
        retrieve_theme_func,
    )


def zero_shot_cot_verbalized_confidence_vanilla(
    themes_list: List[str], themes_hierarchy_level: int
):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    def validation_func(response: str):
        regex = re.compile(r"(Thème:) ([\w| |'|,|-]+)")
        capture = re.search(regex, response)

        guard = Guard().use(ValidChoices, choices=themes_list, on_fail="exception")
        guard.validate(capture.group(2).strip())  # type: ignore

        regex = re.compile(r"(Probabilité:) ([\d|\.]+)")
        capture = re.search(regex, response)

        guard = Guard().use(ValidRange(min=0.0, max=1.0, on_fail="exception"))  # type: ignore
        guard.validate(capture.group(2).strip())  # type: ignore

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )

    def retrieve_theme_func(
        themes_list: List[str], theme_level: int, llm_response: str
    ) -> str:
        regex = re.compile(r"(Thème:) ([\w| |'|,]+)")
        capture = re.search(regex, llm_response)

        return capture.group(2).strip()  # type: ignore

    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit trois choses :\n"
        "- Une explication guidant le choix du thème.\n"
        "- Le thème correspondant, par exemple `retraites` ou `ministères et secrétariats d'état`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides.\n"
        "- La probabilité que le thème choisi soit adéquat (entre 0.0 et 1.0)\n"
        "Réfléchis étape par étape. "
        "Ne fournis que ces trois éléments.\n"
        "Par exemple: \n\n"
        "Explication: <explication guidant le choix du thème>\n"
        "Thème: <le thème le plus adéquat pour annoter la question choisi parmi la liste fournie>\n"
        "Probabilité: <la probabilité comprise entre 0.0 and 1.0>"
    )

    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.ZeroShot, PromptType.ChainOfThought],
        validation_func,
        retrieve_theme_func,
    )


"""
ONE-SHOT PROMPT BUILDERS
"""


def one_shot_vanilla(
    themes_list: List[str], themes_hierarchy_level: int, wrapper: WrapperEnum
):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit contenir une seule chose: le thème correspondant, "
        f"par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides."
    )

    intermediate_prompts = build_random_few_shot_prompt(
        1,
        wrapper,
        as_context=True,
        stop_at_level=themes_hierarchy_level,
        accepted_themes=accepted_themes_for_questions,
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.OneShot])


def one_shot_proxy(
    themes_list: List[str],
    themes_hierarchy_level: int,
    wrapper: WrapperEnum,
):
    a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

    def validation_func(response: str):
        a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]
        guard = Guard().use(ValidChoices, choices=a_to_z_selectors, on_fail="exception")
        guard.validate(response)

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list,
        theme_level=themes_hierarchy_level,
        with_selector=True,
        selectors=a_to_z_selectors,
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]
    selector_associations_table = built_themes_list["selector_associations_table"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        for theme_name, selector in selector_associations_table.items():
            if selector.lower() == llm_response.lower().strip():
                return theme_name

    system_prompt = (
        "Agis comme un assistant de recherche chargé d'annoter des documents. "
        "Ton rôle est d'attribuer un label sous la forme d'une lettre à une question "
        "posée par un député à l'Assemblée nationale française. "
        "Chaque thème est associé à une lettre de A à U. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse ne doit contenir qu'une seule chose : "
        "la lettre associée au thème correspondant. "
        f"Par exemple `{a_to_z_selectors[0]}` pour `{themes_list[0]}` "
        f"ou `{a_to_z_selectors[1]}` pour `{themes_list[1]}`."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    intermediate_prompts = build_random_few_shot_prompt(
        1,
        wrapper,
        as_context=True,
        accepted_themes=accepted_themes_for_questions,
        stop_at_level=themes_hierarchy_level,
        selector_associations_table=selector_associations_table,
    )

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.FewShot],
        validation_func,
        retrieve_theme_func,
    )


"""
FEW-SHOT PROMPT BUILDERS
"""


def few_shot_vanilla(
    themes_list: List[str],
    themes_hierarchy_level: int,
    wrapper: WrapperEnum,
    number_of_shots: int = 3,
):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse doit contenir une seule chose: le thème correspondant, "
        f"par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides."
    )

    intermediate_prompts = build_random_few_shot_prompt(
        number_of_shots,
        wrapper,
        as_context=True,
        accepted_themes=accepted_themes_for_questions,
        stop_at_level=themes_hierarchy_level,
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (prompts, {}, accepted_themes_for_questions, [PromptType.FewShot])


def few_shot_proxy(
    themes_list: List[str],
    themes_hierarchy_level: int,
    wrapper: WrapperEnum,
    number_of_shots: int = 3,
):
    a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

    def validation_func(response: str):
        a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]
        guard = Guard().use(ValidChoices, choices=a_to_z_selectors, on_fail="exception")
        guard.validate(response)

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list,
        theme_level=themes_hierarchy_level,
        with_selector=True,
        selectors=a_to_z_selectors,
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]
    selector_associations_table = built_themes_list["selector_associations_table"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        for theme_name, selector in selector_associations_table.items():
            if selector.lower() == llm_response.lower().strip():
                return theme_name

    system_prompt = (
        "Agis comme un assistant de recherche chargé d'annoter des documents. "
        "Ton rôle est d'attribuer un label sous la forme d'une lettre à une question "
        "posée par un député à l'Assemblée nationale française. "
        "Chaque thème est associé à une lettre de A à U. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Ta réponse ne doit contenir qu'une seule chose : "
        "la lettre associée au thème correspondant. "
        f"Par exemple `{a_to_z_selectors[0]}` pour `{themes_list[0]}` "
        f"ou `{a_to_z_selectors[1]}` pour `{themes_list[1]}`."
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    intermediate_prompts = build_random_few_shot_prompt(
        number_of_shots,
        wrapper,
        as_context=True,
        accepted_themes=accepted_themes_for_questions,
        stop_at_level=themes_hierarchy_level,
        selector_associations_table=selector_associations_table,
    )

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.FewShot],
        validation_func,
        retrieve_theme_func,
    )


def few_shot_cot_vanilla(
    themes_list: List[str],
    themes_hierarchy_level: int,
    wrapper: WrapperEnum,
    number_of_shots: int = 3,
):
    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list, theme_level=themes_hierarchy_level
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        return retrieve_theme_from_cot_response(llm_response)

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides. "
        "Réfléchis étape par étape. Voici un exemple de réflexion :\n"
    )

    intermediate_prompts = build_random_few_shot_prompt(
        number_of_shots,
        wrapper,
        cot=True,
        as_context=True,
        accepted_themes=accepted_themes_for_questions,
        stop_at_level=themes_hierarchy_level,
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.FewShot, PromptType.ChainOfThought],
        retrieve_theme_func,
    )


def few_shot_cot_proxy(
    themes_list: List[str],
    themes_hierarchy_level: int,
    wrapper: WrapperEnum,
    number_of_shots: int = 3,
):
    a_to_z_selectors = [chr(i) for i in range(ord("A"), ord("["))]

    def validation_func(response: str):
        predicted_label = retrieve_theme_from_cot_response(response)

        guard = Guard().use(ValidChoices, choices=a_to_z_selectors, on_fail="exception")
        guard.validate(predicted_label.upper())

    built_themes_list = build_prompt_themes_list(
        themes_list=themes_list,
        theme_level=themes_hierarchy_level,
        with_selector=True,
        selectors=a_to_z_selectors,
    )
    themes_list_as_string = built_themes_list["themes_list_as_string"]
    accepted_themes_for_questions = built_themes_list["accepted_themes_for_questions"]
    selector_associations_table = built_themes_list["selector_associations_table"]

    def retrieve_theme_func(
        themes_list: List[str],
        theme_level: int,
        llm_response: str,
    ):
        theme = retrieve_theme_from_cot_response(llm_response)
        for theme_name, selector in selector_associations_table.items():
            if selector.lower() == theme.lower().strip():
                return theme_name

    system_prompt = (
        "Ton rôle est d'attribuer un thème à une question posée par un député "
        "à l'Assemblée nationale française. La liste des thèmes est la suivante :"
        f"{themes_list_as_string}\n"
        "Le thème assigné doit être un des thèmes de la liste fournie. "
        "Seuls les thèmes de la liste précédente sont valides. "
        "Réfléchis étape par étape. Voici un exemple de réflexion :\n"
    )

    intermediate_prompts = build_random_few_shot_prompt(
        number_of_shots,
        wrapper,
        cot=True,
        as_context=True,
        accepted_themes=accepted_themes_for_questions,
        stop_at_level=themes_hierarchy_level,
        selector_associations_table=selector_associations_table,
    )

    # '{0}' will be replaced by the text of the question when the prompt will loop over the questions
    user_prompt = "{0}"

    prompts = [
        PromptText(role=RoleEnum.System.value, content=system_prompt),
        *intermediate_prompts,
        PromptText(role=RoleEnum.User.value, content=user_prompt),
    ]

    print_prompts(prompts)

    return (
        prompts,
        {},
        accepted_themes_for_questions,
        [PromptType.FewShot, PromptType.ChainOfThought],
        validation_func,
        retrieve_theme_func,
    )
