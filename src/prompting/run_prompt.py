import time
import traceback
from tqdm import tqdm
from bson import ObjectId
from models.Batch import Batch
from pydantic import BaseModel
from prompting.llm_wrappers import (
    prompt_openai,
    prompt_anthropic,
    prompt_google,
    prompt_mistral,
)
from bson.errors import InvalidId
from prompting.prompt_mask import question_processing
from utils.logger import get_logger
from utils.helpers import hash_list
from models.Prompt import WrapperEnum
from databases.connector import Connector
from typing import Callable, List, Optional, Tuple, Dict
from models.ExportFormat import ExportFormat
from guardrails import Guard
from guardrails.hub import ValidChoices
from models.Prompt import (
    Prompt,
    PromptResult,
    PromptRun,
    PromptRunInfo,
    PromptRunParameters,
    PromptText,
)
from models.Question import Question

logger = get_logger()
connector = Connector(ExportFormat.JSON)


def _build_question_list(
    batch_id: str | None, number_of_questions: int, accepted_themes: List[str] | None
) -> Tuple[str, List[Question]]:
    if batch_id is None:
        questions = connector.client.get_random_questions(
            number_of_questions=number_of_questions,
            accepted_themes=accepted_themes,
        )
        question_list = [Question(**question) for question in list(questions)]
        batch = Batch(
            question_ids=[x.id for x in question_list],
            size=number_of_questions,
        )

        batch_id = str(connector.client.add_batch(batch).inserted_id)
    else:
        error_msg = f"Batch with ID {batch_id} does not exist in the database."
        try:
            batch = connector.client.get_batch({"_id": ObjectId(batch_id)})
            if batch is None:
                logger.error(error_msg)
                raise IndexError(error_msg)
        except InvalidId:
            logger.error(f"Batch with ID {batch_id} does not exist in the database.")
            raise IndexError(error_msg)

        question_list = connector.client.aggregate_questions(
            [{"$match": {"id": {"$in": batch["question_ids"]}}}]
        )
        question_list = [Question(**question) for question in list(question_list)]

    return batch_id, question_list


def run_prompt(
    question: Question,
    prompt: Prompt,
    prompt_run_id: str,
    prompt_run: PromptRun,
    assoc: Dict[str, str] | None = None,
    response_format: Optional[BaseModel] = None,
    retrieve_theme_func: Callable[..., str] | None = None,
    validation_func: Callable | None = None,
    ministry_mask: bool = False,
    dry_run: bool = False,
) -> None:
    """
    Run an LLM prompt for a single question.

    Parameters
    ----------
    question: Question
        The question and its associated metadata.
    prompt: Prompt
        The input prompt provided to the LLM.
    prompt_run_id: str
        A unique identifier to identify the prompt run.
    prompt_run: PromptRun
        All the parameters defining the prompt run.
    assoc: Dict[str, str] | None, default=None
        An association table to replace previous LLM prompt answers
        in specific configurations that requires to rerun prompt
        against previous LLM answers.
    response_format: Callable[..., str] | None, default=None
        A function provided to format the output the desired way.
    retrieve_theme_func: Callable[..., str] | None = None
        A function used to retrieve the original corresponding theme
        in the database.
    validation_func: Callable | None, default=None
        A custom validation function in order to reject LLM answers
        that do not follow the provided guardrails.
    ministry_mask: bool, default=False
        If True, remove the ministry names in the question phrasing.
    dry_run: bool, default=False
        Controls if the LLM results should be written in the database
        or not.
    """

    logger.info(f"Question #{question.id}")
    question_text = question.question_text

    if ministry_mask:
        question_text = question_processing(question_text)

    start_time = time.perf_counter()

    try:
        match prompt_run.parameters.wrapper:
            case WrapperEnum.OpenAI:
                response = prompt_openai(
                    prompt,
                    prompt_run,
                    question_text,
                    assoc,
                    response_format,
                    retrieve_theme_func,
                )
            case WrapperEnum.Anthropic:
                response = prompt_anthropic(
                    prompt,
                    prompt_run,
                    question_text,
                    assoc,
                    retrieve_theme_func,
                )
            case WrapperEnum.Mistral:
                response = prompt_mistral(
                    prompt,
                    prompt_run,
                    question_text,
                    assoc,
                    retrieve_theme_func,
                )
            case WrapperEnum.Google:
                response = prompt_google(
                    prompt,
                    prompt_run,
                    question_text,
                    assoc,
                    retrieve_theme_func,
                )
            case _:
                raise TypeError(
                    f"The provided wrapper {prompt_run.parameters.wrapper} does not exists."
                )

        elapsed_time = time.perf_counter() - start_time
        logger.info(f"Time taken for API call: {elapsed_time:.4f} seconds")

        prompt_tokens = response.prompt_tokens  # type: ignore
        logger.info(f"Total prompt tokens : {prompt_tokens}")
        logger.info(f"API response : {response.raw_response}")  # type: ignore

        start_time = time.perf_counter()

        response_message = response.raw_response  # type: ignore
        response_theme = response.predicted_label

        elapsed_time = time.perf_counter() - start_time
        logger.info(f"Time taken to retrieve theme: {elapsed_time:.4f} seconds")

        start_time = time.perf_counter()

        question_theme = connector.client.get_theme(
            {"name": question.theme, "level": 0}
        )
        top_level_theme = connector.client.get_parent_theme(
            question_theme.parent_theme_identifier,  # type: ignore
            stop_at_level=prompt_run.parameters.theme_hierarchy_level,
        )

        elapsed_time = time.perf_counter() - start_time
        logger.info(f"Time taken to retrieve theme from db: {elapsed_time:.4f} seconds")

        if top_level_theme is None:
            error_msg = "An error occurred with the theme mapping."
            logger.error(error_msg)
        else:
            logger.info(f"Predicted theme : {response_theme}")
            logger.info(f"Gold label theme : {top_level_theme.name}")

            # ? edit batch to replace questions that are not valid (encoding, empty, etc.)

            start_time = time.perf_counter()

            if validation_func is not None:
                validation_func(response_message)
            else:
                guard = Guard().use(
                    ValidChoices, choices=prompt_run.themes_list, on_fail="exception"
                )
                guard.validate(response_theme)

            elapsed_time = time.perf_counter() - start_time
            logger.info(
                f"Time taken to validate the output: {elapsed_time:.4f} seconds"
            )

            legislature = question.id[: question.id.index("-")]

            start_time = time.perf_counter()

            prompt_result = PromptResult(
                run_id=prompt_run_id,
                question_id=question.id,
                batch_id=prompt_run.batch_id,
                prompt_id=prompt.unique_identifier,
                response=response.raw_response,  # type: ignore
                final_answer=response_theme.lower().strip(),
                response_tokens=response.response_tokens,  # type: ignore
                prompt_tokens=prompt_tokens,
                legislature=int(legislature),
                logprobs=response.logprobs,  # type: ignore
                question_theme=question_theme.name,  # type: ignore
                gold_label=top_level_theme.name,
            )

            if dry_run:
                print(str(prompt_result) + "\n-------------------------")
            else:
                connector.client.add_prompt_result(prompt_result)

            elapsed_time = time.perf_counter() - start_time
            logger.info(f"Time taken save the result to db: {elapsed_time:.4f} seconds")

    except Exception as _:
        logger.error(traceback.format_exc())
        pass

    logger.info("-----------------------")


def run_prompts(
    parameters: PromptRunParameters,
    prompts: List[PromptText],
    themes_list: List[str],
    description: str,
    name: str,
    accepted_themes_for_questions: List[str] | None = None,
    batch_id: str | None = None,
    number_of_questions: int = 1500,
    retrieve_theme_func: Callable[..., str] | None = None,
    response_format: Optional[BaseModel] = None,
    sleep_time: float = 0.0,
    validation_func: Callable | None = None,
    ministry_mask: bool = False,
    dry_run: bool = False,
) -> PromptRunInfo:
    """
    Run an LLM prompt for a batch of questions.

    Parameters
    ----------
    parameters: PromptRunParameters
        The parameters defining the prompt run on the entire question batch.
    prompts: List[PromptText]
        The list of previous context provided as a base for the prompt.
    themes_list: List[str]
        The list of themes that define the label space.
    description: str
        A custom description for the prompt run.
    name: str
        Name of the prompt run.
    accepted_themes_for_questions: List[str] | None, default=None
        List of themes from which questions can be sampled if no batch is provided.
    batch_id: str | None, default=None
        The list of question IDs used for the prompt run. If set to None, sample random
        questions in the database.
    number_of_questions: int, default=1500
        Defines the size of the question batch to sample if no batch_id is provided.
    retrieve_theme_func: Callable[..., str] | None = None
        A function used to retrieve the original corresponding theme
        in the database.
    response_format: Optional[BaseModel], default=None
        A custom schema used to validate the LLM output.
    sleep_time: float, default=0.0
        A sleep time between each prompt query sent to the LLM.
    validation_func: Callable | None = None
        A custom validation function in order to reject LLM answers
        that do not follow the provided guardrails.
    ministry_mask: bool, default=False
        If True, remove the ministry names in the question phrasing.
    dry_run: bool, default=False
        Controls if the LLM results should be written in the database
        or not.

    Returns
    -------
    PromptRunInfo
        A set of metadata providing high-level informations on the prompt run.
    """
    batch_id, question_list = _build_question_list(
        batch_id, number_of_questions, accepted_themes_for_questions
    )

    logger.info(
        f"model is {parameters.model} ;" f" temperature is {parameters.temperature}"
    )
    for prompt in prompts:
        logger.info(f"{prompt.role} prompt : {prompt.content}")

    prompt = Prompt(
        unique_identifier=hash_list([prompt.model_dump() for prompt in prompts]),
        prompts=prompts,
    )
    if not dry_run:
        prompt = connector.client.upsert_prompt(prompt)

        prompt_run = PromptRun(
            prompt_id=prompt.unique_identifier,
            batch_id=batch_id,
            parameters=parameters,
            timestamp=int(time.time()),
            description=description,
            name=name,
            themes_list=themes_list,
            ministry_mask=ministry_mask
        )
        inserted_prompt_run = connector.client.add_prompt_run(prompt_run)

        logger.info(
            f"Running #{inserted_prompt_run.inserted_id} with batch #{batch_id}"
        )

        for question in tqdm(question_list):
            time.sleep(sleep_time)
            run_prompt(
                question=question,
                prompt=prompt,
                prompt_run=prompt_run,
                prompt_run_id=str(inserted_prompt_run.inserted_id),
                response_format=response_format,
                retrieve_theme_func=retrieve_theme_func,
                validation_func=validation_func,
                dry_run=dry_run,
            )

        return PromptRunInfo(
            run_id=str(inserted_prompt_run.inserted_id),
            prompts=prompts,
            prompt_run=prompt_run,
        )
    else:
        prompt_run = PromptRun(
            prompt_id=prompt.unique_identifier,
            batch_id=batch_id,
            parameters=parameters,
            timestamp=int(time.time()),
            description=description,
            name=name,
            themes_list=themes_list,
        )
        prompt_run_id = "fake_prompt_run_id"
        for question in tqdm(question_list):
            time.sleep(sleep_time)
            run_prompt(
                question=question,
                prompt=prompt,
                prompt_run=prompt_run,
                prompt_run_id=prompt_run_id,
                response_format=response_format,
                retrieve_theme_func=retrieve_theme_func,
                validation_func=validation_func,
                dry_run=dry_run,
            )

        return PromptRunInfo(
            run_id=prompt_run_id,
            prompts=prompts,
            prompt_run=prompt_run,
        )
