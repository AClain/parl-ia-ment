import re
from scrapers.questions.scrape_pre_13_questions import ScrapePre13Questions
from scrapers.questions.scrape_post_13_questions import ScrapePost13Questions
from scrapers.questions.scrape_post_16_questions import ScrapePost16Questions


def test_scrape_question_8():
    url = "https://questions.assemblee-nationale.fr/q8/8-19975QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "8-19975QE")
    result = scraper.question_data
    expected = {
        "id": "8-19975QE",
        "congressman": "M.Abelin Jean-Pierre",
        "questioned_ministry": "agriculture",
        "responsible_ministry": "agriculture",
        "question_date": "09/03/1987",
        "response_date": "22/02/1988",
        "theme": "Lait et produits laitiers",
        "sub_theme": "Quotas de production: Poitou-Charentes",
        "analysis": "Producteurs; revendications",
        "question_text": "",
        "response_text": """Reponse. - Conformement aux decisions figurant dans l'arrete de campagne en date du 25 juillet 1986, apres une large concertation avec les parlementaires et les responsables professionnels, les producteurs ayant depasse de plus de 20 000 litres leurs quantites de reference seront penalises au titre de la campagne 1986-1987. Ce seuil a ete porte a 40 000 litres pour les producteurs de la zone de montagne. Le but de cette disposition, prevue dans la reglementation communautaire, est de retablir une certaine egalite de traitement entre les producteurs. En effet, alors que tous les producteurs de lait de la Communaute economique europeenne sont astreints a maitriser leur production, le choix du quota par laiterie ne saurait autoriser certains d'entre eux a s'affranchir totalement de la contrainte generale. Les montants ainsi preleves pourront contribuer au financement des programmes regionaux de restructuration laitiere."""
    }
    assert result == expected


def test_scrape_question_9():
    url = "https://questions.assemblee-nationale.fr/q9/9-48450QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "9-48450QE")
    result = scraper.question_data
    expected = {
        "id": "9-48450QE",
        "congressman": "M.Trémel Pierre-Yvon",
        "questioned_ministry": "équipement, logement,du transport et espace",
        "responsible_ministry": "équipement, logement,du transport et espace",
        "question_date": "14/10/1991",
        "response_date": "30/03/1992",
        "theme": "Logement",
        "sub_theme": "APL",
        "analysis": "Conditions d'attribution. couples en instance de divorce",
        "question_text": """M Pierre-Yvon Tremel attire l'attention de M le ministre de l'equipement, du logement, des transports et de l'espace sur une mesure qui a ete prise a partir de la circulaire de la CNAF no 43 du 10 aout 1990 relative aux modalites de calcul de l'aide personnalisee au logement pour les couples separes et en instance de divorce. Cette mesure qui est une interpretation de la directive no 2 du FNH consiste a prendre en compte desormais la moitie seulement de la mensualite de remboursement de prets pour calculer le montant de l'APL, ce qui devrait entrainer de graves consequences pour les menages se trouvant dans de telles situations. En effet, un couple avec trois enfants qui avait un revenu familial net de 7 727 francs remboursait chaque mois 1 316 francs (mensualite de 3 653 francs moins l'APL de 2 337 francs). Avec le nouveau calcul, le parent reste seul avec ses enfants et dont le revenu net est toujours de 7 727 francs voit son APL reduite a 1 166 francs, ce qui ne lui permet pas de faire face a ses remboursements mensuels qui passent a 2 487 francs. Dans le cas present, la personne concernee a ete dans l'obligation de mettre sa maison en vente. En consequence, il lui demande de bien vouloir lui faire part de son interpretation de la circulaire de la CNAF et de son sentiment sur les consequences des nouvelles modalites de determination du droit a l'APL concernant les situations consecutives aux divorces, separations et cessations de vie commune.""",
        "response_text": """Reponse. - Le mode de calcul de l'aide personnalisee au logement (APL) en cas de separation ou de divorce, tel qu'il resultait de la circulaire de la caisse nationale des allocations familiales (CNAF) no 43 du 10 aout 1990 visait a remedier aux problemes poses par le principe general de l'APL selon lequel le beneficiaire doit supporter une depense de logement. En effet, lorsque la personne qui occupait le logement n'acquittait aucune charge de logement, parce que cette charge etait supportee par son conjoint a titre de pension alimentaire, elle n'avait droit a aucune aide au logement. Si elle a permis de faire beneficier toutes les personnes en situation de separation ou de divorce d'une aide, la solution prevue par la circulaire du 10 aout 1990 s'est averee dans certains cas moins favorable pour le beneficiaire de l'aide que la precedente pour les raisons signalees. Ces inconvenients sont inevitables des lors que les regles relatives a l'APL cherchent a apporter une solution unique, s'adaptant a la diversite des situations resultant des decisions de justice. Pour resoudre ces difficultes, le conseil de gestion du fonds national de l'habitation, apres une concertation avec les organismes payeurs vient d'adopter un projet de directive modifiant le mode de calcul de l'APL en cas de separation ou de divorce. A partir du 1er janvier 1992, l'APL sera calculee de nouveau selon le droit commun en prenant en compte la charge de logement effectivement supportee par le conjoint continuant a occuper le logement. Parallelement, une action d'information a destination des juges a ete entreprise en accord avec le ministere de la justice afin de leur signaler les problemes que pose la compensation entre pension alimentaire et charge de logement. S'agissant des beneficiaires, ils seront informes par lettre-type des organismes payeurs de la facon dont ils pourront beneficier de l'aide dans les meilleures conditions possibles. Cette solution, qui devrait resoudre les difficultes actuelles,, sera egalement applicable en matiere d'allocation de logement."""
    }
    assert result == expected


def test_scrape_question_10():
    url = "https://questions.assemblee-nationale.fr/q10/10-33145QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "10-33145QE")
    result = scraper.question_data
    expected = {
        "id": "10-33145QE",
        "congressman": "M.Bousquet Dominique",
        "questioned_ministry": "travail et affaires sociales",
        "responsible_ministry": "travail et affaires sociales",
        "question_date": "18/12/1995",
        "response_date": "08/04/1996",
        "theme": "Chomage : indemnisation",
        "sub_theme": "UNEDIC",
        "analysis": "Affiliation. entreprises ayant recours a l'enoisage",
        "question_text": """M. Dominique Bousquet attire l'attention de M. le ministre du travail et des affaires sociales sur la situation des entreprises ayant recours a l'enoisage et sur le risque d'un conflit avec l'ASSEDIC au sujet des cotisations qu'elle souhaite leur reclamer. En effet, l'extraction manuelle des cerneaux de noix est une activite traditionnelle et familiale. Les conditions tres specifiques de cette activite ont necessite des negociations qui ont abouti a la signature, le 10 octobre 1994, d'une circulaire conjointe du ministere du travail, de l'emploi et de la formation professionnelle et du ministere des affaires sociales, de la sante et de la ville. Ainsi, selon cette circulaire, il est considere que « les entreprises ayant recours a l'enoisage ne doivent pas etre tenues aux obligations decoulant de l'application du code du travail et notamment (...) l'affiliation a l'acquittement des cotisations aux ASSEDIC ». Bien que ce document n'ait pas suscite de reaction particuliere au moment de sa diffusion, la commission paritaire nationale de l'assurance chomage, organe deliberatif de l'UNEDIC, reunie le 17 fevrier 1995, s'appuyant sur la disposition d'ordre public etablissant une incontournable presomption de salariat pour tout travailleur a domicile (art. L. 721-1 du code du travail) n'entrant pas dans le champ d'application du premier alinea de l'article L. 120-33 du code du travail, decidait qu'elle etait fondee a percevoir des cotisations sur les sommes versees aux enoiseurs. Ainsi l'UNEDIC remet-elle en cause les bases de l'accord et la profession risque de reagir tres vivement en decidant notamment de faire realiser, hors territoire national, la plus grande partie de l'enoisage. Dans ce cas, l'URSSAF se trouverait privee du versement de cotisations salariales estimees a 1,5 millions de francs par campagne et l'economie locale pourrait perdre le benefice d'un apport de dix millions de francs annuels. Aussi serait-il souhaitable que les dispositions prises par la lettre circulaire du 10 octobre 1994 soient appliquees par l'UNEDIC. C'est pourquoi il lui demande de bien vouloir lui faire savoir si les instructions contenues dans la circulaire du 10 octobre 1994 precitee continuent a s'appliquer et restent opposables a l'UNEDIC.""",
        "response_text": """L'honorable parlementaire a appele l'attention du ministre du travail et des affaires sociales sur la situation des entreprises ayant recours a l'enoisage au regard du regime d'assurance chomage. Eu egard a la specificite de la profession, la commission paritaire nationale de l'assurance chomage s'est reunie a plusieurs reprises pour deliberer sur le statut des enoiseurs. Outre sa decision du 17 fevrier 1995, a laquelle l'honorable parlementaire fait reference, une nouvelle seance de la commission du 24 janvier 1996 s'est prononcee pour l'assujettissement de cette profession au regime d'assurance chomage et aux modalites de recouvrement des contributions. Les partenaires sociaux considerent que la profession ne peut etre exclue de l'assurance chomage et doit pouvoir permettre aux salaries de se constituer des droits au meme titre que l'ensemble des travailleurs."""
    }
    assert result == expected


def test_scrape_question_11():
    url = "https://questions.assemblee-nationale.fr/q11/11-63158QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "11-63158QE")
    result = scraper.question_data
    scraper.question_data["question_text"] = re.sub(
        "\xa0", " ", scraper.question_data["question_text"]
    )
    scraper.question_data["question_text"] = re.sub(
        r"\s{2,}", " ", scraper.question_data["question_text"]
    )
    expected = {
        "id": "11-63158QE",
        "congressman": "M.Bourquin Christian",
        "questioned_ministry": "fonction publique et réforme de l'État",
        "responsible_ministry": "fonction publique et réforme de l'État",
        "question_date": "02/07/2001",
        "response_date": "01/10/2001",
        "theme": "fonction publique territoriale",
        "sub_theme": "filière administrative",
        "analysis": "secrétaires de mairie. carrière",
        "question_text": """M. Christian Bourquin attire l'attention de M. le ministre de la fonction publique et de la réforme de l'Etat sur l'examen professionnel auquel devraient être soumis les secrétaires de mairie des communes qui sont passées à plus de 3 500 habitants, afin d'être rattachés au cadre d'emploi des attachés territoraux. En effet, en application de la loi du 3 janvier 2001, un projet de décret devrait être prochainement soumis au Conseil supérieur de la fonction publique territoriale. Selon la note d'orientation soumise au CNFPT en février dernier, il envisagerait de soumettre à un examen professionnel tous les secrétaires de mairie employés dans des communes de plus de 3 500 habitants afin de les faires intégrer le cadre d'emploi des attachés. Or, certains de ces secrétaires de mairie ont intégré leur poste alors que leur commune était inférieure à 3 500 habitants. Ces communes, par la suite, ont vu leur population croître et ces secrétaires de mairie ont acquis une expérience qui justifie largement leur assimilation au cadre d'emploi des attachés, et ce sans qu'un examen professionnel soit nécessaire. En conséquence, il souhaiterait connaître sa position sur cette question, les mesures qu'il envisage de prendre, sous quelle forme et dans quels délais.""",
        "response_text": """Les conditions d'exercice des fonctions de secrétaire de mairie dans les 34 000 communes dont la population ne dépasse pas 3 500 habitants correspondent à une diversité de situations statutaires, notamment en raison de la taille des communes et de l'hétérogénéité de leurs besoins, à laquelle les représentants des élus locaux, et en particulier l'Association des maires de France, demeurent attachés. Il convient de rappeler que ces fonctions, dans les communes de moins de 2 000 habitants, peuvent être actuellement assurées par des fonctionnaires relevant de quatre cadres d'emplois différents : adjoints administratifs, rédacteurs, secrétaires de mairie et attachés. Pour les communes comprises entre 2 000 et 3 500 habitants, les fonctions sont exercées soit par les secrétaires de mairie, soit par des attachés. Au-delà, seuls ces derniers sont compétents. Il n'est pas envisagé de supprimer cette diversité de situations statutaires, mais de tendre vers une meilleure reconnaissance et une amélioration des possibilités de carrière des agents qui exercent ces fonctions. C'est pourquoi le Gouvernement a présenté au Conseil supérieur de la fonction publique territoriale (CSFPT), le 14 février 2001, une série d'orientations à ce sujet, qui ont donné lieu à une concertation avec les organisations syndicales et l'Association des maires de France (AMF), et débouché sur la rédaction d'un projet de décret qui a obtenu un avis favorable du CSFPT, lors de sa séance du 5 juillet 2001. Ce projet prévoit une possibilité d'intégration des fonctionnaires du cadre d'emplois des secrétaires de mairie dans celui des attachés territoriaux, et une mise en extinction du cadre d'emplois des secrétaires de mairie, afin qu'à l'avenir, dans les communes de plus de 2 000 habitants, le poste de secrétaire de mairie ait vocation à être occupé par les seuls attachés. En effet, malgré la réforme importante dont il a bénéficié en août 1995 (passage de la catégorie B à la catégorie A), le cadre d'emplois des secrétaires de mairie n'en continue pas moins de connaître des difficultés. Elles tiennent pour l'essentiel au caractère atypique du statut qui ne différencie pas grade et emploi, et ne favorise pas suffisamment la fluidité des déroulements de carrière et la mobilité fonctionnelle des agents. Le projet de décret entend remédier à ces difficultés et offrir en particulier des possibilités de gestion et de déroulement des carrières plus complètes à ces fonctionnaires, au nombre de 19 760 au 1er janvier 1998 (sources INSEE). La variété des niveaux de qualification et de recrutement des actuels secrétaires de mairie, les éventuelles possibilités d'avancement aux grades d'attaché principal et de directeur territorial, comme le souci de veiller à un équilibre avec les agents relevant actuellement du cadre d'emplois des attachés territoriaux (22 040 titulaires), justifient néanmoins une intégration progressive assortie de mécanismes de sélection. La période d'intégration, qui sera au moins égale à dix ans, permettra en particulier de tenir compte du dispositif de recrutement par voie d'intégration directe ou de concours réservés prévu par la loi n° 2001-2 du 3 janvier 2001 relative à la résorption de l'emploi précaire et à la modernisation du recrutement dans la fonction publique ainsi qu'au temps de travail dans la fonction publique territoriale. Une telle durée donnera ainsi aux derniers agents nommés et titularisés dans le cadre d'emplois des secrétaires de mairie, au titre du dispositif précité, la possibilité de se présenter au moins deux fois à l'examen professionnel dans le cadre d'emplois des attachés. La possibilité d'intégration sera soumise à deux conditions : la réussite à un examen professionnel et l'exigence d'une durée de services effectifs pour pouvoir s'y présenter. Cette condition d'examen professionnel répond au souci de n'intégrer dans le cadre d'emplois des attachés que des personnels qui justifient d'un niveau de compétences comparable à celui des attachés. Cependant, pour les titulaires d'un diplôme du niveau BAC + 3 - niveau de diplômes requis pour l'accès au concours externe du cadre d'emplois des attachés territoriaux - l'examen sera allégé. Sous réserve de remplir les conditions de durée de services effectifs requises le cas échéant, le nombre de présentations aux examens qui seront organisés par les délégations régionales du Centre national de la fonction publique territoriale chaque année ne sera pas limité. Une condition de durée de services effectifs sera exigée pour les intégrations réalisées au titre des huit premières années et sera supprimée les deux années suivantes, afin d'ouvrir une possibilité d'intégration à tous les membres du cadre d'emplois en fin de dispositif. Le dispositif prévu doit permettre à l'essentiel des membres du cadre d'emplois des secrétaires de mairie, actuellement en fonctions, d'intégrer le cadre d'emplois des attachés durant les cinq premières années. Les intégrations qui seront prononcées au premier grade d'attaché devront l'être au plus tard dans l'année qui suit la date de réussite à l'examen professionnel. Le cadre d'emplois étant mis en extinction, la situation individuelle des secrétaires de mairie, qui ne seraient pas intégrés en qualité d'attachés territoriaux, sera préservée ; dès lors, ceux-ci pourront continuer à exercer leurs missions dans les communes de moins de 3 500 habitants et dans les établissements publics assimilés à ces communes. Enfin, pour tenir compte de la suppression de toute possibilité de promotion interne de rédacteurs dans le cadre d'emplois des secrétaires de mairie mis en extinction, il est prévu de comptabiliser les intégrations de secrétaires de mairie prononcées dans le cadre d'emplois des attachés dans l'assiette des recrutements ouvrant droit à promotion interne dans ce dernier cadre d'emplois et de faciliter ainsi la promotion des rédacteurs. La question d'un assouplissement du quota de promotion interne au profit des adjoints administratifs exerçant les fonctions de secrétaire de communes de moins de 2 000 habitants, pour l'accès au cadre d'emplois des rédacteurs, a été évoquée en février dernier et fera l'objer d'une concertation approfondie dans les mois qui viennent en raison de la diversité des opinions enregistrées à ce sujet."""
    }
    assert result == expected


def test_scrape_question_12():
    url = "https://questions.assemblee-nationale.fr/q12/12-48328QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "12-48328QE")
    result = scraper.question_data
    scraper.question_data["question_text"] = re.sub(
        "\xa0", " ", scraper.question_data["question_text"]
    )
    scraper.question_data["question_text"] = re.sub(
        r"\s{2,}", " ", scraper.question_data["question_text"]
    )
    scraper.question_data["response_text"] = re.sub(
        "\xa0", " ", scraper.question_data["response_text"]
    )
    scraper.question_data["response_text"] = re.sub(
        r"\s{2,}", " ", scraper.question_data["response_text"]
    )
    expected = {
        "id": "12-48328QE",
        "congressman": "M.Le Nay Jacques",
        "questioned_ministry": "éducation nationale",
        "responsible_ministry": "éducation nationale",
        "question_date": "12/10/2004",
        "response_date": "14/12/2004",
        "theme": "enseignement supérieur",
        "sub_theme": "IUFM",
        "analysis": "programmes. dyslexie",
        "question_text": """M. Jacques Le Nay appelle l'attention de M. le ministre de l'éducation nationale, de l'enseignement supérieur et de la recherche sur la formation des maîtres en IUFM et sur la formation des professeurs des collèges et lycées. Il lui demande de lui indiquer le nombre d'heures consacrées à la dyslexie, notamment dans le programme de formation des maîtres en IUFM.""",
        "response_text": """La circulaire n° 2002-070 du 4 avril 2002 portant sur les principes et modalités d'organisation de la deuxième année de formation dans les IUFM précise : « En formation initiale, chaque stagiaire aura l'occasion de rencontrer pour la comprendre et l'analyser, la diversité des réalités scolaires. [Seront abordés, entre autres points, l'accueil et l'intégration des élèves handicapés et les dispositifs d'adaptation et d'intégration scolaires. [...] Les principaux supports de la formation et de l'information sur ces questions [sont par ailleurs constitués par] les différents stages, l'observation, l'analyse de pratiques professionnelles, les enseignements proposés et le travail réflexif que permet le mémoire professionnel. » Cette même circulaire précise que, dans le cadre d'une formation pour partie commune au premier et au second degré, la valeur moyenne recommandée des enseignements intégrant les questions de l'adaptation et de l'intégration scolaire est de 30 heures. Dans le cadre de son autonomie pédagogique, chaque IUFM construit et met en oeuvre un plan de formation qui reçoit un agrément ministériel s'insérant dans le cadre de la politique contractuelle quadriennale. En formation continue, les IUFM mettent en oeuvre les formations qui conduisent à la délivrance des nouvelles certifications permettant la scolarisation des enfants en situation de handicap (400 heures encadrées pour les formations du premier degré conduisant au CAPA-SH, 150 heures encadrées pour les formations du second degré conduisant au 2CA-SH). La trisomie 21 : les problématiques de la trisomie 21 sont étudiées dans les plans de formation centrés sur la prise en charge des enfants présentant des troubles importants des fonctions cognitives (option D du CAPA-SH et du 2 CA-SH). Pour l'année 2003-2004, la quasi-totalité des IUFM ont présenté pour agrément ministériel un plan de formation pour le premier degré et 17 IUFM sur 31 ont présenté un plan de formation correspondant pour le second degré. La dyslexie : dans le premier degré, les problématiques de la dyslexie sont étudiées dans les plans de formation centrés sur les aides spécialisées à dominante pédagogique (option E du CAPA-SH). Dans le second degré, ces problématiques sont étudiées soit dans les plans de formation concernant l'enseignement et l'aide pédagogique auprès des élèves des établissements régionaux d'enseignement adapté et des sections d'enseignement général et professionnel adapté (option F du 2CA-SH), soit lors des modules d'initiative nationale interacadémiques qui porteront sur les troubles du langage. L'épilepsie : les problématiques de l'épilepsie sont étudiées dans les plans de formation centrés sur la prise en charge des enfants présentant une déficience motrice grave ou un trouble de la santé évoluant sur une longue période et/ou invalidant (option C du CAPA-SH et du 2 CA-SH). Seuls l'IUFM de Lyon et le Centre national d'études et de formation pour l'enfance inadaptée (CNEFEI de Suresnes) sont habilités à former des enseignants spécialisés de cette option."""
    }
    assert result == expected


def test_scrape_question_13():
    url = "https://questions.assemblee-nationale.fr/q13/13-92799QE.htm"
    scraper = ScrapePre13Questions()
    scraper.question_scraper(url, "13-92799QE")
    result = scraper.question_data
    expected = {
        "id": "13-92799QE",
        "congressman": "M.Ginesta Georges",
        "questioned_ministry": "Industrie",
        "responsible_ministry": "Commerce, artisanat, PME, tourisme, services et consommation",
        "question_date": "09/11/2010",
        "response_date": "21/06/2011",
        "theme": "consommation",
        "sub_theme": "sécurité des produits",
        "analysis": "éclairage à diodes électroluminescentes",
        "question_text": """Selon une étude récente de l'Agence nationale de sécurité sanitaire (Anses), certains types d'éclairages à LED (diodes électroluminescentes) présentent un risque pour les yeux. Ce système d'éclairage a la particularité de comporter une forte proportion de lumière bleue dans la lumière blanche émise. C'est cette lumière bleue qui peut avoir un effet toxique sur les cellules de la rétine de l'oeil. Les enfants sont particulièrement sensibles à ce risque dans la mesure où leur cristallin encore en formation n'assure pas la même filtration de la lumière bleue. C'est pourquoi M. Georges Ginesta demande à M. le ministre chargé de l'industrie de bien vouloir lui indiquer si son analyse rejoint celle de l'Anses et les mesures qu'il entend mettre en oeuvre auprès des industriels pour éviter ce risque pour la santé.""",
        "response_text": """L'avis de l'Agence nationale de sécurité sanitaire (ANSES) relatif aux ampoules, luminaires et appareils fonctionnant grâce à la mise en oeuvre de diodes luminescentes a retenu toute l'attention des pouvoirs publics. Sur la base de tests effectués sur un échantillon restreint de produits, l'ANSES a identifié des risques liés aux effets photochimiques de cette technologie qui, dans certaines conditions d'utilisation, peuvent affecter des populations à risques ou fragiles. Les pouvoirs publics ont immédiatement informé les autorités européennes des conclusions de l'ANSES en souhaitant une réaction adaptée de la Commission. En réponse, la Commission européenne a informé les autorités françaises qu'elle avait saisi le comité scientifique placé auprès d'elle. Ce comité scientifique travaille actuellement à l'élaboration d'un avis sur les éventuels risques que peuvent poser les lumières artificielles. Cet avis intégrera les LED et les travaux de l'ANSES. Il sera communiqué à la Commission européenne qui pourra s'en saisir afin d'adapter, le cas échéant, la réglementation harmonisée déjà existante. Sans attendre les résultats de ces travaux, les autorités françaises ont élaboré un projet de décret sur les risques photobiologiques des lampes à LED destinées aux consommateurs. Ce projet propose de limiter la commercialisation des lampes LED à usage domestique aux seules lampes présentant, de manière certaine en l'état des connaissances scientifiques, un risque faible ou nul pour la santé des consommateurs. Ce projet de décret, conformément aux procédures requises par le droit communautaire a été transmis à la Commission européenne qui doit se prononcer sur sa validité au regard du traité et des directives applicables aux produits concernés."""
    }
    assert result == expected


def test_scrape_question_14():
    url = "https://questions.assemblee-nationale.fr/q14/14-103711QE.htm"
    scraper = ScrapePost13Questions()
    scraper.question_scraper(url, "14-103711QE")
    result = scraper.question_data
    expected = {
        "id": "14-103711QE",
        "congressman": "M. Olivier Audibert Troin",
        "questioned_ministry": "Défense",
        "responsible_ministry": "Défense",
        "question_date": "04/04/2017",
        "response_date": "09/05/2017",
        "theme": "impôts locaux",
        "sub_theme": "versement transport",
        "analysis": "assujettissement. armée. réglementation.",
        "question_text": """M. Olivier Audibert Troin attire l'attention de M. le ministre de la défense sur la problématique de la mise en œuvre du droit de communication des données susceptibles de permettre aux autorités organisatrices des mobilités (AOM) de déterminer le montant de l'imposition du « versement transport ». Les AOM qui organisent les transports urbains peuvent en effet demander le versement d'une taxe « transport » aux entreprises de plus de 11 employés implantées sur leurs territoires. Le montant de cette taxe résulte de l'application d'un pourcentage sur la masse salariale de l'ensemble de l'effectif employé par cette entité, qu'elle soit publique ou privée. Par principe, ces entités versent cette taxe dans son intégralité, puis sont remboursées par l'AOM sur la fraction correspondant aux employés logés en permanence ou transportés par un service propre. Pour le personnel civil et militaire de l'armée, une double dérogation était consentie jusqu'alors, permettant d'une part le calcul du versement transport sur la base d'effectifs moyens et non pas réels, et d'autre part un décompte préalable de l'assiette de calcul, de la masse salariale des personnels logés/transportés, appelé précompte. Or depuis la loi de finances rectificative de 2014, de nouvelles règles ont été introduites permettant d'entériner la règle du précompte, mais rendant illégale celle du calcul sur la base d'effectifs moyens. Depuis cette date, de nombreuses communautés demandent aux bases de défense la communication du détail des calculs du versement transport. L'objectif visé par ces démarches est à la fois de récupérer le manque à gagner résultant du paiement sur la base de l'effectif moyen, de vérifier l'écart réel entre le volume de militaires servant au calcul et les effectifs réels, de s'assurer que le paiement actuel du versement transports soit bien assis sur l'effectif réel et enfin de vérifier le calcul des effectifs logés/transportés par rapport à l'effectif total. Il lui demande en conséquence une analyse tendant à justifier le détail des calculs du versement transport et lever ainsi l'opacité ressentie qui affecte sensiblement le budget des collectivités concernées.""",
        "response_text": """Aux termes des articles L. 2333-64 et L. 2531-2 et suivants du code général des collectivités territoriales, la contribution dite « versement transport » constitue la participation des personnes publiques ou privées employant au moins 11 salariés au financement des transports en commun. Elle est perçue par les organismes ou services chargés du recouvrement des cotisations de sécurité sociale et des allocations familiales pour être reversée aux autorités organisatrices de mobilité (AOM). Conformément à la réglementation en vigueur, les versements effectués à ce titre par le ministère de la défense ne sont pas calculés sur la base d'effectifs moyens, mais prennent en compte la réalité des rémunérations servies aux personnels employés sur le périmètre géographique des AOM, l'assiette du versement transport étant constituée par ces rémunérations. Le calcul des sommes versées aux URSAFF est automatisé et effectué par les calculateurs de solde sur la base des informations transmises par les systèmes d'information de ressources humaines. Dans l'hypothèse où des difficultés en la matière viendraient à être détectées, les services du ministère ne manqueraient pas de corriger les éventuels dysfonctionnements. Enfin, il est précisé que dans la perspective du prochain déploiement du calculateur de solde ministériel « Source Solde », le ministère de la défense a constitué un groupe de travail afin, notamment, d'expertiser les processus existants. Ces travaux, qui visent en particulier à vérifier la bonne prise en compte par le ministère des déductions légales concernant les personnels logés et transportés, devraient aboutir au cours de l'année 2017."""
    }
    assert result == expected


def test_scrape_question_15():
    url = "https://questions.assemblee-nationale.fr/q15/15-43433QE.htm"
    scraper = ScrapePost13Questions()
    scraper.question_scraper(url, "15-43433QE")
    result = scraper.question_data
    expected = {
        "id": "15-43433QE",
        "congressman": "Mme Christine Pires Beaune",
        "questioned_ministry": "Solidarités et santé",
        "responsible_ministry": "Santé et prévention",
        "question_date": "11/01/2022",
        "response_date": "",
        "theme": "fonction publique hospitalière",
        "sub_theme": "Situation de la psychiatrie publique",
        "analysis": "",
        "question_text": """Mme Christine Pires Beaune attire l'attention de M. le ministre des solidarités et de la santé sur la situation des psychiatres et pédopsychiatres de la fonction publique hospitalière. La psychiatrie connaît une crise depuis plus de 10 ans avec une pénurie croissante des praticiens hospitaliers dans cette spécialité, avec plus d'un tiers des postes sur l'ensemble du territoire national qui sont actuellement non pourvus. Les assises nationales récentes ne répondent aucunement à la réalité de la situation et ne fournissent aucune solution, ni à la nature, ni à la gravité de la crise actuelle qui va s'étendre inexorablement si des mesures de sauvegarde ne sont pas prises rapidement. La question de l'attractivité médicale des postes médicaux hospitaliers est désormais une des questions essentielles. Dans ce contexte, elle lui demande d'indiquer les mesures envisagées pour soutenir les conditions matérielles d'exercice et de rémunération des activités de psychiatrie dans la fonction publique hospitalière et sur les moyens donner aux établissement pour fonctionner en intra- comme en extrahospitalier.""",
        "response_text": ""
    }
    assert result == expected


def test_scrape_question_16():
    url = "https://questions.assemblee-nationale.fr/q16/16-4020QE.htm"
    scraper = ScrapePost16Questions()
    scraper.question_scraper(url, "16-4000QE")
    result = scraper.question_data
    expected = {
        "id": "16-4020QE",
        "congressman": "M. François Piquemal",
        "questioned_minsitry": "Ville et logement",
        "responsible_ministry": "Ville et logement",
        "question_date": "13/12/2022",
        "response_date": "28/02/2023",
        "theme": "Logement",
        "sub_theme": "",
        "analysis": "",
        "question_text": """M. François Piquemal interroge M. le ministre délégué auprès du ministre de la transition écologique et de la cohésion des territoires, chargé de la ville et du logement, sur le bouclier tarifaire d'électricité pour les acteurs du logement accompagné. Les acteurs du logement accompagné (résidences sociales, foyers de jeunes travailleurs, pensions de famille...) sont frappés de plein fouet depuis plusieurs mois par l'augmentation du coût de l'électricité et du gaz. Dans la mesure où ils ne peuvent répercuter cette hausse, ils doivent la financer sur leurs fonds propres. Œuvrant dans l'intérêt général pour améliorer l'accès et les conditions de logements des personnes les plus précaires, ils ne répondent pas à une logique de marché, où les recettes peuvent s'adapter à l'évolution des dépenses, et les marges ne permettent pas de couvrir ces dépenses. Selon une enquête réalisée auprès des adhérents de l'Unafo, union professionnelle du logement accompagné, l'effet du bouclier tarifaire sur l'électricité, dans la version du projet de décret actuellement soumis à concertation, sera limité à au mieux un tiers de la hausse des coûts réels de l'énergie électrique. En effet, le surcoût par logement oscille entre 600 et 700 euros avant application du bouclier tarifaire et reste compris dans une fourchette de 450 à 550 euros par logement après application du bouclier. Cela revient à mettre en danger l'équilibre financier des structures en consommant en quelques mois les trésoreries disponibles. L'Unafo demande, d'une part, que soit couvert l'ensemble des dépenses d'électricité domestique des logements et parties communes et, d'autre part, que la totalité des surcoûts soit prise en charge sans qu'aucun plafonnement ne puisse être appliqué. Dans ces conditions, il lui demande ce qu'il compte faire pour garantir la pérennité des gestionnaires du logement accompagné.""",
        "response_text": """En 2023, le bouclier tarifaire pour l'habitat collectif, qui vise à protéger les ménages vivant en particulier dans les logements sociaux et les copropriétés, est élargi et prolongé afin de protéger tous nos concitoyens, qu'ils soient propriétaires en habitat individuel, en habitat collectif, locataires ou dans quelque situation que ce soit. Ce « bouclier collectif » concerne le gaz et l'électricité. Trois décrets relatifs à leur application ont été publiés le 31 décembre 2022 pour en préciser les modalités de mise en œuvre. Le bouclier tarifaire sur le gaz est prolongé en 2023 pour les structures d'habitat collectif. La compensation est calculée sur la base des tarifs réglementés de vente (TRV) de gaz dont la hausse a été limitée à + 15 % en janvier 2023, par rapport aux niveaux de 2022. Également, la formule de calcul de l'aide a été revue à compter du 1er janvier 2023 afin d'offrir une meilleure couverture des contrats indexés sur le PEG notamment. Les copropriétés en chauffage collectif avec un contrat de fourniture de gaz consommant plus de 150 MWh/an sont intégrées dans le périmètre du bouclier tarifaire pour les particuliers, comme c'est déjà le cas pour les copropriétés consommant moins de 150 MWh/an. Cela permettra aux copropriétés concernées de bénéficier du bouclier tarifaire directement sur leur facture, dans des délais plus courts qu'avec le dispositif du bouclier « habitat collectif » pour lequel un guichet d'aide, géré par l'agence des services de paiement (ASP) de l'Etat, est mis en place. S'agissant de l'électricité, le bouclier tarifaire pour l'habitat collectif, qui a été mis en œuvre dans un premier temps pour le second semestre 2022, est prolongé en 2023 pour les structures d'habitat collectif. La compensation est également calculée sur la base des tarifs réglementés de vente (TRV) de l'électricité dont la hausse a été limitée à + 15 % en février 2023, par rapport aux niveaux de 2022. Par ailleurs, pour renforcer le soutien aux structures qui ont souscrit des contrats d'électricité ou de gaz à prix très hauts au second semestre 2022 dans un contexte où les prix du gaz et de l'électricité étaient très élevés sur les marchés, une aide complémentaire est mise en œuvre. Au-delà du TRV non gelé (part variable) majoré de 30 %, la facture sera prise en charge à hauteur de 75 % par l'État. Dans le cadre des boucliers sur l'habitat collectif, l'aide de l'État est proportionnelle à l'énergie consommée et s'applique à l'intégralité de la consommation d'énergie des bénéficiaires. En revanche, l'effet du bouclier tarifaire en 2023 ne pourra conduire à ce qu'une facture ait un prix unitaire inférieur aux TRV gelés par l'État. Dans ces conditions, il est particulièrement important de relayer les principaux messages de vigilance auprès des structures d'habitat collectif. En particulier, il convient d'anticiper le renouvellement du contrat et d'éviter de contractualiser sur une durée supérieure à un an à prix fixe pour un prix supérieur aux prix de marché moyens. La Commission de régulation de l'énergie (CRE) publie notamment des prix de références pour des consommateurs de type PME qui ont pour vocation de permettre aux PME et aux collectivités locales amenées à souscrire ou renouveler un contrat de fourniture de s'assurer que les offres de leurs fournisseurs sont compétitives et reflètent bien la réalité des coûts d'approvisionnement."""
    }
    assert result == expected
