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
    label = 'Le délai de contradictoire est expiré'
  } else if (joursRestants === 0) {
    label = "Ce délai expire aujourd'hui"
  } else {
    label = `Ce délai sera écoulé dans ${joursRestants} jour${joursRestants > 1 ? 's' : ''}`
  }

  return {
    dateFin: dateFin.toLocaleDateString('fr-FR'),
    joursRestants,
    joursRestantsLabel: label,
    isExpired: joursRestants < 0,
  }
}
