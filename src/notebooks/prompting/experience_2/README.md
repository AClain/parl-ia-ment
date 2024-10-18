# 2. Evaluer la stabilité des résultats pour un même ensemble de questions

**Hypothèse :** La question posée ici porte sur la stabilité (et donc la fiabilité) des résultats produits avec les annotations des LLMs. On souhaite vérifier si plusieurs exécutions, en conservant tous les hyperparamètres de l’expérience identiques, conduisent à observer des résultats différents ou non. Si les résultats observés sont très différents, les LLMs se montreraient donc peu stables pour la tâche qui nous intéresse, ce qui remettrait donc en question la validité de la méthode et questionnerait, de façon incidente, la reproducibilité des résultats.

**Littérature :**

- Michael Reiss, “Testing the reliability of ChatGPT for text annotation and classification : A cautionary remark” (2023) : recommande d’effectuer un vote à la majorité sur un ensemble de trois à cinq résultats pour chaque prompt
- Caleb Ziems et al., “Can large language models transform computational social science ?” (2024) : citant Fabrizio Gilardi et al., “ChatGPT outperforms crowd workers for text-annotation tasks” (2023), les auteurs notent que les LLMs tendent à montrer une grande cohérence interne et que les méthodes d’ensembling ne permettent pas vraiment de lisser efficacement les erreurs
- Mirela Imamovic et al., “Using ChatGPT for annotation of attitude within the appraisal theory : Lessons learned” (2024) : constatent que les résultats varient d’une run d’un prompt strictement identique à un autre
- Minzhi Li et al., “CoAnnotating : Uncertainty-guided work allocation between human and large language models for data annotation” (2023) : notent que les résultats des LLMs sont très stables lorsque ré-exécutés sur un même ensemble de données

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

**Batch :**

- n = 1500

**Prompts :**

- 5x Zero-shot - Vanilla [FR]
- 5x Zero-shot CoT - Vanilla [FR]

**Température :**

- 0.0

**Modèle :**

- OpenAI / `gpt-4o-mini-2024-07-18`