import json
import random
import time
import pandas as pd
from typing import List, TypedDict, Dict, Optional, Set
from tqdm import tqdm
from errors.ThemesListTooLongException import ThemesListTooLongException
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from models.Prompt import WrapperEnum
from models.Prompt import (
    Prompt,
    PromptRun,
    PromptLanguage,
    CotExplanation,
    PromptRunInfo,
    PromptText,
    RoleEnum,
    PromptResult,
)
from models.Question import Question
from prompting.run_prompt import run_prompt
from utils.helpers import hash_list
from utils.helpers import find_src_directory

connector = Connector(ExportFormat.JSON)


class PromptThemesListAndLegalOriginalLabels(TypedDict):
    """
    The formated list of theme labels designed for the LLM prompt
    associated with the legal original labels as existing in the database.
    """

    themes_list_as_string: str
    accepted_themes_for_questions: List[str]
    selector_associations_table: Optional[Dict[str, str]]


def self_calibration_prompt(
    prompt_info: PromptRunInfo, lang: PromptLanguage, sleep_time: int = 0
) -> PromptRunInfo:
    """
    Run a self-calibration process on a set of prompt results, allowing the LLM to validate the proposed theme labels.

    Parameters
    ----------
    prompt_info : PromptRunInfo
        Information about the prompt run, including run ID and metadata.
    lang : PromptLanguage
        The language to be used in the self-calibration prompt (e.g., 'en' or 'fr').
    sleep_time : float, default=0
        Time to wait (in seconds) between sending each prompt, to control rate limits.

    Returns
    -------
    PromptRunInfo
        Updated prompt run information after performing self-calibration, containing the results of validation.
    """
    results = connector.client.get_prompt_results({"run_id": prompt_info.run_id})
    results = [PromptResult(**result) for result in list(results)]
    question_ids = [result.question_id for result in results]
    questions = connector.client.get_questions({"id": {"$in": question_ids}})
    questions = [Question(**question) for question in questions]

    questions_results = {}
    for q in questions:
        for r in results:
            if r.question_id == q.id:
                questions_results[q.id] = (q, r)

    prompts_lang = {
        "fr": {
            "prompt": (
                "Est-ce que le thème proposé est adéquat ? (Répond uniquement avec `Oui` ou `Non`)"
            ),
            "valid_choices": ["Oui", "Non", "oui", "non"],
            "format_token": "Réponse: #!result",
        },
        "en": {
            "prompt": (
                "Is the proposed answer:" "\nTrue" "\nFalse" "\nThe proposed answer is:"
            ),
            "valid_choices": ["True", "False", "true", "false"],
            "format_token": "Response: #!result",
        },
    }

    if prompt_info.prompt_run.parameters.wrapper == WrapperEnum.Google:
        prompt_info.prompts += [
            PromptText(
                role=RoleEnum.Model, content=prompts_lang[lang.value]["format_token"]
            ),
            PromptText(role=RoleEnum.User, content=prompts_lang[lang.value]["prompt"]),
        ]
    else:
        prompt_info.prompts += [
            PromptText(
                role=RoleEnum.Assistant,
                content=prompts_lang[lang.value]["format_token"],
            ),
            PromptText(role=RoleEnum.User, content=prompts_lang[lang.value]["prompt"]),
        ]

    prompt = Prompt(
        unique_identifier=hash_list(
            [prompt.model_dump() for prompt in prompt_info.prompts]
        ),
        prompts=prompt_info.prompts,
    )
    prompt = connector.client.upsert_prompt(prompt)

    prompt_run = PromptRun(
        prompt_id=prompt.unique_identifier,
        batch_id=prompt_info.prompt_run.batch_id,
        parameters=prompt_info.prompt_run.parameters,
        timestamp=int(time.time()),
        comment=f"Self-Calibration run for run_id : {prompt_info.run_id}.",
        name=f"Self-Calibration #{prompt_info.run_id}",
        themes_list=prompts_lang[lang.value]["valid_choices"],
    )
    inserted_prompt_run = connector.client.add_prompt_run(prompt_run)

    print("Running calibration prompts...")
    for question, result in tqdm(questions_results.values()):
        association_format_list = {"#!result": result.final_answer}
        time.sleep(sleep_time)
        run_prompt(
            question=question,
            assoc=association_format_list,
            prompt=prompt,
            prompt_run=prompt_run,
            prompt_run_id=str(inserted_prompt_run.inserted_id),
        )

    return PromptRunInfo(
        run_id=str(inserted_prompt_run.inserted_id),
        prompts=prompt.prompts,
        prompt_run=prompt_run,
    )


def build_random_few_shot_prompt(
    k: int,
    llm_wrapper: WrapperEnum,
    as_context: bool = False,
    cot: bool = False,
    stratified: bool = True,
    legislature: Optional[int] = None,
    stop_at_level: int = 3,
    accepted_themes: Optional[List[str]] = None,
    json_format: bool = False,
    selector_associations_table: Optional[Dict[str, str]] = None,
) -> str | List[PromptText]:
    """
    Either sample random questions or sample random questions and explanations from the
    database or the JSON explanations file. Those pieces of data are then used to
    build the few-shot prompts.

    Parameters
    ----------
    k: int
        The number of shots to build the few-shot template.
    llm_wrapper: WrapperEnum
        A wrapper defining the type of LLM used.
    as_context: bool, default=False
        Defines if the few-shot examples should be outputed as plain string
        or as LLM context objects.
    cot: bool, default=False
        Defines if chain-of-thought should be used.
    stratified: bool, default=True
        Controls if the examples sampled can have duplicates.
    legislature: int | None, default=None
        Sample the questions from a given 'legislature'.
    stop_at_level: int, default=3
        Defines the top level from which to retrieve the parent theme.
    json_format: bool, default=False
        Defines if the prompt should be formated as JSON.
    selector_associations_table: Dict[str, str], default=None
        Dictionany describing the association between a label and a proxy identifier. Used with proxy prompts.

    Returns
    -------
    str
        The few-shot prompt template.
    """
    if stratified:
        if accepted_themes is None:
            raise ValueError(
                "When using stratified sampling, the accepted theme "
                "list should also be provided."
            )

        if cot:
            stratified_examples = get_few_shot_cot_stratified_examples(
                k=k,
                legislature=legislature,
                accepted_themes=accepted_themes,
                stop_at_level=stop_at_level,
            )
        else:
            stratified_examples = get_few_shot_stratified_examples(
                k=k,
                legislature=legislature,
                accepted_themes=accepted_themes,
                stop_at_level=stop_at_level,
            )

        if as_context:
            return _build_few_shot_prompt_as_context(
                stratified_examples,
                llm_wrapper,
                stop_at_level,
                json_format,
                selector_associations_table,
            )
        else:
            return _build_few_shot_prompt_as_string(
                stratified_examples,
                stop_at_level,
                json_format,
                selector_associations_table,
            )
    else:
        if cot:
            with open(f"{find_src_directory()}/data/explanations.json", "r") as file:
                json_file = file.read()
                questions = json.loads(json_file)
                questions = [
                    CotExplanation(**question)
                    for question in random.sample(questions, k)
                ]
        else:
            questions = connector.client.get_random_questions(
                number_of_questions=k,
                legislature=legislature,
                accepted_themes=accepted_themes,
            )
            questions = [Question(**question) for question in questions]

        if as_context:
            return _build_few_shot_prompt_as_context(
                questions,
                llm_wrapper,
                stop_at_level,
                json_format,
                selector_associations_table,
            )
        else:
            return _build_few_shot_prompt_as_string(
                questions, stop_at_level, json_format, selector_associations_table
            )


def _build_child_to_parent_theme_mapping(
    accepted_themes: List[str],
    stop_at_level: int,
) -> Dict[str, Set[str]]:
    parent_to_child_theme = {}
    for theme in accepted_themes:
        parent_theme = connector.client.get_parent_theme_from_child_theme_name(
            theme,
            stop_at_level=stop_at_level,
        )
        try:
            parent_to_child_theme[parent_theme.name].add(theme)
        except KeyError:
            parent_to_child_theme[parent_theme.name] = set()
            parent_to_child_theme[parent_theme.name].add(theme)

    return parent_to_child_theme


def get_few_shot_cot_stratified_examples(
    k: int,
    legislature: int | None,
    accepted_themes: List[str],
    stop_at_level: int,
) -> List[Question]:
    """
    Get stratified question examples for few-shot chain-of-thought settings.

    Parameters
    ----------
    k: int
        Number of question examples.
    legislature: int | None
        The legislature number.
    accepted_themes: List[str]
        List of themes from which to sample questions from.
    stop_at_level: int
        Defines the level from which to start looking from the child theme.

    Returns
    -------
    List[Question]
        The list of questions sampled.
    """
    sampled_questions = []
    parent_to_child_theme = _build_child_to_parent_theme_mapping(
        accepted_themes, stop_at_level
    )
    with open(f"{find_src_directory()}/data/explanations.json", "r") as json_file:
        content = json_file.read()
        explanations = json.loads(content)
        explanations_df = pd.DataFrame(explanations)

    for _ in range(k):
        try:
            theme = random.choice(list(parent_to_child_theme.keys()))
        except IndexError:
            raise ValueError(
                "The number of shots is higher than the number of available parent themes."
            )
        if legislature:
            sampled_question = explanations_df[
                (explanations_df["legislature"] == legislature)
                & (explanations_df["label"] == theme)
            ]
        else:
            sampled_question = (
                explanations_df[explanations_df["label"] == theme]
                .sample()
                .iloc[0]
                .to_dict()
            )
        sampled_questions.append(CotExplanation(**sampled_question))
        del parent_to_child_theme[theme]

    return sampled_questions


def get_few_shot_stratified_examples(
    k: int,
    legislature: int | None,
    accepted_themes: List[str],
    stop_at_level: int,
) -> List[Question]:
    """
    Get stratified question examples for few-shot settings.

    Parameters
    ----------
    k: int
        Number of question examples.
    legislature: int | None
        The legislature number.
    accepted_themes: List[str]
        List of themes from which to sample questions from.
    stop_at_level: int
        Defines the level from which to start looking from the child theme.

    Returns
    -------
    List[Question]
        The list of questions sampled.
    """
    sampled_questions = []
    parent_to_child_theme = _build_child_to_parent_theme_mapping(
        accepted_themes, stop_at_level
    )

    for _ in range(k):
        try:
            theme = random.choice(list(parent_to_child_theme.keys()))
        except IndexError:
            raise ValueError(
                "The number of shots is higher than the number of available parent themes."
            )
        if legislature is None:
            question = connector.client.get_question(
                {"theme": {"$in": list(parent_to_child_theme[theme])}}
            )
        else:
            question = connector.client.get_question(
                {
                    "legislature": {"$in": legislature},
                    "theme": {"$in": list(parent_to_child_theme[theme])},
                }
            )
        sampled_questions.append(Question(**question))
        del parent_to_child_theme[theme]

    return sampled_questions


def _build_llm_context_as_json(
    question: CotExplanation | Question,
    stop_at_level: int,
    llm_wrapper: WrapperEnum,
    selector_associations_table: Optional[Dict[str, str]] = None,
) -> List[PromptText]:
    """
    Build the LLM context as a JSON representation from a given question.

    Parameters
    ----------
    question : CotExplanation | Question
        The question object or a chain-of-thought (CoT) explanation containing the question text, explanation, and label.
    stop_at_level : int
        The level at which to stop retrieving parent themes.
    llm_wrapper : WrapperEnum
        The wrapper used for formatting the LLM response.
    selector_associations_table: Dict[str, str], default=None
        Dictionany describing the association between a label and a proxy identifier. Used with proxy prompts.

    Returns
    -------
    List[PromptText]
        A list of prompt texts representing the LLM context in JSON format.
    """

    llm_context = []
    if type(question) is CotExplanation:
        user_input = f"{question.question_text}"
        user_question = PromptText(role=RoleEnum.User, content=str(user_input))
        llm_context.append(user_question)
        if selector_associations_table is not None:
            llm_answer = {
                "explanation": question.explanation,
                "label": selector_associations_table[question.label],
            }
        else:
            llm_answer = {"explanation": question.explanation, "label": question.label}

        if llm_wrapper == WrapperEnum.Google:
            llm_answer = PromptText(role=RoleEnum.Model, content=str(llm_answer))
        else:
            llm_answer = PromptText(role=RoleEnum.Assistant, content=str(llm_answer))
        llm_context.append(llm_answer)
    else:
        user_input = f"\n\nQuestion: {question.question_text}"
        user_question = PromptText(role=RoleEnum.User, content=str(user_input))
        llm_context.append(user_question)
        parent_theme = connector.client.get_parent_theme_from_child_theme_name(
            question.theme,  # type: ignore
            stop_at_level=stop_at_level,
            base_theme_level=0,
        )
        if selector_associations_table is not None:
            llm_answer = {"label": selector_associations_table[parent_theme.name]}
        else:
            llm_answer = {"label": parent_theme.name}

        if llm_wrapper == WrapperEnum.Google:
            llm_answer = PromptText(role=RoleEnum.Model, content=str(llm_answer))
        else:
            llm_answer = PromptText(role=RoleEnum.Assistant, content=str(llm_answer))
        llm_context.append(llm_answer)

    return llm_context


def _build_llm_context_as_string(
    question: CotExplanation | Question,
    stop_at_level: int,
    llm_wrapper: WrapperEnum,
    selector_associations_table: Optional[Dict[str, str]] = None,
) -> List[PromptText]:
    """
    Build the LLM context as a string representation from a given question.

    Parameters
    ----------
    question : CotExplanation | Question
        The question object or a chain-of-thought (CoT) explanation containing the question text, explanation, and label.
    stop_at_level : int
        The level at which to stop retrieving parent themes.
    llm_wrapper : WrapperEnum
        The wrapper used for formatting the LLM response.
    selector_associations_table: Dict[str, str], default=None
        Dictionany describing the association between a label and a proxy identifier. Used with proxy prompts.

    Returns
    -------
    List[PromptText]
        A list of prompt texts representing the LLM context in string format.
    """
    llm_context = []
    if type(question) is CotExplanation:
        user_text = f"\n{question.question_text}"
        user_question = PromptText(role=RoleEnum.User, content=user_text)
        llm_context.append(user_question)
        llm_text = f"\n{question.explanation}"
        if selector_associations_table is not None:
            llm_text += f"\n\nLabel: {selector_associations_table[question.label]}"
        else:
            llm_text += f"\n\nLabel: {question.label}"
        if llm_wrapper == WrapperEnum.Google:
            llm_answer = PromptText(role=RoleEnum.Model, content=llm_text)
        else:
            llm_answer = PromptText(role=RoleEnum.Assistant, content=llm_text)
        llm_context.append(llm_answer)
    else:
        user_text = f"\n{question.question_text}"
        user_question = PromptText(role=RoleEnum.User, content=user_text)
        llm_context.append(user_question)
        parent_theme = connector.client.get_parent_theme_from_child_theme_name(
            question.theme,  # type: ignore
            stop_at_level=stop_at_level,
            base_theme_level=0,
        )
        if selector_associations_table is not None:
            llm_text = f"\n{selector_associations_table[parent_theme.name]}"
        else:
            llm_text = f"\n{parent_theme.name}"
        if llm_wrapper == WrapperEnum.Google:
            llm_answer = PromptText(role=RoleEnum.Model, content=llm_text)
        else:
            llm_answer = PromptText(role=RoleEnum.Assistant, content=llm_text)
        llm_context.append(llm_answer)

    return llm_context


def _build_few_shot_prompt_as_context(
    questions: List[CotExplanation] | List[Question],
    llm_wrapper: WrapperEnum,
    stop_at_level: int,
    json_format: bool = False,
    selector_associations_table: Optional[Dict[str, str]] = None,
) -> List[PromptText]:
    """
    Build the few-shot prompt as context, including examples and the question.

    Parameters
    ----------
    examples : List[Dict]
        A list of example dictionaries, where each dictionary contains an example question, explanation, and label.
    question : Question
        The question for which the prompt is being constructed.
    llm_wrapper : WrapperEnum
        The wrapper used for formatting the LLM response.
    selector_associations_table: Dict[str, str], default=None
        Dictionany describing the association between a label and a proxy identifier. Used with proxy prompts.

    Returns
    -------
    List[PromptText]
        A list of prompt texts representing the few-shot context.
    """
    llm_context = []
    if json_format:
        for question in questions:
            llm_context += _build_llm_context_as_json(
                question, stop_at_level, llm_wrapper, selector_associations_table
            )
    else:
        for question in questions:
            llm_context += _build_llm_context_as_string(
                question, stop_at_level, llm_wrapper, selector_associations_table
            )

    return llm_context


def _build_few_shot_prompt_as_string(
    questions: List[CotExplanation] | List[Question],
    stop_at_level: int,
    json_format: bool = False,
    selector_associations_table: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build the few-shot prompt template as plain string.

    Parameters
    ----------
    questions: List[CotExplanations] | List[Question]
        Questions used as few-shot examples.
    stop_at_level: int, default=3
        Defines the top level from which to retrieve the parent theme.
    json_format: bool, default=False
        Defines if the prompt should be formated as JSON.
    selector_associations_table: Dict[str, str], default=None
        Dictionany describing the association between a label and a proxy identifier. Used with proxy prompts.

    Returns
    -------
    str
        The prompt content.
    """
    template = ""

    if json_format:
        for question in questions:
            json_template = {}
            if type(question) is CotExplanation:
                json_template["question"] = question.question_text
                json_template["explanation"] = question.explanation
                if selector_associations_table is not None:
                    json_template["label"] = selector_associations_table[question.label]
                else:
                    json_template["label"] = question.label
            else:
                parent_theme = connector.client.get_parent_theme_from_child_theme_name(
                    question.theme,  # type: ignore
                    stop_at_level=stop_at_level,
                    base_theme_level=0,
                )
                json_template["question"] = question.question_text
                if selector_associations_table is not None:
                    json_template["label"] = selector_associations_table[
                        parent_theme.name
                    ]
                else:
                    json_template["label"] = parent_theme.name
            template += str(json_template)
    else:
        for question in questions:
            template += f"\nQuestion: {question.question_text}"
            if type(question) is CotExplanation:
                template += f"\n\nExplication: {question.explanation}"
                if selector_associations_table is not None:
                    template += (
                        f"\n\nLabel: {selector_associations_table[question.label]}"
                    )
                else:
                    template += f"\n\nLabel: {question.label}"
            else:
                parent_theme = connector.client.get_parent_theme_from_child_theme_name(
                    question.theme,  # type: ignore
                    stop_at_level=stop_at_level,
                    base_theme_level=0,
                )
                if selector_associations_table is not None:
                    template += (
                        f"\n\nLabel: {selector_associations_table[parent_theme.name]}"
                    )
                else:
                    template += f"\n\nLabel: {parent_theme.name}"

    return template


def build_prompt_themes_list(
    themes_list: List[str],
    theme_level: int,
    with_selector: bool = False,
    selectors: List[str] = [],
) -> PromptThemesListAndLegalOriginalLabels:
    """
    Build a custom list of theme labels formated for the LLM prompt.

    Parameters
    ----------
    theme_list: List[str]
        A list of themes.
    theme_level: int
        The aggregation level where to stop in the database.
    with_selector: bool, default=False
        Defines if the prompt should associate the theme label with a proxy
        selector (A letter between 'A' and 'Z').

    Returns
    -------
    PromptThemesListAndLegalOriginalLabels
        The formated list of theme labels designed for the LLM prompt
        associated with the legal original labels as existing in the database.

    Raises
    ------
    ThemesListTooLongException
        If the themes list provided is too long to be associated with one
        letter proxy selector.
    """
    if with_selector and len(themes_list) > (len(selectors)):
        raise ThemesListTooLongException

    theme_documents = connector.client.get_themes(
        {"level": theme_level, "name": {"$in": themes_list}}
    )

    theme_documents = list(theme_documents)
    themes = []

    accepted_themes_for_questions = []

    for theme in theme_documents:
        themes.append(theme)
        sub_themes = connector.client.get_sub_themes_list_from_theme(
            theme["unique_identifier"], flatten=True
        )
        for sub_theme in sub_themes:
            if sub_theme["name"] not in accepted_themes_for_questions:
                accepted_themes_for_questions.append(sub_theme["name"])

    themes_string = ""

    selector_associations_table = {}
    if with_selector:
        for i, theme in enumerate(themes_list):
            selector_associations_table[theme] = selectors[i]
            themes_string += f"\n- {selectors[i]}. {theme}"

        return PromptThemesListAndLegalOriginalLabels(
            themes_list_as_string=themes_string,
            accepted_themes_for_questions=accepted_themes_for_questions,
            selector_associations_table=selector_associations_table,
        )
    else:
        for i, theme in enumerate(themes_list):
            themes_string += f"\n- {theme}"

        return PromptThemesListAndLegalOriginalLabels(
            themes_list_as_string=themes_string,
            accepted_themes_for_questions=accepted_themes_for_questions,
        )
