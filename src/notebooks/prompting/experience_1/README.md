# 1. Comparer les stratégies de prompting

**Hypothèse :** La stratégie de prompting a un impact sur les résultats de la tâche de classification. Concrètement, est-ce que la formulation du prompt a un impact sur les résultats produits. En particulier, est-ce que des modifications mineures (sans modification significative du sens global de la tâche décrite) dans la forme du prompt ont un impact sur les résultats observés ?

Pour le traduire autrement, on voudrait vérifier si deux façons différentes, en termes de forme seulement, de formuler une tâche qui serait comprise, a priori, de la même façon par un même annotateur humain, le sont aussi pour le même LLM. La question épistémologique sous-jacente porte sur le processus même d’annotation : si des modifications très mineures de formulation d’une tâche ont un impact drastique sur les performances observées des modèles, peut-on vraiment se fier à eux pour effectuer des annotations dans la mesure où de très bonnes performances observées pourraient être simplement due à un effet d’appariement statistique entre les données des jeux d’entraînement des LLMs et la ressemblance plus ou moins proche, au regard du prompt fourni, avec la tâche décrite et les données fournies à annoter en entrée du modèle.

Autrement dit, si les résultats sont très différents pour deux formulations très proches du prompt, on pourrait se demander si le modèle “comprend” vraiment la tâche ou s’il ajuste simplement des corrélations entre des données d’entrée et des données de sortie (et dans ce cas, une corrélation très forte avec un prompt donné pourrait s’effacer complètement avec un autre prompt ayant pourtant la même signification globale).

**Littérature :**

- Xingwei He et al., “AnnoLLM : Making large language models to better crowdsourced annotators” (2024) : sur un problème d’annotation qui consiste à définir si un ensemble de mots-clés sont pertinents par rapport à une recherche dans un moteur de recherche, un ensemble de questions factuelles et logiques relatives à un contexte donné auxquelles répondre par “oui” ou “non” ([BoolQ](https://paperswithcode.com/dataset/boolq)) et un problème de résolution de références consistant à définir à quel autre mot d’une phrase se réfère un pronom ou un autre moyen de construire une référence à un second groupe d’une phrase ([WiC](https://paperswithcode.com/dataset/wic)), les auteurs observent que le fait d’annoter des documents avec une explication en complément du label permet d’améliorer les performances du modèle (en suivant la stratégie plus générale dite de “chain-of-thought” décrite initialement par Jason Wei et al., “Chain-of-thought prompting elicits reasoning in large language models” (2022))
- Jason Wei et al., “Chain-of-thought prompting elicits reasoning in large language models” (2022) : décrit la technique dite de “chain-of-thought” qui consiste, en plus des exemples (few-shot) associés à la réponse attendue, à fournir une explication et un raisonnement permettant de conduire au choix de l’annotation sélectionnée en définitive par le modèle (pour un exemple illustré se référer au lien [suivant](https://learnprompting.org/docs/intermediate/chain_of_thought))
- Michael Reiss, “Testing the reliability of ChatGPT for text annotation and classification : A cautionary remark” (2023) : estime que même des modifications très mineures dans la formulation du prompt peut entraîner des écarts importants dans les résultats finaux
- Christopher Michael Rytting et al., “Towards coding social science datasets with language models” (2023) : sur une tâche d’annotation comptant 21 catégories différentes, note que les LLMs montrent une stabilité élevée dans les résultats qu’ils fournissent en fonction des variations introduites dans le prompt ; les auteurs notent également que, en utilisant du few-shot prompting, deux ou trois exemples suffisent pour noter une amélioration des résultats
- Chandreen Liyanage, Ravi Gokani & Vijay Mago, “GPT-4 as an X data annotator : Unraveling its performance on a stance classification task” (2024) : sur une tâche de détection de positionnement (pour ou contre) à partir d’un jeu de données collecté sur Twitter, les auteurs notent que la technique de Zero-shot chain-of-thought est une solution très performante et moins coûteuse que du few-shot pour réaliser des tâches d’annotation
- Meysam Alizadeh et al., “Open-source LLMs for text annotation : A practical guide for model setting and fine-tuning” (2024) : notent qu’il est difficile de savoir pour quels cas d’usage les techniques de fine-tuning fonctionnent mieux que les techniques de few-shot, ils notent également que la littérature existante sur les tâches d’annotation conduites par des LLMs ne permet pas de conclure sur le lien entre performance et complexité de la tâche, le type de modèle choisi et le type de tâche d’annotation réalisé
- Nicholas Pangakis, Samuel Wolken & Neil Fasching, “Automated annotation with generative AI requires validation” (2023) : notent que les subtilités liées au prompting n’ont pas vraiment d’impact sur les performance du modèle observées en définitive, bien qu’ils notent également qu’il s’agit tout de même de trouver, au préalable, un prompt efficace qui permette d’enregistrer des bons niveaux de performance ; partant, des modifications mineurs apportées sur un prompt fonctionnelles ne semblent pas entraîner des différences majeures dans les résultats observés
- Jonathan Mellon et al., “Do AIs know what the most important issue is ? Using language models to code open-text social survey responses at scale” (2023) : fournir le code book détaillant comment annoter chaque catégorie semble distraire le modèle de la tâche initiale et produire de moins bons résultats
- Maximilian Weber & Merle Reichardt, “Evaluation is all you need. Prompting generative large language models for annotation tasks in the social science. A primer using open models”, 2023 : notent que la nature des textes à annoter et de la tâche demandée influence largement l’efficacité des stratégies de prompt choisies
- Autumn Toney-Wails, Christian Schoeberl & James Dunham, “AI on AI : Exploring the utility of GPT as an expert annotator of AI publications” (2024) : expérimentent une série de “role” prompts (chercheur, expert d’un domain spécifique, etc.) pour annoter des articles de recherche en IA selon des sous-catégories de champs de recherche en ne notant pas de différence significative selon le rôle utilisé

**Batch :**

- n = 1500

**Métriques :**

- Inter-coder agreement (Cohen’s Kappa / Krippendorff’s alpha)
    - Vérifier si plusieurs LLMs différents annotent de la même façon les mêmes questions
    - Vérifier si un même LLM, en utilisant plusieurs prompts différents, annotent les questions de la même façon
- F1 score par label / Macro F1 score
    - Vérifier si certaines catégories sont plus “sensibles” au prompt que d’autres
- Recall par label / Macro Recall
- Precision par label / Macro Precision
- Average Self-confidence / Average Self-consistency
    - Vérifier si le prompt a un impact sur le niveau de confiance des prédictions du LLM

**Prompts :**

- 1x Zero-shot - Vanilla [FR]
- 1x Zero-shot - Assistant Role [FR]
- 1x Zero-shot - Expert Role [FR]
- 1x Zero-shot - Proxy [FR]
- 1x One-shot - Vanilla [FR]
- 1x Few-shot (3-shot) - Vanilla [FR]
- 1x Few-shot (5-shot) - Vanilla [FR]
- 1x Zero-shot CoT - Vanilla [FR]
- 1x Few-shot CoT (3-shot) - Vanilla [FR]
- 1x Few-shot CoT (5-shot) - Vanilla [FR]

**Température :**

- 0.0

**Modèle :**

- OpenAI / `gpt-4o-mini-2024-07-18`