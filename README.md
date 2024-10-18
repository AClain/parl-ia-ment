# Scripts

> compact_into_json.py

Export the 4 Notion tables into CSV files. Rename them as the following :
- Thèmes Lvl0 => themes_step_0.csv
- Thèmes Lvl1 => themes_step_1.csv
- Thèmes Lvl2 => themes_step_2.csv
- Thèmes Lvl3 => themes_step_3.csv

Place all the files into the `src/data` folder, then run the following :

`python3 compact_into_json.py`

The `hierarchy.json` file will be created in the `src/data` folder.

> import_themes_into_db.py

Once the `hierarchy.json` file is created, we can import all the themes into the database by running the following :

`python3 import_themes_into_db.py`

All the themes will be imported into the `Themes` collection.

> count_themes_total_questions.py

The `total` column will be empty (set to 0) for every theme. To aggregate the total number of question for each themes, we can run the following :

`python3 count_themes_total_questions.py`

All the `total` column will be filled based on the `Questions` collection.

# Working with the database (Pymongo)

### Add or update a theme

```python
from utils.helpers import generate_theme_unique_identifier

theme_name = "animaux, agriculture et agroalimentaire"
theme_level = 3
unique_identifier = generate_theme_unique_identifier(theme_name, theme_level)

theme = Theme(
    name=theme_name,
    parent_theme_identifier=None,
    unique_identifier=unique_identifier,
    level=theme_level,
    total=0, # There is an other script to get the total number of questions for a any level theme
)

theme_doc = connector.client.upsert_theme(theme)
```

### Get one or more themes

```python
theme = connector.client.get_theme({"name": "administration", "level": 1})

theme["name"] # "administration"

level_3_themes = connector.client.get_themes({"level": 3}) # Returns a Cursor
level_3_themes = list(level_3_themes) # Cast the Cursor to a list

# Retrieve all level 2 themes, sorted ASC by name
level_2_themes = connector.client.get_themes_by_level(2)
```

### Retrieve details of one or more themes

```python
connector.client.get_themes({"total": {"$gt": 1500}}) # Get all the themes with 0 or more total questions
connector.client.get_themes({"level": 2, "total": {"$gt": 1500}}) # Get all the themes at level 2 with 0 or more total questions

theme = connector.client.get_theme({"name": "administration", "level": 1}) # Get the "administration" named theme at level 0

theme["total"] # Get the total number of questions of a specific theme

# Retrieve the parent theme of the level 1 theme "agriculture"
theme = connector.client.get_theme({"level": 1, "name": "agriculture"})
top_level_theme = connector.client.get_parent_theme(theme["parent_theme_identifier"], stop_at_level=2, base_theme_level=1)

top_level_theme["name"] # "agriculture et agroalimentaire"
```

### Retrieve all sub themes of a given theme

```python
# Get the "industrie" theme at level 0
theme = connector.client.get_theme({"name": "industrie", "level": 0})

# Get all sub themes of the "industrie" theme and flatten the list
result = connector.client.get_sub_themes_list_from_theme(theme["unique_identifier"], flatten=True)  # returns a list
```

### Add or update a question

```python
from models.Question import Question, QuestionType

question = Question(
    id: "13-132810QE"
    congressman: "Goldberg Daniel"
    questioned_ministry: "Intérieur"
    responsible_ministry: "Intérieur"
    question_date: date.strftime('%Y-%m-%d')
    response_date: date.strftime('%Y-%m-%d')
    theme: "transports aériens"
    sub_theme: "aéroports"
    question_text: "M. Daniel Goldberg attire l'attention de M. le ministre de l'intérieur sur les problèmes d'autorisation et de renouvellement des badges d'accès aux zones aéroportuaires. (...)"
    response_text: "(...)"
    question_type: QuestionType.QUESTION_ECRITE
)

question = connector.client.upsert_question(question)
```

### Get one or more questions

```python
question = connector.client.get_question({"id": "13-132810QE"})

question_ids = ["13-132810QE", "13-132809QE", "13-132808QE"]
questions = connector.client.get_questions({"id": {"$in": question_ids}}) # Returns a Cursor
questions = list(questions) # Cast the Cursor to list

# Get 1000 random questions from the 13th legislature
random_questions = connector.client.get_random_questions({
    number_of_questions=1000, legislature=13
}) # Returns a Cursor
random_questions = list(random_questions) # Cast Cursor to list
```

### Aggregate questions

```python
# Retrieve all questions asked in 2015
year = 2015
questions = connector.client.aggregate_questions(
    [
        {"$match": {"question_date": {"$regex": f"{year}-"}}},
    ]
) # Returns a Cursor
questions = list(questions) # Cast the Cursor to list

# Retrieve all questions asked during the 13th legislature
legislature = 13
questions = connector.client.aggregate_questions(
    [{"$match": {"id": {"$regex": f"{legislature_number}-"}}}]
)
```

### Count questions

```python
# Count number of questions for a given theme (only works for level 0 themes)
number_of_questions = connector.client.count_documents_by_theme("agriculture")

print(number_of_questions) # 12225
```

### Add or update a prompt

```python
from models.Prompt import Prompt, PromptText, RoleEnum
from utils.helpers import hash_list

system_prompt = (
    "Ton rôle est d'attribué un thème à une question posée par un député à l'Assemblée Nationale."
    "(...)"
)

question = (...)
user_prompt = question["question_text"]

prompts = [
    PromptText(role=RoleEnum.System.value, content=system_prompt).model_dump(),
    PromptText(role=RoleEnum.User.value, content=user_prompt).model_dump(),
]

prompt = Prompt(
    unique_identifier=hash_list(prompts),
    prompts=prompts,
)

prompt = connector.client.upsert_prompt(prompt)
```

### Get one or more prompts

```python
prompt = connector.client.get_prompt({"unique_identifier": "47af3b6af20cd7a(...)cd3b98c078de8"})

unique_identifiers = []
prompts = connector.client.get_prompts({"unique_identifier": { "$in": unique_identifiers }}) # Returns a Cursor
prompts = list(prompts) # Cast Cursor to list
```

### Add batches

```python
from models.Batch import Batch
from prompting.create_batch import get_sample

batch = Batch(
    question_ids=get_sample(size=1000),
    size=sample_size,
)

batch = connector.client.add_batch(batch)
```

### Get one or more batches

```python
from bson import ObjectId
batch = connector.client.get_batch({"_id_": ObjectId("66e30fdd937b37056f9e3d40")})

unique_identifiers = []
batchs = connector.client.get_batches({"unique_identifier": { "$in": unique_identifiers }}) # Returns a Cursor
batchs = list(batchs) # Cast Cursor to list
```

### Add prompt runs
```python
from models.Prompt import PromptRun

prompt_run = PromptRun(
    prompt_id=prompt["unique_identifier"],
    batch_id=batch_id,
    parameters={"temperature": 0, "model": "gpt-3.5-turbo", "type": "zero-shot"},
    timestamp=int(time.time()),
    name="Zero-shot [FR] OpenAI"
)
prompt_run = connector.client.add_prompt_run(prompt_run)
```

### Get prompt runs

```python
from bson import ObjectId

run = connector.client.get_prompt_run({
    "_id": ObjectId(run_id)
})
```

### Add prompt results

```python
from models.Prompt import PromptResult

prompt_result = PromptResult(
    run_id="66e4141(...)094409b",
    question_id="13-131118QE",
    batch_id="66e4141(...)094409b",
    prompt_id="913db8de6f9c326f(...)4362138e2a48e24e34",
    response="administration",
    response_tokens=response_tokens,
    prompt_tokens=prompt_tokens,
    legislature=legislature,
    confidence=confidence,
)

connector.client.add_prompt_result(prompt_result)
```

### Get one or more prompt results

```python
run_results = connector.client.get_prompt_results({"run_id": run_id}) # Returns a Cursor
run_results_list = list(run_results) # Cast Cursor to list
```

### Update many

For example, to update many PromptResults

```python
# This will rename the "question_theme_mapping" column to "gold_label" for every PromptResult in the database
connector.client.update_many_prompt_results({"$rename": {"question_theme_mapping": "gold_label"}})

# This will remove the "confidence" column for every PromptResult in the database
connector.client.update_many_prompt_results({"$unset": {"confidence": ""}})

# This will add a column named "wrapper" with the value of ""
connector.client.update_many_prompt_results({"$set": {"wrapper": "openai"}})
```

# Measurements

### Precision

Precision is a measure of how many selected items are actually relevant. It tells you the proportion of true positive results out of all the results that were predicted to be positive. For example, if a search algorithm returns mostly correct results, it has high precision.

How is it calculated :

We loop through all the results of a run. If the predicted theme (by the LLM) is the same as in our theme mapping, we count it as a true positive. We also keep track of every time a theme as been predicted by the LLM, whether it's a true or false positive that we call "retrieved". At the end of the loop, we divide the number of true positives by the number of question that were predicted to be the same theme to obtain a precision measure between 0 and 1.

### Recall

Recall measures how many relevant items were selected out of all the possible relevant items. It shows the proportion of true positive results out of all actual positives, emphasizing the ability to retrieve all relevant instances.

How is it calculated :

We loop through all the results of a run. If the predicted theme (by the LLM) is the same as in our theme mapping, we count it as a true positive. At the end of the loop, we divide the number of true positives by the number of question that were the same theme to obtain a recall measure between 0 and 1.

### F-score / F-measure

The F-score (or F1-score) is a measure that balances precision and recall in a single metric. The F-score is the harmonic mean of precision and recall, providing a combined measure of a test's accuracy. A perfect F-score is 1, meaning perfect precision and recall, while 0 indicates both are absent. Different F-scores can weigh precision and recall differently depending on the problem.

How is it calculated :

$$F_1 = 2 \times \frac{\text{precision} \times \text{recall}}{\text{precision} + \text{recall}}$$

### Expected Calibration Error (ECE)

### Krippendorff's alpha

### Cohen's kappa

### Student's t-test

### Chi-squared test

# How to prompt

# Available LLM wrapper

- OpenAI's GPT
  - set WRAPPER to "openai"
  - [docs](https://docs.anthropic.com/en/api/getting-started)
  - [pricing](https://openai.com/api/pricing/)
    - gpt-3.5-turbo (less expensive)
    - gpt-4o-mini-2024-07-18

- Anthropic's Claude
  - set WRAPPER to "anthropic"
  - [docs](https://docs.anthropic.com/en/api/getting-started)
  - [pricing](https://docs.anthropic.com/en/docs/about-claude/models#model-comparison-table)
    - claude-3-haiku-20240307 (less expensive)
    - claude-3-5-sonnet-20240620

- Google's Gemini
  - set WRAPPER to "google"
  - [docs](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
  - [pricing](https://ai.google.dev/pricing)
    - models/gemini-1.5-flash (less expensive)
    - models/gemini-1.5-pro

- Mistral's AI
  - set WRAPPER to "mistral"
  - [docs](https://docs.mistral.ai/getting-started/quickstart/)
  - [pricing](https://mistral.ai/technology/)
    - open-mistral-nemo-2407 (less expensive)
    - mistral-small-2409

- Replicate's API
  - set WRAPPER to "replicate"
  - [docs](https://replicate.com/docs/get-started/python)
  - [pricing](https://replicate.com/pricing)

# Run an experiment

### Select the experiment

Once you know which experiment you want to run, select and edit an associated notebook to create a run for a specific batch of questions. The run can take up to an hour if lots of requests are done within an hour. Once the run is finished, you can plot the results using the associated `plot_results.ipynb` notebook. Be thorough to report all the results into the associated Notion page.

```
Available models (based on selected Wrapper, sorted by pricing) :
WrapperEnum.OpenAI
- gpt-3.5-turbo
- gpt-4o-mini-2024-07-18

WrapperEnum.Anthropic
- claude-3-haiku-20240307
- claude-3-5-sonnet-20240620

WrapperEnum.Google
- gemini-1.5-flash
- gemini-1.5-pro

WrapperEnum.Mistral
- open-mistral-nemo-2407
- mistral-small-2409

THEME_HIERARCHY_LEVEL :
- Level 3 themes are the top themes
- Level 0 is the initial theme list as defined by the Assemblée nationale

TEMPERATURE :
Set the temperature to 0.0 for a more deterministic output, 1.0 for a more random output

BATCH_ID :
Defines an existing questions list on which to rerun a new experiment
(either 'None' or an existing ID in the database)

QUESTION_SIZE_SAMPLE :
Define the size of the question batch on which to run the experiment. Defaults to 1000, more questions results in a more cost-effective run

COMMENT :
Add contextual information to the prompt run
```