# À propos des fichiers "all_themes_normalized" et "all_unique_themes.json"

À partir du fichier "all_themes_question_count", nous pouvons faire un travail de normalisation pour
réduire le nombre de thème.

Pour "all_themes_normalized.json" :

1. Tout passer en minuscule
2. Retirer les caractères spéciaux
3. Respecter la ponctuation
  a. "theme: sous-titre" => "theme : sous-titre"

Pour "all_unique_themes.json" à partir du fichier précédent :

1. Corriger les typos
  a. "franais" => "français"
2. Combiner les thèmes identiques
3. Retirer les thèmes sans questions

### Corriger les typos

```json
{
    "franais : langue": 1 => "francais : langue",
    "franais": 4 => "francais",
    "franais : ressortissants": 8 => "francais : ressortissants",
    "imps locaux": 1 => "impots locaux",
    "logement : aides et prets.": 1 => "logement : aides et prets",
}
```

### Combiner les thèmes identiques

```json
{
  "professions judiciaires": 1 => "professions judiciaires et juridiques",
  "retraite : fonctionnaires civils et militaires": 1 => "retraites : fonctionnaires civils et militaires",
  "vente et echanges": 1 => "ventes et echanges",
  "domaine public et prive": 2 => "domaine public et domaine prive",
  "insignes et emblemes": 2 => "decorations, insignes et emblemes",
  "geometres": 34 => "geometres et metreurs",
  "libertes publiques": 3 => "droits de l'homme et libertes publiques",
  "fondations": 4 => "associations",
  "associations et mouvements": 31 => "associations",
  "associations et fondations": 409 => "associations",
  "etablissements de bienfaisance et fondations": 1 => "associations",
  "departements et territoires d'outre-mer": 1 => "departements",
  "fonctionnaires et agents": 1 => "fonctionnaires et agents publics",
  "journaux et bulletins officiels": 2 => "journaux officiels",
  "pain, patisserie et confiserie": 2 => "boulangerie et patisserie",
  "boulangerie patisserie": 30 => "boulangerie et patisserie",
  "armes et munitions": 5 => "armes",
  "materiel medico-chirurgical et protheses": 5 => "materiel medico-chirurgical",
  "partis et groupements politiques": 5 => "partis et mouvements politiques",
  "saisies et suretes": 79 => "saisies",
  "saisies et sequestres": 30 => "saisies",
  "ventes et commerce electronique": 6 => "ventes et echanges",
  "objets d'art et de collection": 7 => "objets d'art et de collection et antiquites",
  "objets d'art, collections, antiquites": 9 => "objets d'art et de collection et antiquites",
  "police privee": 7 => "police",
  "police municipale": 55 => "police",
  "droits de l'homme": 8 => "droits de l'homme et libertes publiques",
  "minerais": 8 => "minerais et metaux",
  "optique et instruments de precision": 8 => "instruments de precision et d'optique",
  "aquaculture": 9 => "aquaculture et peche professionnelle",
  "construction navale": 10 => "constructions navales",
  "examens et concours": 10 => "examens, concours et diplomes",
  "medecines alternatives": 11 => "medecines paralleles",
  "mutuelles : societes": 12 => "mutuelles",
  "instruments de precision et d'optique": 13 => "optique et precision",
  "sectes": 13 => "sectes et societes secretes",
  "imprimerie": 15 => "edition, imprimerie et presse",
  "langues regionales": 22 => "langues et cultures regionales",
  "cultures regionales": 30 => "langues et cultures regionales",
  "archives": 16 => "archives et bibliotheques",
  "bijoux et produits de l'horlogerie": 5 => "bijouterie et horlogerie",
  "livres": 17 => "presse et livres",
  "edition": 18 => "edition, imprimerie et presse",
  "mediateur de la republique": 2 => "mediateur",
  "professions comptables": 4 => "comptables",
  "cuir": 23 => "habillement, cuirs et textiles",
  "equipements industriels et machines-outils": 23 => "equipements industriels",
  "dechets et produits de la recuperation": 25 => "dechets",
  "ordures et dechets": 110 => "dechets",
  "metaux": 27 => "minerais et metaux",
  "poissons et produits d'eau douce et de la mer": 28 => "produits d'eau douce et de la mer",
  "bourses et allocations d'etudes": 30 => "bourses d'etudes",
  "tom et collectivites territoriales d'outre-mer": 33 => "collectivites territoriales",
  "foires et marches": 35 => "foires et expositions",
  "syndicats professionnels": 34 => "syndicats",
  "constructions aeronautiques": 23 => "construction aeronautique",
  "communication": 38 => "audiovisuel et communication",
  "etablissements de soins et de cure": 41 => "etablissements sociaux et de soins",
  "etablissements d'hospitalisation, de soins et de cure": 199 => "etablissements sociaux et de soins",
  "spectacles": 105 => "arts et spectacles",
  "religions et cultes": 45 => "cultes",
  "professions et activites immobilieres": 47 => "professions immobilieres",
  "organes humains": 49 => "sang et organes humains",
  "papier et carton": 50 => "papiers et cartons",
  "energie nucleaire": 51 => "energie et carburants",
  "energie": 247 => "energie et carburants",
  "recherche scientifique et technique": 51 => "recherche",
  "recherche et innovation": 130 => "recherche",
  "petrole et produits raffines": 54 => "petrole et derives",
  "chasse": 55 => "chasse et peche",
  "protection civile": 58 => "securite civile",
  "patrimoine archeologique, esthetique, historique et scientifique": 59 => "patrimoine culturel",
  "sang": 66 => "sang et organes humains",
  "calamites et catastrophes": 68 => "catastrophes naturelles",
  "conferences et conventions internationales": 70 => "traites et conventions",
  "nuisances": 72 => "dechets, pollution et nuisances",
  "pollution et nuisances": 258 => "dechets, pollution et nuisances",
  "politique sociale": 3153 => "politique economique et sociale",
  "politique economique": 1256 => "politique economique et sociale",
  "habillement, cuirs et textiles": 77 => "textile et habillement",
  "medicaments": 79 => "pharmacie et medicaments",
  "economie sociale et solidaire": 81 => "economie sociale",
  "ceremonies publiques et commemorations": 84 => "ceremonies publiques et fetes legales",
  "alcools et boissons alcoolisees": 93 => "boissons et alcools",
  "assainissement": 99 => "eau et assainissement",
  "television": 746 => "radiodiffusion et television",
  "bibliotheques": 127 => "archives et bibliotheques",
  "audiovisuel": 133 => "audiovisuel et communication",
  "presse": 159 => "presse et livres",
  "institutions sociales et medico sociales": 191 => "institutions sociales et medico-sociales",
  "mort et deces": 192 => "mort",
  "apprentissage": 194 => "formation professionnelle et apprentissage",
  "pollution": 202 => "dechets, pollution et nuisances",
  "taxes parafiscales": 217 => "impots et taxes",
  "successions et liberalites": 224 => "donations et successions",
  "agro-alimentaire": 257 => "agroalimentaire",
  "dechets": 307 => "dechets, pollution et nuisances",
  "automobiles": 366 => "automobiles et cycles",
  "pensions militaires d'invalidite et des victimes de guerre": 369 => "pensions militaires d'invalidite",
  "pharmacie": 382 => "pharmacie et medicaments",
  "dom": 471 => "dom-tom",
  "patrimoine culturel": 1112 => "patrimoine",
  "formation professionnelle": 2105 => "formation professionnelle et apprentissage",
  "droits d'enregistrement et de timbre": 172 => "enregistrement et timbre",
  "professions et activites paramedicales": 22 => "professions paramedicales",
}
```

### Retirer les thèmes sans questions

```json
{   
    "budget": 0,
    "bureautique": 0,
    "engrais": 0,
    "industrie, p et t et tourisme": 0,
    "marches d'interet national": 0,
    "recherche et enseignement superieur": 0,
    "t.v.a.": 0,
    "travailleurs independants et autoentrepreneurs": 0
}
```
