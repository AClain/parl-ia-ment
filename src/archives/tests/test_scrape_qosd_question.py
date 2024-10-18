import re
from scrapers.questions.scrape_new_questions import ScrapeNewQuestions


def test_scrape_question_8():
    pass


def test_scrape_question_9():
    pass


def test_scrape_question_10():
    pass


def test_scrape_question_11():
    pass


def test_scrape_question_12():
    pass


def test_scrape_question_13():
    pass


def test_scrape_question_14():
    pass


def test_scrape_question_15():
    url = "https://questions.assemblee-nationale.fr/q15/15-8QOSD.htm"
    scraper = ScrapeNewQuestions()
    scraper.question_scraper(url, "15-8QOSD")
    result = scraper.question_data
    response_text = """SITUATION DU CENTRE HOSPITALIER D'AUBENAS

M. le président. La parole est à M. Fabrice Brun, pour exposer sa question, n°  8, relative à la situation du centre hospitalier d'Aubenas.

M. Fabrice Brun. Madame la ministre des solidarités et de la santé, nos centres hospitaliers, qui sont en lien avec nos médecins et nos hôpitaux locaux, constituent la pierre angulaire de notre organisation sanitaire régionale. C'est particulièrement vrai dans ma circonscription, qui s'étend du Mont Gerbier de Jonc aux gorges de l'Ardèche.

Malheureusement, la loi « Touraine » du 26 janvier 2016, votée avec la complicité des députés de la majorité de la précédente législature, a porté un très mauvais coup à l'hôpital d'Aubenas, en érigeant l'hôpital de Montélimar, dans le département voisin de la Drôme, « hôpital support » de notre groupement hospitalier de territoire. L'Ardèche, qui comprend 320 000 habitants, a ainsi le triste privilège d'être l'un des seuls départements de France dépourvu d'hôpital support, alors que la Lozère voisine, peuplée de 76 000 habitants, dispose d'un hôpital support à Mende. Au total, 135 groupements hospitaliers de territoire en France, et pas un propre au département de l'Ardèche !

Nous n'acceptons pas cette véritable mise sous tutelle, d'ailleurs unanimement dénoncée par les acteurs de santé de notre bassin de vie. En effet, la convergence annoncée des moyens vers les hôpitaux support fait courir un risque majeur d'affaiblissement du plateau technique du centre hospitalier d'Aubenas, qui pourra avoir des difficultés à recruter de nouveaux médecins. Or la question de l'attractivité médicale est une clé pour l'avenir.

Il est de ma responsabilité de vous alerter, madame la ministre. Connaissez-vous la réalité des conditions de transport et de transfert des patients dans l'un des bassins les plus enclavés de France ? Allez-vous me confirmer votre volonté de maintenir les activités actuelles du centre hospitalier d'Aubenas, sans pour autant brider le développement d'activités nouvelles, aussi bien en cancérologie que dans d'autres disciplines ?

M. le président. La parole est à Mme la ministre des solidarités et de la santé.

Mme Agnès Buzyn, ministre des solidarités et de la santé. Monsieur le député, les groupements hospitaliers de territoire ont pour objet la mise en œuvre d'une stratégie de prise en charge partagée et graduée des patients dans un territoire ou un bassin de vie, dans le but d'assurer une égalité d'accès à des soins sécurisés et de qualité, garantissant à la population une offre de proximité comme une offre de référence et de recours. Cet objectif peut conduire le groupement hospitalier de territoire à organiser la mise en commun de fonctions ou des transferts d'activités entre établissements. Une telle démarche ne doit aucunement être comprise comme une « mise sous tutelle » d'un établissement par l'établissement support.

Concernant la situation particulière du centre hospitalier d'Ardèche méridionale, la décision de constituer le groupement hospitalier de territoire dans son périmètre actuel a été prise en 2016, après concertation des acteurs du bassin de vie défini à l'époque. Le rôle de l'établissement sur son territoire et l'éventail des activités assurées ne sont nullement remis en cause dans le cadre du projet régional de santé en vigueur. Cette réflexion ne pourra être fructueuse si chaque établissement se focalise exclusivement sur le maintien de toutes ses activités propres : le positionnement des activités doit pouvoir être déterminé dans un objectif d'amélioration du service public à l'échelle du groupement et de sécurité des soins.

Les axes de travail ne sont d'ailleurs pas spécifiques à la création des groupements hospitaliers de territoire, mais peuvent avoir été définis bien antérieurement : des parcours de santé ou des parcours médicaux entre ces différents hôpitaux ont parfois été identifiés. C'est le cas notamment des coopérations en biologie entre les sites de Montélimar, Privas et Aubenas, pour lesquels des réflexions restent inabouties depuis 2014. Les discussions entre les acteurs locaux se poursuivent.

M. le président. La parole est à M. Fabrice Brun.

M. Fabrice Brun. Je vous remercie de votre réponse, madame la ministre. Nous sommes évidemment convaincus de l'intérêt de la coopération hospitalière, à la condition, toutefois, que soit garantie une base forte à Aubenas. Je me tiens à votre disposition et à celle de vos services pour trouver ensemble des solutions concrètes complémentaires pour notre bassin de santé, dont les spécificités et les particularités sont réelles. C'est en effet un des bassins les plus enclavés de France, avec des zones de montagne et de pentes isolées. De plus, le pic saisonnier y est très important, puisque le bassin passe de 100 000 habitants à l'année à 300 000 durant la période touristique. Il regroupe également la population la plus âgée de la région Auvergne-Rhône-Alpes, avec une tradition séculaire d'accueil du handicap qui fait sa fierté tout en nécessitant une offre de soins particulière.

Enfin, c'est le dernier bassin d'emplois de la région Auvergne-Rhône-Alpes. Il ne vous aura d'ailleurs pas échappé que l'hôpital d'Aubenas, avec 1 200 collaborateurs, est le premier employeur de ce bassin de vie. Je tiens, du reste, à rendre hommage à l'engagement quotidien des agents. Or le gouvernement précédent n'a pas pris en considération de nombreuses particularités de ce bassin de santé. Je souhaite que nous travaillions ensemble à ce qu'elles le soient enfin, au service de l'accès aux soins de tous les Ardéchois."""
    response_text = re.sub("\xa0", " ", response_text)
    response_text = re.sub(r"\s{2,}", " ", response_text)
    expected = {
        "id": "15-8QOSD",
        "congressman": "M. Fabrice Brun",
        "questioned_ministry": "Solidarités et santé",
        "responsible_ministry": "Solidarités et santé",
        "question_date": "05/12/2017",
        "response_date": "13/12/2017",
        "theme": "établissements de santé",
        "sub_theme": "Révision du périmètre de groupement hospitalier de territoire",
        "analysis": "",
        "question_text": """M. Fabrice Brun attire l'attention de Mme la ministre des solidarités et de la santé sur l'avenir du centre hospitalier d'Aubenas. L'égalité d'accès aux soins pour tous, en tout point du territoire, est un défi partagé. La loi n° 2016-41 du 26 janvier 2016 de modernisation de notre système de santé a créé les groupements hospitaliers de territoire (GHT), qui ont pour conséquence la mise sous tutelle des centres hospitaliers non support. Ces centres hospitaliers s'inquiètent d'une perte d'autonomie évidente et des conséquences de la convergence annoncée des moyens vers les hôpitaux supports des GHT. Tel est le cas de l'hôpital d'Aubenas puisque l'hôpital support est le centre hospitalier de Montélimar dans le département voisin de la Drôme ! Ce qui importe dans un premier temps, au regard des besoins et des attentes de la population, c'est d'une part de maintenir les activités actuelles sur le centre hospitalier d'Aubenas, et d'autre part de faire évoluer la législation sur les GHT afin de permettre aux établissements parties à un groupement qui ont la gestion d'un équipement lourd ou d'une activité spécifique de pouvoir gérer par délégation un pôle inter-établissements dans le cadre d'avenants aux conventions GHT.""",
        "response_text": response_text,
    }
    assert result == expected
