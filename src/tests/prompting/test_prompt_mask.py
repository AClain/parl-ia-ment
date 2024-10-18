from prompting.prompt_mask import question_processing


def test_prompt_mask(real_prompt_environnement):
    expected = """Agis comme un assistant de recherche chargé d'annoter des documents. Ton rôle est d'attribuer un label sous la forme d'une lettre à une question posée par un député à l'Assemblée nationale française. Chaque thème est associé à une lettre de A à U. La liste des thèmes est la suivante :
- A. retraites
- B. ministères et secrétariats d'état
- C. handicapés
- D. enseignement
- E. politique extérieure
- F. agriculture
- G. logement
- H. anciens combattants et victimes de guerre
- I. énergie et carburants
- J. impôts et taxes
- K. sécurité sociale
- L. justice
- M. entreprises
- N. outre-mer
- O. déchets, pollution et nuisances
- P. communes
- Q. commerce et artisanat
- R. sports
- S. consommation
- T. famille
- U. étrangers
Ta réponse ne doit contenir qu'une seule chose : la lettre associée au thème correspondant. Par exemple `A` pour `retraites` ou `B` pour `ministères et secrétariats d'état`.

Question: M. Éric Jalton attire l'attention de Mme la ministre à propos du schéma national des véloroutes et voies vertes et son application dans les départements ultramarins. Il lui demande quelles mesures elle compte prendre en collaboration avec le ministère de l'outre-mer pour le développement et l'adaptation de ce schéma national en outre-mer qui favoriseraient la pratique vélocipédique en lien avec les objectifs fixés par la loi de transition énergétique relatifs aux modes de mobilité douce.
Label: N
"""
    result = question_processing(real_prompt_environnement)
    assert expected == result


def test_prompt_mask_commerce_et_artisanat(
    real_prompt_commerce_et_artisanat
):
    expected = """Ton rôle est d'attribuer un thème à une question posée par un député à l'Assemblée nationale française. La liste des thèmes est la suivante :
- retraites
- ministères et secrétariats d'état
- handicapés
- enseignement
- politique extérieure
- agriculture
- logement
- anciens combattants et victimes de guerre
- énergie et carburants
- impôts et taxes
- sécurité sociale
- justice
- entreprises
- outre-mer
- déchets, pollution et nuisances
- communes
- commerce et artisanat
- sports
- consommation
- famille
- étrangers
Ta réponse doit contenir une seule chose: le thème correspondant, par exemple `retraites` ou `ministères et secrétariats d'état`. Le thème assigné doit être un des thèmes de la liste fournie. Seuls les thèmes de la liste précédente sont valides.

Question: M. André Schneider * attire l'attention de M. le ministre d'État, ministre sur sa proposition de modifier la réglementation en vigueur concernant l'ouverture dominicale des commerces qu'il a présentée dans le cadre d'une série de mesures visant à soutenir l'activité économique et relancer la consommation. Après l'ouverture de la publicité télévisée aux grandes enseignes et la libéralisation des règles promotionnelles en matière de crédit gratuit, il est à craindre que l'accroissement des dérogations en faveur de l'ouverture des magasins le dimanche remette en cause l'équilibre fragile instauré entre les différentes formes de commerce que sont la grande distribution et le commerce de détail au détriment de ce dernier. Au-delà de la volonté tout à fait louable de relancer la consommation, il convient de s'interroger sur les risques concurrentiels que représente l'ouverture des magasins le dimanche au regard des vertus que représente, avec 1 million d'entreprises artisanales et de commerce indépendant, le commerce de détail en matière d'aménagement du territoire ou de cohésion sociale. Aussi, il lui demande de bien vouloir lui préciser ses intentions dans ce domaine.
Label: commerce et artisanat
"""
    result = question_processing(real_prompt_commerce_et_artisanat)
    assert expected == result


def test_prompt_mask_enseignement(real_prompt_enseignement):
    expected = """Ton rôle est d'attribuer un thème à une question posée par un député à l'Assemblée nationale française. La liste des thèmes est la suivante :
- retraites
- ministères et secrétariats d'état
- handicapés
- enseignement
- politique extérieure
- agriculture
- logement
- anciens combattants et victimes de guerre
- énergie et carburants
- impôts et taxes
- sécurité sociale
- justice
- entreprises
- outre-mer
- déchets, pollution et nuisances
- communes
- commerce et artisanat
- sports
- consommation
- famille
- étrangers
Ta réponse doit contenir une seule chose: le thème correspondant, par exemple `retraites` ou `ministères et secrétariats d'état`. Le thème assigné doit être un des thèmes de la liste fournie. Seuls les thèmes de la liste précédente sont valides.

Question: M. Alexis Corbière attire l'attention de M. le ministre sur les conséquences pédagogiques de la crise sanitaire et des mesures de confinement en vigueur depuis le 17 mars 2020. Pour de nombreuses familles n'ayant pas accès aux outils numériques, ce confinement se traduit en deux mois de cours perdus. Pour d'autres, la singularité des cours à distance a pu entraîner de lourdes difficultés d'apprentissage. Les équipes pédagogiques s'inquiètent et témoignent que certains élèves n'assistent pas aux cours à distance. Dès lors, ce temps de scolarité perdu nécessitera des mesures de rattrapage dès la rentrée prochaine. Il est donc crucial de connaître le nombre exact d'élèves n'ayant pas pu assister aux cours en ligne afin de mieux les accompagner,a fortioris'ils sont rattachés à un établissement d'éducation prioritaire. C'est pourquoi il demande à connaître le nombre d'élèves concernés dans le département de la Seine-Saint-Denis pour les premier et second degrés, en enseignement général et professionnel, et notamment ceux relevant des établissements du régime d'éducation prioritaire. Il souhaite également être informé des moyens prévus pour la rentrée prochaine afin d'assurer le rattrapage des lacunes et retards causés par le confinement.
Label: enseignement
"""
    result = question_processing(real_prompt_enseignement)
    assert expected == result
