export const getProcedureStatut = (procedure: any) => {
  const sp = procedure.suivi_procedure
  if (sp.etape_en_cours === 1) {
    if (sp.identification_reussie === false) return 'Auteur non identifié'
    if (!sp.preuves_fournies || !sp.constatation_signee) return 'Pièces incomplètes'
    return 'Pièces prêtes'
  }
  if (sp.etape_en_cours === 2) {
    if (!sp.lettre_signe) return 'Lettre à signer'
    return 'Lettre à envoyer'
  }
  if (sp.etape_en_cours === 3) return 'Décision à prendre'
  if (sp.etape_en_cours === 4) return 'Exécution en cours'
  if (sp.etape_en_cours === 5) return 'Clôturé'
  return 'Inconnu'
}



export const getAuteurIdentifieText = (val: boolean | null) => {
  if (val === true) return 'Oui'
  if (val === false) return 'Non'
  return 'Inconnu'
}

export const getBadgeClass = (status: string) => {
  if (status === 'Pièces incomplètes') return 'bo-badge bo-badge--yellow'
  if (status === 'Auteur non identifié') return 'bo-badge bo-badge--red'
  if (status === 'Décision à prendre') return 'bo-badge bo-badge--blue'
  if (status === 'Lettre à envoyer' || status === 'Lettre à signer')
    return 'bo-badge bo-badge--gray'
  return 'bo-badge bo-badge--green'
}

export const getStepLabel = (step: number) => {
  const labels = ['Constatation', 'Pièces jointes', 'Notification', 'Décision', 'Exécution/Clôture']
  return labels[step - 1]
}
