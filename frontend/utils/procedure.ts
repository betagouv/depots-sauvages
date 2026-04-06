export interface ContradictoireInfo {
  dateFin: string | null
  joursRestants: number
  joursRestantsLabel: string
  isExpired: boolean
}

/**
 * Calcule les informations de délai de contradictoire (AR + 10 jours)
 * @param arDate Date de présentation de l'AR (ISO string)
 */
export const calculateContradictoire = (arDate: string | null | undefined): ContradictoireInfo => {
  if (!arDate) {
    return {
      dateFin: null,
      joursRestants: 0,
      joursRestantsLabel: '',
      isExpired: false,
    }
  }

  const dateFin = new Date(arDate)
  dateFin.setDate(dateFin.getDate() + 10)

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const fin = new Date(dateFin)
  fin.setHours(0, 0, 0, 0)

  const diffTime = fin.getTime() - today.getTime()
  const joursRestants = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  let label = ''
  if (joursRestants < 0) {
    label = 'Le délai du contradictoire est expiré : vous pouvez continuer la procédure.'
  } else if (joursRestants === 0) {
    label = "Le délai du contradictoire expire aujourd'hui : vous pouvez continuer la procédure."
  } else {
    label = `La période du contradictoire sera écoulée dans ${joursRestants} jour${joursRestants > 1 ? 's' : ''} : vous pourrez alors continuer la procédure.`
  }

  return {
    dateFin: dateFin.toLocaleDateString('fr-FR'),
    joursRestants,
    joursRestantsLabel: label,
    isExpired: joursRestants < 0,
  }
}
