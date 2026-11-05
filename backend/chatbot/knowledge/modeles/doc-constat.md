# Modèle officiel : DOC-CONSTAT
> Source : `doc-constat.odt` (modèle de document généré par Stop Dépôt Sauvage)

RAPPORT DE CONSTATATION

DEPOT SAUVAGE DE DECHETS

{{ date_courante }}

Mairie de {{ commune }}

OBJET : Rapport de constatation en matière de gestion de déchets en date du {{ date_constat }}.

CONSTATATIONS

Nous, {{ constatant_nom_complet }},{%- if constatant_role %} en qualité {{ "d'" if constatant_role_needs_elision else "de " }}{{ constatant_role }},{% endif -%}

Rapportons les constatations suivantes :

Le {{ date_constat }}à {{ heure_constat }}à {{ localisation_depot }}({{ commune }}), un dépôt sauvage est présent.

Le volume estimé est : {{ volume_depot }}

{% if types_depot %}

Le dépôt se compose des éléments suivants :

{%- for item in types_depot -%}

{{ item }}

{%- endfor -%}

{%- endif -%}

{%- if nature_terrain -%}

{%- if nature_terrain | length > 1 -%}

Ce dépôt se trouve dans les terrains suivants :

{%- for item in nature_terrain -%}

{%- if item == "je ne sais pas" -%}

Terrain de nature inconnue

{%- else -%}

{{ item }}

{%- endif -%}

{%- endfor -%}

{%- endif -%}

{%- if nature_terrain | length == 1 -%}

{% set item = nature_terrain[0] %}

{%- if item == "forêt domaniale" -%}

Ce dépôt se trouve dans une forêt domaniale.

{%- endif -%}

{%- if item == "terrain privé" -%}

Ce dépôt se trouve sur un terrain privé.

{%- endif -%}

{%- if item == "terrain public" -%}

Ce dépôt se trouve sur un terrain public.

{%- endif -%}

{%- if item == "je ne sais pas" -%}

Ce dépôt se trouve sur un terrain de nature inconnue.

{%- endif -%}

{%- endif -%}

{%- endif -%}

{%- if "terrain privé" in nature_terrain -%}

Le dépôt sauvage constaté présente une atteinte à la salubrité ou la sécurité publique, telles que définies à l’article L. 2212-2 du Code général des collectivités territoriales (notamment : risque de pollution de toute nature et/ou risque d’incendie). À ce titre, le pouvoir de police municipale s’applique même sur une propriété privée et permet de prendre des mesures pour prévenir ces atteintes.

{%- endif -%}

{%- if photo_dispo -%}

Les éventuelles photographies sont jointes en annexe du présent rapport.

{%- endif -%}

{%- if precisions_depot -%}

Les observations suivantes ont été apportées :

{{ precisions_depot }}

{%- endif -%}

{%- if indices_disponibles -%}

Les éléments suivants pourraient permettre d’identifier l’auteur des faits :

{% for item in indices_disponibles %}

{{ item }}

{% endfor %}

{% endif %}

{% if auteur_identifie %}

L’auteur présumé des faits est :

{%- if statut_auteur == 'entreprise' -%}

{{ auteur_nom }}

{%- if auteur_siret -%}

(SIRET : {{ auteur_siret }})

{%- endif -%}

{%- else -%}

{{ auteur_nom_complet }}

{%- endif -%}

Adresse :

{{ auteur_adresse }}

{%- endif -%}

{% if precisions_indices %}

Les précisions suivantes ont été apportées :

{{ precisions_indices }}

{%- endif -%}

{%- if not auteur_identifie and souhaite_porter_plainte -%}

PRÉJUDICE

{%- if prejudice_montant_connu -%}

Le préjudice financier pour la commune est estimé à {{ prejudice_montant }} €.

{%- endif -%}

{%- if not prejudice_montant_connu -%}

Une estimation du montant du préjudice a été établie.

Nombre de personnes mobilisées : {{ prejudice_nombre_personnes }}

Nombre d’heures mobilisées : {{ prejudice_nombre_heures }}

Nombre de véhicules mobilisés : {{ prejudice_nombre_vehicules }}

Kilométrage parcouru par véhicule : {{ prejudice_kilometrage }}

Autres coûts : {{ prejudice_autres_couts }} €

En considérant les estimations suivantes :

Taux horaire par agent : 18,03 €/h

Coût d’usage par véhicule : 1,30 €/km

Le préjudice financier pour la commune est estimé à {{ prejudice_montant_calcule }} €

{%- endif -%}

{%- if souhaite_porter_plainte -%}

Une plainte au nom de la commune de {{ commune }}sera déposée pour les faits constatés.

{%- endif -%}

{%- endif -%}

DESTINATAIRES

Archives de {{ commune }}.

Rapport fait et clos

à {{ commune }}le {{ date_courante }}

Par {{ constatant_nom|upper }}{{ constatant_prenom|capitalize }}

{{ constatant_role|capitalize }}

Signature et tampon

{%- if photos -%}

ANNEXES - Photographies

{%- for photo in photos -%}

{%- endfor -%}

{%- endif -%}
