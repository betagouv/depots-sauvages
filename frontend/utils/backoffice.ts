export const getBadgeClass = (step: number) => {
  if (step === 1) return 'bo-badge bo-badge--yellow'
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

export const getStepLabel = (step: number) => {
  const labels = ['Constatation', 'Pièces jointes', 'Notification', 'Décision', 'Clôture']
  return labels[step - 1]
}
