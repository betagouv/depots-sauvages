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
  links: PreparationLink[]
  // Resources not published yet: shown as "Bientôt disponible" until a URL is set.
  upcoming?: string[]
}

export interface PreparationSection {
  id: string
  title: string
  icon: string
  steps: PreparationStep[]
}

// Resources to fill in before going live (Trello 998). Leave null to show "Bientôt disponible".
export const PENDING_RESOURCES: Record<string, string | null> = {
  temoignagesAudio: null,
  replayWebinaire: null,
  arreteTypePrevention: null,
  guideUtilisation: null,
}

const faq = (slug: string) => `/faq/${slug}`
const blog = (slug: string) => `/blog/${slug}`

export const PREPARATION_SECTIONS: PreparationSection[] = [
  {
    id: 'organisation',
    title: "Plus d'info sur mon organisation",
    icon: 'fr-icon-team-line',
    steps: [
      {
        id: 'habilites-constater',
        label: "J'identifie les personnes habilitées à constater un dépôt sauvage",
        description:
          'Le maire et ses adjoints, le garde champêtre et les agents de police municipale peuvent constater sans habilitation supplémentaire. Tout autre agent (service technique, DGS, ASVP…) doit être commissionné par arrêté du maire.',
        links: [
          {
            label: 'Qui peut constater un dépôt sauvage ?',
            to: faq('qui-peut-constater-un-depot-sauvage'),
          },
          { label: 'Comment commissionner un agent ?', to: faq('comment-commissionner-un-agent') },
        ],
      },
      {
        id: 'habilites-procedure',
        label: "J'identifie les personnes habilitées à lancer une procédure",
        description:
          "Le maire, ou ses adjoints par délégation. Le président d'un EPCI compétent en collecte des déchets ménagers, lorsque les maires lui ont transféré leurs prérogatives.",
        links: [
          {
            label: 'Qui peut engager la procédure administrative ?',
            to: faq('qui-peut-engager-la-procedure-administrative'),
          },
        ],
      },
    ],
  },
  {
    id: 'questions-frequentes',
    title: 'Consulter les questions les plus fréquentes',
    icon: 'fr-icon-question-line',
    steps: [
      {
        id: 'deliberation',
        label:
          "Est-ce que j'ai besoin d'une délibération ou d'un arrêté pour mettre en œuvre la procédure administrative ?",
        description:
          "Non. La procédure relève du pouvoir de police administrative du maire : aucune délibération du conseil municipal n'est nécessaire, ni pour l'engager, ni pour prononcer l'amende. Aucun arrêté préalable n'est non plus requis : seul l'arrêté prononçant l'amende à l'encontre de l'auteur est nécessaire.",
        links: [
          {
            label: 'Lire la réponse complète',
            to: faq(
              'faut-il-une-deliberation-du-conseil-municipal-pour-demarrer-une-procedure-administrative'
            ),
          },
        ],
      },
      {
        id: 'zone-police',
        label:
          'Zone police ou gendarmerie : est-ce que je peux utiliser Stop Dépôt Sauvage partout ?',
        description:
          "Oui. Stop Dépôt Sauvage peut être utilisé par toutes les communes, qu'elles soient en zone Police nationale ou en zone Gendarmerie. La procédure administrative relève des pouvoirs du maire et n'est pas liée au zonage des forces de sécurité.",
        links: [
          {
            label: 'Lire la réponse complète',
            to: faq('puis-je-utiliser-protectenvi-si-ma-commune-est-en-zone-police-nationale'),
          },
        ],
      },
      {
        id: 'faq',
        label: 'Je consulte la FAQ pour répondre à toutes mes questions',
        links: [{ label: 'Consulter la FAQ', to: '/faq' }],
      },
    ],
  },
  {
    id: 'eligibilite',
    title: 'Vérifier mon éligibilité',
    icon: 'fr-icon-checkbox-circle-line',
    steps: [
      {
        id: 'simulateur',
        label:
          'En cas de doute, je vérifie mon éligibilité à la procédure administrative avec le simulateur',
        links: [{ label: "Ouvrir le simulateur d'éligibilité", action: 'simulator' }],
      },
    ],
  },
  {
    id: 'identifier-auteur',
    title: "Identifier l'auteur",
    icon: 'fr-icon-search-line',
    steps: [
      {
        id: 'bonnes-pratiques-identification',
        label: "Je consulte les bonnes pratiques pour identifier l'auteur d'un dépôt sauvage",
        description:
          "Indices trouvés dans le dépôt, vidéoprotection, plaque d'immatriculation, témoignages : ce qui est possible et dans quel cadre.",
        links: [
          {
            label: "Identifier l'auteur d'un dépôt sauvage : indices, plaque, vidéo",
            to: blog('identifier-lauteur-dun-depot-sauvage-indices-plaque-video'),
          },
          { label: "Comment identifier l'auteur ?", to: faq('comment-identifier-lauteur') },
          {
            label: 'Peut-on utiliser des caméras de chasse ?',
            to: faq('peut-on-utiliser-des-cameras-de-chasse'),
          },
          {
            label: 'La police municipale peut-elle identifier un véhicule ?',
            to: faq('la-police-municipale-peutelle-identifier-un-vehicule'),
          },
        ],
      },
    ],
  },
  {
    id: 'retours-experience',
    title: "S'inspirer d'autres communes",
    icon: 'fr-icon-chat-quote-line',
    steps: [
      {
        id: 'retours-experience',
        label:
          "Je parcours les retours d'expériences d'autres communes qui ont utilisé Stop Dépôt Sauvage",
        description: 'Utile aussi pour présenter la démarche à vos élus.',
        links: [
          {
            label: 'Comment une commune a traité son premier dossier',
            to: blog('comment-une-commune-a-traite-son-premier-dossier-sur-protectenvi'),
          },
          {
            label: "Le retour d'expérience des Salles-du-Gardon",
            to: blog('depots-dencombrants-le-retour-dexperience-des-salles-du-gardon'),
          },
          {
            label: 'Strasbourg : sensibiliser, prévenir, verbaliser',
            to: blog('strasbourg-contre-les-depots-sauvages-sensibiliser-prevenir-verbaliser'),
          },
          ...(PENDING_RESOURCES.temoignagesAudio
            ? [
                {
                  label: 'Écouter les témoignages de communes',
                  href: PENDING_RESOURCES.temoignagesAudio,
                },
              ]
            : []),
        ],
        upcoming: PENDING_RESOURCES.temoignagesAudio ? [] : ['Témoignages audio de communes'],
      },
    ],
  },
  {
    id: 'webinaire',
    title: 'Participer au webinaire',
    icon: 'fr-icon-video-chat-line',
    steps: [
      {
        id: 'webinaire',
        label: 'Je participe au webinaire',
        description:
          'En moins de 60 minutes, découvrir comment agir concrètement contre les dépôts sauvages grâce à la procédure administrative.',
        links: [
          { label: "S'inscrire au prochain webinaire", to: '/rdv' },
          ...(PENDING_RESOURCES.replayWebinaire
            ? [{ label: 'Voir le replay', href: PENDING_RESOURCES.replayWebinaire }]
            : []),
        ],
        upcoming: PENDING_RESOURCES.replayWebinaire ? [] : ['Replay du webinaire'],
      },
    ],
  },
  {
    id: 'prevention',
    title: 'Prévenir les dépôts',
    icon: 'fr-icon-shield-line',
    steps: [
      {
        id: 'prevention',
        label: 'Je parcours les bonnes pratiques pour prévenir les dépôts',
        description: 'Panneaux, aménagement, communication auprès des habitants.',
        links: [
          {
            label: 'Comment communiquer pour réduire les dépôts sauvages',
            to: blog('depots-sauvages-bien-communiquer-pour-les-reduire'),
          },
          {
            label: "Prévenir les dépôts par l'aménagement de l'espace public",
            to: blog('prevenir-les-depots-sauvages-par-lamenagement-urbain'),
          },
          {
            label: 'Organiser un plan de lutte dans sa commune',
            to: blog('plan-de-lutte-contre-les-depots-sauvages-5-volets'),
          },
          ...(PENDING_RESOURCES.arreteTypePrevention
            ? [{ label: "Télécharger l'arrêté type", href: PENDING_RESOURCES.arreteTypePrevention }]
            : []),
        ],
        upcoming: PENDING_RESOURCES.arreteTypePrevention ? [] : ['Arrêté type'],
      },
    ],
  },
  {
    id: 'guide',
    title: "Consulter le guide d'utilisation",
    icon: 'fr-icon-book-2-line',
    steps: [
      {
        id: 'guide',
        label: "Je consulte le guide d'utilisation",
        links: PENDING_RESOURCES.guideUtilisation
          ? [{ label: "Ouvrir le guide d'utilisation", href: PENDING_RESOURCES.guideUtilisation }]
          : [],
        upcoming: PENDING_RESOURCES.guideUtilisation ? [] : ["Guide d'utilisation"],
      },
    ],
  },
]
