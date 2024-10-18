import os
import anthropic
from typing import Dict
from openai import OpenAI
from mistralai import Mistral
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.logger import get_logger
import google.generativeai as genai
from typing import Optional, Callable
from models.LLMOutput import WrapperOutput
from models.Prompt import Prompt, PromptRun, RoleEnum

load_dotenv()
logger = get_logger()

openai_client = OpenAI()
anthropic_client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MAX_TOKEN = 512


def prompt_openai(
    prompt: Prompt,
    prompt_run: PromptRun,
    question_text: str,
    assoc: Dict[str, str] | None = None,
    response_format: Optional[BaseModel] = None,
    retrieve_theme_func: Callable[..., str] | None = None,
) -> WrapperOutput:
    """
    Sends a prompt to OpenAI's API and retrieves a response.

    Parameters
    ----------
    prompt : Prompt
        The prompt object containing the initial prompt data.
    prompt_run : PromptRun
        Metadata related to the current run of the prompt, such as parameters and settings.
    question_text : str
        The text of the question being processed.
    assoc : Dict[str, str] | None, optional
        An optional dictionary for associating additional data, by default None.
    response_format : Optional[BaseModel], optional
        If provided, defines the format of the response to be expected, by default None.
    retrieve_theme_func : Callable[..., str] | None, optional
        A callable function that can be used to retrieve themes for the prompt, by default None.

    Returns
    -------
    WrapperOutput
        The response object wrapping the output from the OpenAI API, including the generated text.
    """
    messages = [
        {
            "role": pr.role.value,
            # Template user content contains '{0}'
            "content": pr.content.format(question_text),
        }
        for pr in list(prompt.prompts)
    ]

    if assoc:
        for i, msg in enumerate(messages):
            for k, v in assoc.items():
                messages[i]["content"] = msg["content"].replace(k, v)

    if response_format is not None:
        response = openai_client.beta.chat.completions.parse(
            temperature=prompt_run.parameters.temperature,
            max_tokens=MAX_TOKEN,
            model=prompt_run.parameters.model,
            messages=messages,  # type: ignore
            logprobs=True,
            top_logprobs=4,
            response_format=response_format,  # type: ignore
        )
    else:
        response = openai_client.chat.completions.create(
            temperature=prompt_run.parameters.temperature,
            max_tokens=MAX_TOKEN,
            model=prompt_run.parameters.model,
            messages=messages,  # type: ignore
            logprobs=True,
            top_logprobs=4,
        )

    dict_response = response.to_dict()

    logger.info(dict_response["choices"][0]["message"]["content"])

    if retrieve_theme_func is not None:
        predicted_label = retrieve_theme_func(
            prompt_run.themes_list,
            prompt_run.parameters.theme_hierarchy_level,
            dict_response["choices"][0]["message"]["content"],  # type: ignore
        )
    else:
        predicted_label = dict_response["choices"][0]["message"]["content"]  # type: ignore

    return WrapperOutput(
        raw_response=dict_response["choices"][0]["message"]["content"],  # type: ignore
        prompt_tokens=dict_response["usage"]["prompt_tokens"],  # type: ignore
        response_tokens=dict_response["usage"]["completion_tokens"],  # type: ignore
        predicted_label=predicted_label.lower().strip(),
        logprobs=dict_response["choices"][0]["logprobs"]["content"],  # type: ignore
    )


def prompt_anthropic(
    prompt: Prompt,
    prompt_run: PromptRun,
    question_text: str,
    assoc: Dict[str, str] | None = None,
    retrieve_theme_func: Callable[..., str] | None = None,
) -> WrapperOutput:
    """
    Sends a prompt to Anthropic's API and retrieves a response.

    Parameters
    ----------
    prompt : Prompt
        The prompt object containing the initial prompt data.
    prompt_run : PromptRun
        Metadata related to the current run of the prompt, such as parameters and settings.
    question_text : str
        The text of the question being processed.
    assoc : Dict[str, str] | None, optional
        An optional dictionary for associating additional data, by default None.
    response_format : Optional[BaseModel], optional
        If provided, defines the format of the response to be expected, by default None.
    retrieve_theme_func : Callable[..., str] | None, optional
        A callable function that can be used to retrieve themes for the prompt, by default None.

    Returns
    -------
    WrapperOutput
        The response object wrapping the output from the Anthropic API, including the generated text.
    """
    system_prompt = next(
        (pr for pr in prompt.prompts if pr.role == RoleEnum.System.value),
        None,
    )
    messages = [
        {
            "role": pr.role.value,
            # Template user content contains '{0}'
            "content": pr.content.format(question_text),
        }
        for pr in list(prompt.prompts)
        if pr.role != RoleEnum.System.value
    ]

    if assoc:
        for i, msg in enumerate(messages):
            for k, v in assoc.items():
                messages[i]["content"] = msg["content"].replace(k, v)

    response = anthropic_client.messages.create(
        model=prompt_run.parameters.model,
        max_tokens=MAX_TOKEN,
        temperature=prompt_run.parameters.temperature,
        system=system_prompt.content,  # type: ignore
        # ? top_k=1,
        # ? top_p=3,
        messages=messages,
    )

    dict_response = response.to_dict()

    if retrieve_theme_func is not None:
        predicted_label = retrieve_theme_func(
            prompt_run.themes_list,
            prompt_run.parameters.theme_hierarchy_level,
            dict_response["content"][0]["text"],  # type: ignore
        )
    else:
        predicted_label = dict_response["content"][0]["text"]  # type: ignore

    return WrapperOutput(
        raw_response=dict_response["content"][0]["text"],  # type: ignore
        prompt_tokens=dict_response["usage"]["input_tokens"],  # type: ignore
        response_tokens=dict_response["usage"]["output_tokens"],  # type: ignore
        predicted_label=predicted_label,
        logprobs=None,
    )


def prompt_mistral(
    prompt: Prompt,
    prompt_run: PromptRun,
    question_text: str,
    assoc: Dict[str, str] | None = None,
    retrieve_theme_func: Callable[..., str] | None = None,
) -> WrapperOutput:
    """
    Sends a prompt to Mistral's API and retrieves a response.

    Parameters
    ----------
    prompt : Prompt
        The prompt object containing the initial prompt data.
    prompt_run : PromptRun
        Metadata related to the current run of the prompt, such as parameters and settings.
    question_text : str
        The text of the question being processed.
    assoc : Dict[str, str] | None, optional
        An optional dictionary for associating additional data, by default None.
    response_format : Optional[BaseModel], optional
        If provided, defines the format of the response to be expected, by default None.
    retrieve_theme_func : Callable[..., str] | None, optional
        A callable function that can be used to retrieve themes for the prompt, by default None.

    Returns
    -------
    WrapperOutput
        The response object wrapping the output from the Mistral API, including the generated text.
    """
    messages = [
        {
            "role": pr.role.value,
            # Template user content contains '{0}'
            "content": pr.content.format(question_text),
        }
        for pr in list(prompt.prompts)
    ]

    if assoc:
        for i, msg in enumerate(messages):
            for k, v in assoc.items():
                messages[i]["content"] = msg["content"].replace(k, v)

    response = mistral_client.chat.complete(
        model=prompt_run.parameters.model,
        temperature=prompt_run.parameters.temperature,
        max_tokens=MAX_TOKEN,
        messages=messages,
    )

    if retrieve_theme_func is not None:
        predicted_label = retrieve_theme_func(
            prompt_run.themes_list,
            prompt_run.parameters.theme_hierarchy_level,
            response.choices[0].message.content,
        )
    else:
        predicted_label = response.choices[0].message.content

    return WrapperOutput(
        raw_response=response.choices[0].message.content,
        prompt_tokens=response.usage.prompt_tokens,
        response_tokens=response.usage.completion_tokens,
        predicted_label=predicted_label,
        logprobs=None,
    )


def prompt_google(
    prompt: Prompt,
    prompt_run: PromptRun,
    question_text: str,
    assoc: Dict[str, str] | None = None,
    retrieve_theme_func: Callable[..., str] | None = None,
) -> WrapperOutput:
    """
    Sends a prompt to Google's API and retrieves a response.

    Parameters
    ----------
    prompt : Prompt
        The prompt object containing the initial prompt data.
    prompt_run : PromptRun
        Metadata related to the current run of the prompt, such as parameters and settings.
    question_text : str
        The text of the question being processed.
    assoc : Dict[str, str] | None, optional
        An optional dictionary for associating additional data, by default None.
    response_format : Optional[BaseModel], optional
        If provided, defines the format of the response to be expected, by default None.
    retrieve_theme_func : Callable[..., str] | None, optional
        A callable function that can be used to retrieve themes for the prompt, by default None.

    Returns
    -------
    WrapperOutput
        The response object wrapping the output from the Google API, including the generated text.
    """
    system_prompt = next(
        (pr for pr in prompt.prompts if pr.role == RoleEnum.System.value),
        None,
    )

    parts = [
        {
            "parts": [
                {
                    "text": pr.content.format(question_text),
                }
            ],
            "role": pr.role.value,
        }
        for pr in prompt.prompts
        if pr.role != RoleEnum.System.value
    ]

    if assoc:
        for i, msg in enumerate(parts):
            for k, v in assoc.items():
                parts[i]["parts"][0]["text"] = msg["parts"][0]["text"].replace(k, v)

    model = genai.GenerativeModel(
        prompt_run.parameters.model,
        system_instruction=system_prompt.content,
    )

    response = model.generate_content(
        parts,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=MAX_TOKEN,
            temperature=prompt_run.parameters.temperature,
            # response_logprobs=True,
        ),
    )

    dict_response = response.to_dict()

    if retrieve_theme_func is not None:
        predicted_label = retrieve_theme_func(
            prompt_run.themes_list,
            prompt_run.parameters.theme_hierarchy_level,
            dict_response["candidates"][0]["content"]["parts"][0]["text"],
        )
    else:
        predicted_label = dict_response["candidates"][0]["content"]["parts"][0]["text"]

    return WrapperOutput(
        raw_response=dict_response["candidates"][0]["content"]["parts"][0]["text"],
        prompt_tokens=dict_response["usage_metadata"]["prompt_token_count"],
        response_tokens=dict_response["usage_metadata"]["candidates_token_count"],
        predicted_label=predicted_label,
        logprobs=None,  # ? Gratuit = pas logprobs ? :(
    )


def prompt_replicate(
    prompt: Prompt,
    prompt_run: PromptRun,
    question_text: str,
    assoc: Dict[str, str] | None = None,
    retrieve_theme_func: Callable[..., str] | None = None,
):
    return True
