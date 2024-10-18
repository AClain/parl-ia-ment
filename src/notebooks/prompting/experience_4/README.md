# 4. Estimer l’impact de la température

**Hypothèse :** Pour des tâches plus complexes, une température plus élevée peut permettre de fournir de meilleurs résultats pour laisser s’exprimer la “créativité” du modèle. En variant la température légèrement, on ne devrait pas voir de différences significatives de variation dans les résultats.

**Littérature :**

- Fabrizio Gilardi et al., “ChatGPT outperforms crowd workers for text-annotation tasks” (2023) : une température faible (test seulement avec 0.2 et 1.0) permet de recueillir de meilleurs résultats sur des tâches comme l’”analyse de cadrage” (définir comment des articles de presse axe un sujet sur une façon de le comprendre plutôt qu’une autre), la prise de position (pour ou contre des mesures, généralement politiques), l’analyse de sentiment (positif ou négatif), l’analyse de pertinence (si une réponse est pertinente par rapport à un contexte, une question) à partir de jeux de données collectés via Twitter
- Peter Törnberg, “ChatGPT-4 outperforms experts and crowd workers in annotating political Twitter messages with zero-shot learning” (2023) : compare avec seulement deux valeurs de 0.2 et 1.0
- Meysam Alizadeh et al., “Open-source LLMs for text annotation : A practical guide for model setting and fine-tuning” (2024) : notent qu’une température plus faible permet d’augmenter la stabilité du modèle sans impact sur la précision mesurée

**Batch :**

- n = 1500

**Métriques :**

- Inter-coder agreement (Cohen’s Kappa / Krippendorff’s alpha)
- F1 score par label / Macro F1 score
- Recall par label / Macro Recall
- Precision par label / Macro Precision

**Prompts :**

- 1x Zero-shot - Vanilla [FR]
- 1x Zero-shot - Proxy [FR]
- 1x Few-shot (5-shot) - Vanilla [FR]
- 1x Few-shot (5-shot) - Proxy [FR]
- 1x Few-shot CoT (5-shot) - Vanilla [FR]
- 1x Few-shot CoT (5-shot) - Proxy [FR]

**Température :**

- 0.2
- 0.5
- 1.0

**Modèle :**

- OpenAI / `gpt-4o-mini-2024-07-18`