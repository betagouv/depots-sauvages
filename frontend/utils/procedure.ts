import dayjs from 'dayjs'

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
  const fin = dayjs(arDate).add(10, 'day').startOf('day')
  const today = dayjs().startOf('day')
  const joursRestants = fin.diff(today, 'day')
  let label = ''
  if (joursRestants < 0) {
    label = 'Le délai du contradictoire est expiré : vous pouvez continuer la procédure.'
  } else if (joursRestants === 0) {
    label = "Le délai du contradictoire expire aujourd'hui : vous pouvez continuer la procédure."
  } else {
    label =
      "La période du contradictoire débute à la réception de l'accusé de réception, même si le courrier est refusé ou non réclamé. Vous pourrez continuer la procédure à la fin de cette période."
  }
  return {
    dateFin: fin.format('DD/MM/YYYY'),
    joursRestants,
    joursRestantsLabel: label,
    isExpired: joursRestants < 0,
  }
}
