# 6. Estimer les performances du modèle sur des catégories et du texte plus ou moins contemporain

**Hypothèse :** Les LLMs sont entraînés sur des jeux de données ultra-contemporains, consistant essentiellement de grands ensembles de texte récupérés sur le web (Common crawl). On exécute des batchs sur les législatures 8/9 et 15 qui sont les deux points extrêmes de notre jeu de données pour tester cette hypothèse.

**Batchs :**

- VIIIe législature : n = 1500
- IXe législature : n = 1500
- Xe législature : n = 1500
- XIe législature : n = 1500
- XIIe législature : n = 1500
- XIIIe législature : n = 1500
- XIVe législature : n = 1500
- XVe législature : n = 1500

**Métriques :**

- Inter-coder agreement (Cohen’s Kappa / Krippendorff’s alpha)
- F1 score par label / Macro F1 score
- Recall par label / Macro Recall
- Precision par label / Macro Precision
- Self-confidence
- Verbalized confidence
- Logprobs

**Prompt :**

- 1x Zero-shot - Vanilla [FR]
- 1x Zero-shot Verbalized confidence - Vanilla [FR]
- 1x Zero-shot Self-calibration - Vanilla [FR]

**Température :**

- 0.2