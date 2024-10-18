# 3. Comparer anglais vs. français

**Hypothèse :** Vérifier si les LLMs ont un biais pour la langue représentée en majorité dans leur corpus de pre-training et s’il est possible d’appliquer des tâches de labeling en dehors de textes en anglais.

**Littérature :**

- Bosheng Ding et al., “Is GPT-3 a good data annotator ?” (2023) : les auteurs notent que les LLMs montrent une capacité d’adaptation impressionnante, même lorsqu’ils n’ont pas été fine-tune sur les langues représentées dans le corpus à annoter, en particulier pour des tâches d’annotation linguistiques qui intéressent les auteurs de l’article (analyse de sentiment, extraction des relations entre termes, reconnaissance d’entités nommées)
- Taja Kuzman, Igor Mozetič & Nikola Ljubešić, “ChatGPT : Beginning of an end of manual linguistic data annotation ? Use case of automatic genre identification” (2023) : sur une tâche de classification de genre de documents, sur un corpus en slovène, si le prompt décrivant la tâche est formulé en anglais, les performances mesurées sur un corpus composé de documents en slovène et un corpus équivalent composé de documents en anglais, on observe au final des performances comparables ; la langue du texte sur laquelle la tâche est effectuée ne semble pas avoir un impact important, mais la langue utilisée pour décrire la tâche dans le prompt a un impact
- Steve Rathje et al., “GPT is an effective tool for multilingual psychological text analysis” (2024) : évaluent une tâche de détection de sentiment sur des corpus constitué de documents rédigés dans des langues peu représentées dans les datasets de pré-entraînement des LLMs ; ils notent également qu’il n’y a que peu de variation lorsque la tâche décrite dans le prompt est rédigée en anglais ou dans une autre langue

**Batch :**

- n = 1500

**Métriques :**

- F1 score par label / Macro F1 score
- Recall par label / Macro Recall
- Precision par label / Macro Precision

**Prompts :**

- 1x Zero-shot - Vanilla [FR]
- 1x Zero-shot - Vanilla [EN], Labels [FR]
- 1x Zero-shot - Vanilla [EN]

**Température :**

- 0.0

**Modèle :**

- OpenAI / `gpt-4o-mini-2024-07-18`