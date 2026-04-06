export interface ContradictoireInfo {
  dateFin: string | null
  joursRestants: number
  joursRestantsLabel: string
  isExpired: boolean
  isClose: boolean // Moins de 3 jours
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
      isClose: false,
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
    label = 'Délai expiré'
  } else if (joursRestants === 0) {
    label = "Aujourd'hui"
  } else {
    label = `${joursRestants} jour${joursRestants > 1 ? 's' : ''} restant${joursRestants > 1 ? 's' : ''}`
  }

  return {
    dateFin: dateFin.toLocaleDateString('fr-FR'),
    joursRestants,
    joursRestantsLabel: label,
    isExpired: joursRestants < 0,
    isClose: joursRestants >= 0 && joursRestants < 3,
  }
}
