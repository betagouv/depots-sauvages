export const getBadgeClass = (step: number) => {
  if (step === 0) return 'bo-badge bo-badge--yellow'
  if (step === 1) return 'bo-badge bo-badge--gray'
  if (step === 2) return 'bo-badge bo-badge--gray'
  if (step === 3) return 'bo-badge bo-badge--gray'
  if (step === 4) return 'bo-badge bo-badge--blue'
  if (step === 5) return 'bo-badge bo-badge--green'
  return 'bo-badge bo-badge--gray'
}

export const getAuteurIdentifieText = (val: boolean | null) => {
  if (val === true) return 'Oui'
  if (val === false) return 'Non'
  return 'Inconnu'
}

export const getProcedureTraitement = (procedure: any) => {
  const sp = procedure.suivi_procedure
  if (sp.statut_traitement) return sp.statut_traitement
  if (sp.dossier_archive) return 'Clôturé'
  if (sp.etape_en_cours === 5 || sp.montant_recouvre) return 'Résolu'
  if (sp.observations_internes?.toLowerCase().includes('pause')) return 'En pause'
  if (sp.personne_assignee) return 'Ouvert'
  return 'Nouveau'
}

export const getTraitementBadgeClass = (traitement: string) => {
  if (traitement === 'Nouveau') return 'bo-badge bo-badge--blue'
  if (traitement === 'Ouvert') return 'bo-badge bo-badge--blue'
  if (traitement === 'En pause') return 'bo-badge bo-badge--yellow'
  if (traitement === 'Résolu') return 'bo-badge bo-badge--green'
  if (traitement === 'Clôturé') return 'bo-badge bo-badge--gray'
  return 'bo-badge bo-badge--gray'
}

export const getStepLabel = (step: number, auteurIdentifie: boolean = true) => {
  if (auteurIdentifie) {
    const labels = [
      'Constatation',
      'Pièces jointes',
      'Notification',
      'Décision',
      'Sanctionner',
      'Clôture',
    ]
    return labels[step] || ''
  } else {
    const labels = [
      'Constatation',
      'Pièces jointes',
      "Identifier l'auteur",
      'Recherche',
      '',
      'Clôture',
    ]
    return labels[step] || ''
  }
}

/**
 * Generic query parameter parser to parse and typed-coerce query values
 */
export const parseQueryParam = (val: any, defaultValue: any) => {
  if (val === undefined || val === null || val === '') return defaultValue

  // If the val is a digit, parse it as a number
  const parsedInt = parseInt(val, 10)
  if (!isNaN(parsedInt) && String(parsedInt) === String(val)) {
    return parsedInt
  }

  return val
}
