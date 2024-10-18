from models.Question import Question
from scrapers.scrape_search_tool import ScrapeSearchTool


def test_scrape_qg_10():
    result = ScrapeSearchTool.for_question_content(
        question_link="https://questions.assemblee-nationale.fr/q10/10-2052QG.htm",
        question_id="10-2052QG",
        legislature=10
    )
    expected = Question(
        id="10-2052QG",
        congressman="M. Bur Yves",
        questioned_ministry="coopération",
        responsible_ministry="coopération",
        question_date="11/12/1996",  # type: ignore
        response_date="11/12/1996",  # type: ignore
        theme="Politique exterieure",
        sub_theme="Allemagne",
        analysis="Sommet franco-allemand de Nuremberg de decembre 1996",
        question_text="""M. le president. La parole est a M. Yves Bur.\nM. Yves Bur. Ma question s'adresse a M. le Premier ministre, qui vient de participer, aux cotes du President de la Republique, au soixante-huitieme sommet franco-allemand. Ces rencontres, instituees par le general de Gaulle et le chancelier Adenauer, soulignent l'importance de l'amitie franco-allemande, qui est non seulement le vecteur de la paix et de la stabilite en Europe, mais aussi le veritable moteur de la construction europeenne. Cette rencontre a eu lieu dans un contexte economique et social difficile, en Allemagne comme en France, et a un moment crucial pour la construction europeenne.\nLe premier theme aborde touche aux problemes communs de securite interieure, qui appellent un renforcement de la cooperation policiere et judiciaire pour que nous puissions lutter ensemble et de maniere plus efficace contre le terrorisme, la grande criminalite et les trafics de drogue, en developpant notamment Europol.\nLa securite exterieure a constitue un autre theme de discussion. En effet, promouvoir une defense commune passe par un renforcement de la cooperation en matiere d'armement qui, seule, garantira l'independance de l'Europe vis-a-vis de la technologie americaine. L'approbation d'un concept franco-allemand en matiere de securite et de defense complete les avancees dans les domaines industriel et strategique, tels les satellites Helios et Horus et les helicopteres Tigre ou NH 90.\nPar ailleurs, la construction et l'approfondissement de l'Union europeenne sont au coeur des discussions franco-allemandes. MM. Chirac et Kohl ont confirme leur attachement a un euro qui ne soit pas une monnaie molle, tout en soulignant le role du pouvoir politique face aux instances monetaires.\nEnfin, une relance vigoureuse de la CIG, notamment sur le dossier institutionnel, est vivement souhaitee par nos deux pays et sera au centre des debats a Dublin.\nJe souhaiterais que la representation nationale soit eclairee sur les resultats de ce sommet, qui concerne tres directement les Francais. Quelles sont les perspectives d'une cooperation policiere et judiciaire renforcee pour assurer la securite de nos concitoyens ? Quel est le contenu des accords de cooperation pour la defense et l'armement ? Enfin, ou en sont les discussions sur les conditions de la reussite du passage a la monnaie unique, qui doit etre une chance de croissance pour les pays europeens et un espoir pour des millions de chomeurs ? (Applaudissements sur plusieurs bancs du groupe de l'Union pour la democratie francaise et du Centre.)\nM. le president. M. le Premier ministre, chacun l'aura compris, se trouve actuellement au Senat.\nLa parole est a M. le ministre delegue a la cooperation.\nM. Jacques Godfrain, ministre delegue a la cooperation. Monsieur le depute, c'est en lieu et place de M. le ministre des affaires etrangeres que je repondrai a votre question.\nLes soixante-huitiemes consultations franco-allemandes, qui se sont tenues hier a Nuremberg, se sont d'ores et deja traduites par un bilan tres positif: lettre commune franco-allemande sur la reforme de l'Union europeenne; preparation en commun du prochain Conseil europeen, qui se tiendra vendredi et samedi a Dublin; adoption d'un concept commun en matiere de securite et de defense, qualifie d'historique par le President de la Republique.\nS'agissant d'abord de la conference intergouvernementale, ce sommet a donc ete marque par l'adoption d'une lettre commune du President de la Republique et du chancelier Kohl a la presidence irlandaise du Conseil europeen. Cette initiative illustre la determination de nos deux pays a presenter des positions communes sur les principaux points en negociation. Elle devrait faire progresser les discussions au sein de la CIG.\nPour ce qui est de l'Union economique et monetaire, des progres significatifs ont ete accomplis dans la preparation de l'entree en vigueur de la monnaie unique. Les efforts se poursuivent pour finaliser un accord sur le pacte de stabilite, qui doit etre, selon nous, un pacte de stabilite, et de croissance.\nEn ce qui concerne la preparation du prochain elargissement de l'Union europeenne aux pays d'Europe centrale et orientale, le projet francais de conference europeenne a ete evoque avec beaucoup d'interet dans la perspective de la prochaine reunion ministerielle, dite du «Triangle de Weimar», qui reunira les ministres des affaires etrangeres francais, allemand et polonais le 19 decembre prochain, a Varsovie.\nA propos des questions strategiques, nous nous sommes mis d'accord sur un concept commun en matiere de defense et de securite, qui inclut des directives concretes pour la future cooperation dans les domaines militaire et de l'armement. Ce document sera presente au Parlement avant d'etre rendu public.\nNous avons egalement reaffirme l'importance que nous attachons au developpement en commun d'un systeme de reconnaissance spatiale comprenant les satellites Helios II et Horus.\nM. Didier Boulaud. Ce n'est pas vrai !\nM. le ministre delegue a la cooperation. C'est vrai puisque ce programme est deja lance. (Exclamations sur les bancs du groupe socialiste.) Si l'Allemagne, pour des raisons budgetaires, en retarde quelque peu la realisation, la France, quant a elle, s'y engage des maintenant. («Tres bien !» sur les bancs du groupe du Rassemblement pour la Republique et du groupe de l'Union pour la democratie francaise et du Centre.)\nPar ailleurs, les questions bilaterales n'ont pas ete oubliees puisqu'elles donneront lieu a une concertation diplomatique entre nos deux pays.\nEnfin, nos preoccupations communes relatives a l'emploi se sont traduites par un accord sur la reconnaissance mutuelle des brevets de maitrise de l'artisanat (Applaudissements sur divers bancs du groupe du Rassemblement pour la Republique.)""",
        response_text=""
    )
    assert result.id == expected.id


def test_scrape_qe_14():
    result = ScrapeSearchTool.for_question_content(
        question_link="https://questions.assemblee-nationale.fr/q14/14-103711QE.htm",
        question_id="14-103711QE",
        legislature=14
    )
    expected = Question(
        id="14-103711QE",
        congressman="M. Olivier Audibert Troin",
        questioned_ministry="Défense",
        responsible_ministry="Défense",
        question_date="04/04/2017",  # type: ignore
        response_date="09/05/2017",  # type: ignore
        theme="impôts locaux",
        sub_theme="versement transport",
        analysis="assujettissement. armée. réglementation.",
        question_text="""M. Olivier Audibert Troin attire l'attention de M. le ministre de la défense sur la problématique de la mise en œuvre du droit de communication des données susceptibles de permettre aux autorités organisatrices des mobilités (AOM) de déterminer le montant de l'imposition du « versement transport ». Les AOM qui organisent les transports urbains peuvent en effet demander le versement d'une taxe « transport » aux entreprises de plus de 11 employés implantées sur leurs territoires. Le montant de cette taxe résulte de l'application d'un pourcentage sur la masse salariale de l'ensemble de l'effectif employé par cette entité, qu'elle soit publique ou privée. Par principe, ces entités versent cette taxe dans son intégralité, puis sont remboursées par l'AOM sur la fraction correspondant aux employés logés en permanence ou transportés par un service propre. Pour le personnel civil et militaire de l'armée, une double dérogation était consentie jusqu'alors, permettant d'une part le calcul du versement transport sur la base d'effectifs moyens et non pas réels, et d'autre part un décompte préalable de l'assiette de calcul, de la masse salariale des personnels logés/transportés, appelé précompte. Or depuis la loi de finances rectificative de 2014, de nouvelles règles ont été introduites permettant d'entériner la règle du précompte, mais rendant illégale celle du calcul sur la base d'effectifs moyens. Depuis cette date, de nombreuses communautés demandent aux bases de défense la communication du détail des calculs du versement transport. L'objectif visé par ces démarches est à la fois de récupérer le manque à gagner résultant du paiement sur la base de l'effectif moyen, de vérifier l'écart réel entre le volume de militaires servant au calcul et les effectifs réels, de s'assurer que le paiement actuel du versement transports soit bien assis sur l'effectif réel et enfin de vérifier le calcul des effectifs logés/transportés par rapport à l'effectif total. Il lui demande en conséquence une analyse tendant à justifier le détail des calculs du versement transport et lever ainsi l'opacité ressentie qui affecte sensiblement le budget des collectivités concernées.""",
        response_text="""Aux termes des articles L. 2333-64 et L. 2531-2 et suivants du code général des collectivités territoriales, la contribution dite « versement transport » constitue la participation des personnes publiques ou privées employant au moins 11 salariés au financement des transports en commun. Elle est perçue par les organismes ou services chargés du recouvrement des cotisations de sécurité sociale et des allocations familiales pour être reversée aux autorités organisatrices de mobilité (AOM). Conformément à la réglementation en vigueur, les versements effectués à ce titre par le ministère de la défense ne sont pas calculés sur la base d'effectifs moyens, mais prennent en compte la réalité des rémunérations servies aux personnels employés sur le périmètre géographique des AOM, l'assiette du versement transport étant constituée par ces rémunérations. Le calcul des sommes versées aux URSAFF est automatisé et effectué par les calculateurs de solde sur la base des informations transmises par les systèmes d'information de ressources humaines. Dans l'hypothèse où des difficultés en la matière viendraient à être détectées, les services du ministère ne manqueraient pas de corriger les éventuels dysfonctionnements. Enfin, il est précisé que dans la perspective du prochain déploiement du calculateur de solde ministériel « Source Solde », le ministère de la défense a constitué un groupe de travail afin, notamment, d'expertiser les processus existants. Ces travaux, qui visent en particulier à vérifier la bonne prise en compte par le ministère des déductions légales concernant les personnels logés et transportés, devraient aboutir au cours de l'année 2017."""
    )
    assert result == expected


def test_scrape_qe_15():
    result = ScrapeSearchTool.for_question_content(
        question_link="https://questions.assemblee-nationale.fr/q15/15-45066QE.htm",
        question_id="15-45066QE",
        legislature=15
    )
    expected = Question(
        id="15-45066QE",
        congressman="M. Patrick Hetzel",
        questioned_ministry="Solidarités et santé",
        responsible_ministry="Santé et prévention",
        question_date="29/03/2022",  # type: ignore
        response_date="",  # type: ignore
        theme="professions de santé",
        sub_theme="Hausse du carburant pour les professionnels de l'aide aux personnes âgées",
        analysis="",
        question_text="""M. Patrick Hetzel alerte M. le ministre des solidarités et de la santé sur les nouvelles difficultés liées à la hausse du carburant pour les professionnels de l'aide aux personnes âgées. En effet, au-delà de la crise structurelle qui touche les professionnels du domicile et des établissements pour personnes âgées, ceux-ci ont dû faire face à la gestion de la crise sanitaire sans que leur condition de travail ne se soient améliorées en sortie de crise. Les dépenses qui augmentent dans les établissements ne sont pas compensés par des hausses de budget et peuvent conduire ces établissements à faire des économies sur d'autres postes. Par ailleurs, les professionnels de l'aide à domicile ont des frais d'essence qui ont explosés alors qu'ils ne sont remboursés que via les frais kilométriques à des montants qui ne sont pas augmentés et bien insuffisants (0,35 euro/kilomètre). C'est donc à présent la hausse du carburant qui touche directement ces professionnels dont les salaires font partie des plus bas de la Nation. À ce stade, aucune réponse ciblée des pouvoirs publics n'a été apportée à cette problématique de fond qui touche au budget des professionnels et des structures. Tout le monde mesure combien la France a besoin de ces professionnels notamment en tant de crise car ce secteur de l'aide aux personnes âgées est source de cohésion sociale. M. le député souhaite donc savoir ce que l'État compte faire pour se saisir de cette question essentielle pour la profession.""",
        response_text=""
    )
    assert result == expected
