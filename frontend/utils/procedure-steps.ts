export interface StepTitleContext {
  auteurIdentifie: boolean
  identificationReussie?: boolean | null
  decisionPoursuite?: string | null
}

/**
 * Libellés courts, utilisés dans les vues back-office (tableau de bord, liste des
 * procédures, timeline). Indexés directement par `etape_en_cours`, sans dépendre de
 * l'issue de l'identification ni de la décision de poursuite.
 */
const SHORT_LABELS_AUTEUR_IDENTIFIE = [
  'Constatation',
  'Pièces jointes',
  'Notification',
  'Décision',
  'Sanctionner',
  'Clôture',
]

const SHORT_LABELS_AUTEUR_NON_IDENTIFIE = [
  'Constatation',
  'Pièces jointes',
  "Identifier l'auteur",
  'Recherche',
  '',
  'Clôture',
]

export const getShortStepLabel = (step: number, auteurIdentifie: boolean = true): string => {
  const labels = auteurIdentifie ? SHORT_LABELS_AUTEUR_IDENTIFIE : SHORT_LABELS_AUTEUR_NON_IDENTIFIE
  return labels[step] || ''
}

/**
 * Libellés longs, utilisés comme titres de section sur la page suivi-procedure et
 * comme "prochaine étape" sur la page mes-procedures. L'index dans le tableau
 * correspond à la valeur de `etape_en_cours`.
 */
export const getStepTitles = ({
  auteurIdentifie,
  identificationReussie,
  decisionPoursuite,
}: StepTitleContext): string[] => {
  if (!auteurIdentifie) {
    const titles = [
      'Réaliser la constatation',
      'Compléter les pièces de procédure',
      "Identifier l'auteur",
    ]
    if (identificationReussie === true) {
      titles.push('Mettre à jour le dossier')
    } else if (identificationReussie === false) {
      titles.push('Clôturer la procédure')
    }
    return titles
  }

  const actionStepTitle =
    decisionPoursuite === 'sanction'
      ? "Sanctionner l'auteur"
      : decisionPoursuite === 'abandon'
        ? 'Abandonner les poursuites'
        : "Mener l'action de poursuite"

  return [
    'Réaliser la constatation',
    'Signer les pièces de procédure',
    "Notifier l'auteur présumé",
    'Décider des poursuites',
    actionStepTitle,
    'Clôturer la procédure',
  ]
}

export const getCurrentStepTitle = (etapeEnCours: number, context: StepTitleContext): string =>
  getStepTitles(context)[etapeEnCours] ?? ''
