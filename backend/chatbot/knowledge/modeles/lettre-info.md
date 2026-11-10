# Modèle officiel : LETTRE-INFO
> Source : `lettre-info.odt` (modèle de document généré par Stop Dépôt Sauvage)

LETTRE D’INFORMATION

RELATIVE A UN DEPÔT SAUVAGE

{% if auteur_identifie %}

{%- if statut_auteur == 'entreprise' -%}

{{ auteur_nom }}

{%- else -%}

{{ auteur_nom_complet }}

{% endif %}

{{ auteur_adresse_l1 }}

{{ auteur_adresse_l2 }}

{% endif %}

Fait à {{ commune }}, le {{ date_courante }}

Commune de {{ commune }}

{% if auteur_civilite == 'M' -%}

Monsieur,

{%- elif auteur_civilite == 'Mme' -%}

Madame,

{%- else -%}

Madame, Monsieur,

{%- endif %}

Vu le rapport de constatation en date du {{ date_courante }}, un dépôt sauvage a été constaté à {{ localisation_depot }}le {{ date_constat }}à {{ heure_constat }}.

{% if types_depot %}Il s’agit d’un ensemble de : {% for type in types_depot %}{{ type }}{% if not loop.last %}, {% endif %}{% endfor %}.{% endif %}

Le volume approximatif est : {{ volume_depot }}.

Au vu des constatations, il semblerait que vous soyez responsable de ce dépôt sauvage en qualité de producteur ou détenteur de ces déchets au sens de l’article L. 541-1-1 du Code de l’environnement.

Je vous rappelle que les dépôts sauvages de déchets et d’encombrants sont interdits sur l’ensemble des voies, espaces publics et privés de la commune et que ce faisant, vous portez atteinte à l’environnement et à la santé publique, et êtes tenu d’en assurer l’élimination.

{% if souhaite_porter_plainte %}

Je vous informe qu’une plainte pénale a également été déposée auprès de la brigade de gendarmerie.

{% endif %}

En tant que titulaire du pouvoir de police spéciale de gestion des dépôts sauvages de déchets je vous informe que j’envisage d’appliquer les dispositions de l’article L. 541-3 du Code de l’environnement.

Par la présente, je vous informe donc qu’en considération du dépôt sauvage de déchets susvisé dont vous êtes détenteur ou producteur, vous encourez les sanctions listées à l’article L.541-3 du Code de l’environnement :

Une première amende d’un montant maximal de 15 000 euros à l’issue de la procédure contradictoire préalable décrite ci-après ;

Une mise en demeure d’effectuer les diligences nécessaires dans un délai imparti. À défaut d’accomplissement de ces mesures dans le délai indiqué, d’autres sanctions bien plus lourdes pourront être appliquées (listées au 1°, 2°, 3°, 4° et 5° du I de l’article L.541-3 du Code de l’environnement). Ces sanctions, qui peuvent être cumulatives, pourront être les suivantes :

Obligation de consignation d’une somme d’argent aux fins d’accomplissement des mesures prescrites ;

Exécution d’office des mesures, par Monsieur le Maire en tant que titulaire du pouvoir de police spéciale, afin de remédier au dépôt sauvage de déchets en usant des sommes consignées le cas échéant ;

Suspension du fonctionnement de l’installation et de l’ouvrage, de tous travaux, opérations ou encore de tout exercice de l’activité à l’origine des infractions jusqu’à exécution complète des mesures prescrites ;

Une astreinte journalière au plus égale à 1 500 euros courant à compter d’une date fixée et jusqu’à accomplissement des mesures prescrites ;

Une amende d’un montant de 150 000 euros au maximum.

Cela étant, avant toute suite de la procédure et en application du principe du contradictoire, vous avez la possibilité de me faire parvenir toute observation orale ou écrite dans un délai de 10 jours. Le cas échéant, vous pouvez être assisté d’un conseil ou être représenté par le mandataire de votre choix.

Sachez que mon souhait n’est aucunement d’en arriver à de pareilles sanctions. Toutefois en tant que Maire de {{ commune }}, j’ai le devoir de garantir la sécurité et la salubrité sur le territoire de la commune.

Comme mentionné supra, à l’issue de la phase de procédure contradictoire et sauf éléments de fait remettant en cause votre responsabilité, je me réserve le droit de faire application des dispositions de l’article L.541-3 du Code de l’environnement et ainsi vous adresser une première amende administrative. Le montant sera déterminé en fonction de la gravité des faits dans la limite de 15 000 euros.

Je vous prie de bien vouloir recevoir l'expression de mes salutations distinguées.

Signature et tampon de l’autorité compétente
