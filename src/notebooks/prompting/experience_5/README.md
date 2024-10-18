# 5. Estimer la calibration des modèles

**Hypothèse :** Le fine-tuning par renforcement humain (RLHF) tend à rendre les modèles très confiants de leur réponse et conduit à produire des LLMs moins bien calibrés qu’avant la phase de fine-tuning. Est-il possible d’exploiter des métriques annexes pour tenter d’obtenir une information fiable sur le niveau de confiance que le modèle attribue à un label ?

**Littérature :**

- Nicholas Pangakis, Samuel Wolken & Neil Fasching, “Automated annotation with generative AI requires validation” (2023) : utiliser des LLMs pour annoter automatiquement des corpus peut aussi permettre de mieux cibler comment répartir la tâche et confier certains cas spécifiques à vérifier par des annotateurs humains ; la mesure de “consistence” (à quel point est-ce qu’un modèle, générant un label pour un même texte à plusieurs reprise, propose des résultats divergents ou non) est très largement corrélée à la précision finalement mesurée, ceci permettant au final d’utiliser une telle mesure pour identifier des cas très spécifiques au sein d’un corpus
- Kristina Gligoric et al., “Can unconfident LLM annotations be used for confident conclusions ?” (2024) : utilisée la confidence verbalisée des modèles telle que suggérée ici n’est pas une bonne idée car les modèles tendent à être mal calibrées dans leurs confidence verbalisée sans fine-tuning préalable pour une telle tâche
- Autumn Toney-Wails, Christian Schoeberl & James Dunham, “AI on AI : Exploring the utility of GPT as an expert annotator of AI publications” (2024) : notent que la méthode de verbalisation du niveau de confiance entraîne une calibration très mauvaise avec un niveau de confiance des LLMs trop élevée par rapport aux résultats ; GPT-4 comme GPT-3 ne retournent que quelques valeurs spécifiques (0, 1 ou 0.95)
- Joseph Ornstein, Elise Balsingame & Jake Truscott, “How to train your stochastic parrot : Large language models for political texts” (2024) : sur une tâche d’annotation d’analyse de sentiment, en utilisant les logprobs GPT-4 montre une probabilité de 99% de catégoriser les textes soumis comme négatifs, GPT-3 une probabilité moyenne de 77%, les auteurs en concluent que les modèles fine-tune avec des techniques de RLHF sont mal calibrés
- Minzhi Li et al., “CoAnnotating : Uncertainty-guided work allocation between human and large language models for data annotation” (2023) : notent que les résultats des LLMs sont bien calibrés, que ce soit en utilisant des métriques de logprobs ou des métriques d’ensembling des résultats

**Métriques :**

- Self-confidence (Générer n réponses : max(predicted) / total_generation())
- Perplexity
- Verbalized confidence (80%-100%)
- Logprobs

**Prompt :**

- 1x Zero-shot - Vanilla [FR]
- 1x Zero-shot - Proxy [FR]
- 1x One-shot - Vanilla [FR]
- 1x One-shot - Proxy [FR]
- 1x Few-shot - Vanilla [FR]
- 1x Few-shot - Proxy [FR]
- 1x Few-shot CoT - Vanilla [FR]
- 1x Few-shot CoT - Proxy [FR]
- 1x Zero-shot CoT - Vanilla [FR]
- 1x Zero-shot CoT - Proxy [FR]
- 5x Zero-shot Self-calibration - Vanilla [FR]
- 5x Zero-shot CoT Self-calibration - Vanilla [FR]
- 5x Few-shot CoT Self-calibration - Vanilla [FR]

**Température :**

- 0.0

**Modèle :**

- OpenAI / `gpt-4o-mini-2024-07-18`