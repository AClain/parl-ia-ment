# About this project

This project was done in colaboration with students of Epitech (Romain MULARCZYK, Thibault VALLET and Myriam ABDELLI) in the context of the writing of a scientific paper about _Automating Topic Classification of French Parliamentary
Questions with Large Language Models_. This project was used to prompt an LLM (mainly _OpenAI's GPT 4o-mini_) using an interface written in Python inside of different notebooks. To see the final result, refer to this README and the _notebooks_ folder inside _src_.

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

Expected Calibration Error (ECE) is a metric that measures how well the predicted probabilities of a model align with the actual outcomes. ECE is useful when dealing with models that output confidence scores or probabilities, as it shows whether the model’s confidence matches its accuracy.

For example, if a model predicts something with 80% confidence, it should be correct 80% of the time for that prediction to be considered well-calibrated.

How is it calculated:

ECE is computed by grouping predictions into bins based on their predicted probability (e.g., 10 bins for probabilities ranging from 0 to 1). For each bin, the difference between the average predicted confidence and the actual accuracy in that bin is calculated. The final ECE is a weighted average of these differences, where the weight corresponds to the number of samples in each bin.

### Krippendorff's alpha

Krippendorff's alpha is a reliability metric used to measure the agreement between multiple raters or coders. It accounts for the possibility of the agreement occurring by chance and can handle multiple coders, missing data, and different types of data (nominal, ordinal, interval, or ratio scales).

How is it calculated:

Krippendorff’s alpha is calculated by comparing observed disagreement to expected disagreement (i.e., how often coders agree compared to what would be expected by random chance).

$$\alpha = 1 - \frac{D_o}{D_e}$$

where:
- \( D_o \) is the observed disagreement.
- \( D_e \) is the expected disagreement by chance.

A higher value (closer to 1) indicates better agreement.

### Cohen's kappa

Cohen's kappa is a statistical measure used to assess the inter-rater agreement between two raters. Like Krippendorff’s alpha, Cohen’s kappa accounts for the possibility of agreement occurring by chance.

How is it calculated:

Cohen’s kappa compares the observed agreement (how often the two raters agree) with the expected agreement (how often the two raters would agree by random chance).

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

where:
- \( P_o \) is the observed agreement.
- \( P_e \) is the expected agreement by chance.

A kappa of 1 indicates perfect agreement, while 0 indicates no agreement better than chance.

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

# Running an experiment

### Select the experiment

Once you know which experiment you want to run, select and edit an associated notebook to create a run for a specific batch of questions. The run can take up to an hour if lots of requests are done within an hour. Once the run is finished, you can plot the results using the associated `analysis.ipynb` notebook.

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
Define the size of the question batch on which to run the experiment. Defaults to 1500, more questions results in a more cost-effective run

DESCRIPTION :
Add contextual information to the prompt run

NAME :
Add a unique name for the prompt run
```
