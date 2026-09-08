# Mesure du KR2.3 — Taux de réussite du parcours « comprendre la procédure »

Rattachement OKR : **Objectif 2 (Sensibilisation)** — *Protect'Envi permet aux collectivités de
connaître les moyens d'action contre les dépôts sauvages.*

Ce document décrit la définition retenue pour le KR2.3, les événements Matomo émis par le site, et
la configuration à réaliser dans l'interface Matomo pour obtenir le chiffre.

## 1. Ce que le KR mesure

La cible est un agent ou un élu qui **n'a pas forcément un dépôt à traiter tout de suite** : il se
renseigne, prépare sa commune, veut savoir de quels moyens il dispose. Le parcours réussit donc s'il
repart avec la procédure en tête ou engagé dans un accompagnement — pas nécessairement s'il démarre
une constatation.

**Formule**

```
Taux de réussite = visites ayant atteint une « issue de valeur » ÷ visites entrées dans le parcours
```

| Terme | Définition |
| --- | --- |
| **Entrée dans le parcours** (dénominateur) | Visite ayant consulté `/comment-agir` ou `/comprendre-la-procedure` |
| **Issue de valeur** (numérateur) | Visite ayant réalisé **au moins une** des actions ci-dessous |
| → *Comprendre* | Lecture aboutie : avoir atteint 75 % de la page `/comprendre-la-procedure` |
| → *Se former* | Clic « Je m'inscris au webinaire » **ou** envoi du formulaire « Je souhaite être informé » |
| → *Agir* | Clic vers le démarrage d'une constatation depuis le parcours |

Une visite qui cumule plusieurs issues n'est comptée **qu'une seule fois** (voir §4, réglage des
objectifs Matomo).

### Indicateurs d'accompagnement (à lire systématiquement avec le KR)

- **Clarté perçue** — micro-sondage de fin de page : % de « Oui » parmi les répondants. Sert de
  contrôle qualité : si le taux de réussite progresse sans que la clarté perçue suive, on optimise
  de l'engagement, pas de la compréhension.
- **Volume d'entrées dans le parcours** — sans lui un pourcentage n'est pas interprétable.

### Choix de conception

- **Profondeur de lecture plutôt que temps passé.** Matomo calcule le temps d'une page par
  différence avec la page suivante : la **dernière page d'une visite compte 0 seconde**. C'est
  exactement le cas de quelqu'un qui lit puis quitte le site — le comportement qu'on veut valoriser
  serait systématiquement compté comme un échec. Le scroll n'a pas ce biais.
- **Le sondage n'entre pas dans le numérateur.** Il est répondu par une minorité auto-sélectionnée ;
  l'inclure gonflerait le taux sans le fiabiliser.
- **L'inscription au webinaire n'est mesurable que jusqu'au clic**, l'inscription se faisant sur
  RDV Service public (site externe). Le formulaire « être informé » est, lui, mesuré à l'envoi.

## 2. Événements émis par le site

Tous les événements utilisent la catégorie **`Parcours information`**.

| Action | Nom (name) | Émis quand |
| --- | --- | --- |
| `Entrée parcours` | Nom de la page | Affichage de `/comment-agir` ou `/comprendre-la-procedure` |
| `Lecture 25%` / `50%` / `75%` / `100%` | Nom de la page | Palier de lecture atteint (une fois par visite) |
| `Sortie - Guide complet` | `Comment agir` | Clic vers `/comprendre-la-procedure` |
| `Sortie - Webinaire` | Nom de la page | Clic vers la page webinaire |
| `Sortie - Inscription webinaire` | `Prendre rendez-vous` | Clic vers RDV Service public (départ du site) |
| `Sortie - Être informé` | Nom de la page | Envoi du formulaire Tally « être informé » |
| `Sortie - Constatation` | `Comprendre la procédure` | Clic vers le démarrage d'une constatation |
| `Sortie - FAQ` | Nom de la page | Clic vers la FAQ |
| `Clarté - Oui` / `En partie` / `Non` | Nom de la page | Réponse au micro-sondage |
| `Clarté - Rebond Webinaire` / `Rebond Contact` | Nom de la page | Rattrapage proposé après une réponse négative |
| `Ouverture accordéon` | `Comprendre la procédure - <clé>` | Dépliage d'un accordéon |

Noms de page utilisés : `Comment agir`, `Comprendre la procédure`, `Prendre rendez-vous`.

Implémentation : [`frontend/composables/useScrollDepth.ts`](../frontend/composables/useScrollDepth.ts)
et [`frontend/components/shared/ClarteFeedback.vue`](../frontend/components/shared/ClarteFeedback.vue).

## 3. Prérequis

Le suivi ne fonctionne qu'avec les variables d'environnement Matomo renseignées :

```
VITE_MATOMO_ENABLED=true
VITE_MATOMO_HOST=https://stats.beta.gouv.fr
VITE_MATOMO_SITE_ID=<id du site>
```

Le tracking est **sans cookie** (`disableCookies`) : aucun bandeau de consentement n'est requis.

## 4. Configuration à faire dans Matomo

Dans **Objectifs → Gérer les objectifs → Ajouter un objectif**, créer les deux objectifs suivants.

Pour chacun : *L'objectif est converti quand le visiteur* → **déclenche un événement**, et laisser
**« Autoriser plusieurs conversions par visite » sur NON** — c'est ce réglage qui garantit qu'une
visite n'est comptée qu'une fois.

### Objectif A — `KR2.3 · Entrée parcours` (dénominateur)

- Condition : **Action de l'événement** — *est exactement* — `Entrée parcours`

### Objectif B — `KR2.3 · Issue de valeur` (numérateur)

- Condition : **Action de l'événement** — *correspond à l'expression régulière* :

```
^(Lecture 75%|Sortie - (Inscription webinaire|Être informé|Constatation))$
```

Un seul objectif couvre les trois issues : une visite qui en cumule plusieurs n'est donc comptée
qu'une fois, ce qui est exactement la définition du numérateur.

> Si la version de Matomo permet d'ajouter une seconde condition, ajouter **Catégorie de
> l'événement — est exactement — `Parcours information`** sur les deux objectifs. Ce n'est pas
> indispensable aujourd'hui (aucune autre page n'émet ces actions) mais protège d'une réutilisation
> future du composant de mesure ailleurs sur le site.

### Lecture du résultat

**KR2.3 = conversions de l'objectif B ÷ conversions de l'objectif A**, sur la période retenue
(Objectifs → vue d'ensemble).

### Segment utile

Créer un segment **« Parcours information »** (*Catégorie de l'événement est exactement
`Parcours information`*) pour analyser ce public à part : origine du trafic, type de collectivité,
pages vues ensuite.

### Suivi des indicateurs d'accompagnement

- **Clarté perçue** : Comportement → Événements → catégorie `Parcours information`. Comparer les
  actions `Clarté - Oui`, `Clarté - En partie`, `Clarté - Non`.
- **Décrochage dans la page** : comparer les volumes `Lecture 25%` → `50%` → `75%` → `100%` pour
  situer l'endroit où la lecture s'arrête.

## 5. Cible

**À ne pas fixer avant d'avoir une ligne de base.** Relever le taux sur le premier mois complet de
collecte, puis fixer la cible du trimestre à partir de cette valeur observée.

## 6. Limite connue

`/comprendre-la-procedure` n'est **pas dans le menu principal** : on n'y accède que depuis
`/comment-agir`, un lien du formulaire de constatation et le plan du site. Le volume d'entrées sur
la partie « lecture aboutie » du parcours en dépend directement. Si les entrées sont trop faibles
pour que le KR soit significatif, c'est l'exposition de la page qu'il faut traiter en premier — pas
la définition du KR.
