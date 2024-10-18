# How to prompt in a notebook

Let's go through the most common prompting notebook. At the took, we define all the required parameters :

```
model = "gpt-4o-mini-2024-07-18"
themes_hierarchy_level = 1
question_sample_size = 1000
temperature = 0
batch_id = "66e7e41fd0dcb66c2ca95006"
accepted_themes_for_questions = []
themes_list = connector.client.get_themes({"level": themes_hierarchy_level})
themes_list = list(themes)
```

- `model` are choosen from [this list](https://platform.openai.com/docs/models/gpt-4o)
- `themes_hierarchy_level` is the hierarchy level of the themes in `themes_list`
- `question_sample_size` is used to create a new Batch of random questions if no `batch_id` is specified
- `temperature` is the temperature to use for the associated model
- `batch_id` is the ID of the batch to use with the prompt. Set to `None` if no batch should be used for the run
- `accepted_themes_for_questions` is the list of accepted theme for the question in the Batch. This is important for the theme mapping of each Question. If any of the Question taken in the Batch does not map to one of the theme in `themes_list`, the PromptResult for this Question will not be exploitable for metrics. Initialized as an empty list
- `themes_list` is the list of the theme to use in the prompt. All the themes MUST be of the SAME hierarchy level


Once done, we need to aggregate the list of all sub themes from the `themes_list` to fill the `accepted_themes_for_questions` list :

```
themes = list()
for theme in themes_list:
    themes.append(theme)

    sub_themes = connector.client.get_sub_themes_list_from_theme(theme["unique_identifier"], flatten=True)
    for sub_theme in sub_themes:
        if sub_theme["name"] not in accepted_themes_for_questions:
            accepted_themes_for_questions.append(sub_theme["name"])
```

We then create a string formatting all the themes to fit the prompt :

```
themes_string = "\n- "+("\n- ".join(theme["name"] for theme in themes))
themes_list = [theme["name"] for theme in themes]

system_prompt = (
    "Ton rôle est d'attribuer un thème à une question posée par un député à l'Assemblée nationale française. "
    f"La liste des thèmes est la suivante : {themes_string}. \n"
    f"Ta réponse doit contenir une seule chose: le thème correspondant, par exemple `{themes_list[0]}` ou `{themes_list[1]}`. "
    "Le thème assigné doit être un des thèmes de la liste fournie. Seuls les thèmes de la liste précédente sont valides."
)

"""
'{0}' will be replaced by the text of the question when the prompt will loop over the questions
"""
user_prompt = "{0}"

prompts = [
    PromptText(role=RoleEnum.System.value, content=system_prompt).model_dump(),
    PromptText(role=RoleEnum.User.value, content=user_prompt).model_dump(),
]

#!
comment = "15th legislature"

run_prompt(
    model=model,
    prompts=prompts,
    themes_list=themes_list,
    temperature=temperature,
    stop_at_level=themes_hierarchy_level,
    number_of_questions=question_sample_size,
    accepted_themes_for_questions=accepted_themes_for_questions,
    comment=comment,
    batch_id=batch_id
)
```