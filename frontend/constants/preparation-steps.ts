export interface PreparationLink {
  label: string
  to?: string
  href?: string
  action?: 'simulator'
}

export interface PreparationStep {
  id: string
  label: string
  description?: string
  link: PreparationLink
}

export interface PreparationNote {
  text: string
  link: PreparationLink
}

export interface PreparationSection {
  id: string
  title: string
  icon: string
  steps: PreparationStep[]
  notes?: PreparationNote[]
}

// Resources to fill in before or after going live (Trello 998). A step whose resource is null is hidden.
export const PENDING_RESOURCES: Record<string, string | null> = {
  guideUtilisation: null,
}

const faq = (slug: string) => `/faq/${slug}`
const blog = (slug: string) => `/blog/${slug}`

const guideStep: PreparationStep[] = PENDING_RESOURCES.guideUtilisation
  ? [
      {
        id: 'guide',
        label: "Je consulte le guide d'utilisation",
        description: "Toutes les étapes de l'outil, de la constatation à la sanction.",
        link: { label: "Ouvrir le guide d'utilisation", href: PENDING_RESOURCES.guideUtilisation },
      },
    ]
  : []

export const PREPARATION_SECTIONS: PreparationSection[] = [
  {
    id: 'prevenir-anticiper',
    title: 'Prévenir et anticiper les dépôts sauvages',
    icon: 'fr-icon-book-2-line',
    steps: [
      ...guideStep,
      {
        id: 'webinaire',
        label: 'Je participe au webinaire',
        description:
          'En moins de 60 minutes, découvrez comment agir concrètement grâce à la procédure administrative.',
        link: { label: "S'inscrire au prochain webinaire", to: '/rdv' },
      },
      {
        id: 'retours-experience',
        label:
          "Je parcours les retours d'expériences d'autres communes qui ont utilisé Stop Dépôt Sauvage",
        description: 'Utile aussi pour présenter la démarche à vos élus.',
        link: {
          label: 'Comment une commune a traité son premier dossier',
          to: blog('comment-une-commune-a-traite-son-premier-dossier-sur-protectenvi'),
        },
      },
      {
        id: 'prevention',
        label: 'Je parcours les bonnes pratiques pour prévenir les dépôts',
        description: 'Panneaux, aménagement, communication auprès des habitants.',
        link: {
          label: 'Plan de lutte contre les dépôts sauvages : comment l’organiser',
          to: blog('plan-de-lutte-contre-les-depots-sauvages-5-volets'),
        },
      },
    ],
  },
  {
    id: 'jour-j',
    title: 'Être prêt le jour J',
    icon: 'fr-icon-flashlight-line',
    steps: [
      {
        id: 'bons-reflexes',
        label: 'Je découvre les bons réflexes face à un dépôt sauvage',
        description: 'Les 3 étapes à suivre quand un dépôt est découvert sur votre territoire.',
        link: {
          label: 'Dépôt sauvage : plan d’action en 3 étapes pour les communes',
          to: blog('depot-sauvage-plan-daction-en-3-etapes-pour-les-communes'),
        },
      },
      {
        id: 'identifier-auteur',
        label: "Je consulte les bonnes pratiques pour identifier l'auteur d'un dépôt sauvage",
        description:
          'Indices trouvés dans le dépôt, vidéoprotection, plaque d’immatriculation, témoignages : ce qui est possible et dans quel cadre.',
        link: {
          label: 'Identifier l’auteur d’un dépôt sauvage : indices, plaque, vidéo',
          to: blog('identifier-lauteur-dun-depot-sauvage-indices-plaque-video'),
        },
      },
      {
        id: 'enlever-depot',
        label: 'Je vérifie si je peux enlever un dépôt sans attendre',
        link: {
          label: 'Dépôt sauvage : faut-il attendre 10 jours avant de l’enlever ?',
          to: blog('depot-sauvage-faut-il-attendre-10-jours-avant-de-lenlever'),
        },
      },
      {
        id: 'simulateur',
        label:
          'En cas de doute, je vérifie mon éligibilité à la procédure administrative avec le simulateur',
        link: { label: "Ouvrir le simulateur d'éligibilité", action: 'simulator' },
      },
    ],
    notes: [
      {
        text: "Pas besoin de délibération du conseil municipal ni d'arrêté préalable pour initier une procédure « dépôt sauvage » : celle-ci relève du pouvoir de police administrative du maire.",
        link: {
          label: 'En savoir plus sur la délibération',
          to: faq(
            'faut-il-une-deliberation-du-conseil-municipal-pour-demarrer-une-procedure-administrative'
          ),
        },
      },
      {
        text: 'Stop Dépôt Sauvage peut être utilisé partout, en zone Police nationale comme en zone Gendarmerie.',
        link: {
          label: 'En savoir plus sur les zones police et gendarmerie',
          to: faq('puis-je-utiliser-protectenvi-si-ma-commune-est-en-zone-police-nationale'),
        },
      },
      {
        text: 'Une autre question ?',
        link: { label: 'Consulter la FAQ', to: '/faq' },
      },
    ],
  },
  {
    id: 'organisation',
    title: 'Identifier qui peut agir dans la collectivité',
    icon: 'fr-icon-team-line',
    steps: [
      {
        id: 'habilites-constater',
        label: "J'identifie les personnes habilitées à constater un dépôt sauvage",
        description:
          'Le maire, ses adjoints, le garde champêtre et les policiers municipaux peuvent constater sans habilitation supplémentaire. Tout autre agent doit être commissionné par arrêté du maire.',
        link: {
          label: 'Qui peut constater un dépôt sauvage ?',
          to: faq('qui-peut-constater-un-depot-sauvage'),
        },
      },
      {
        id: 'habilites-procedure',
        label: "J'identifie les personnes habilitées à lancer une procédure",
        description:
          "Le maire, ou ses adjoints par délégation. Dans une intercommunalité, le président de l'EPCI si les maires lui ont transféré ce pouvoir.",
        link: {
          label: 'Qui peut engager la procédure administrative ?',
          to: faq('qui-peut-engager-la-procedure-administrative'),
        },
      },
    ],
  },
]
