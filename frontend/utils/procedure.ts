import dayjs from 'dayjs'

export interface ContradictoireInfo {
  dateFin: string | null
  joursRestants: number
  joursRestantsLabel: string
  isExpired: boolean
}

/**
 * Calculates contradictory period details (delivery date + 10 days)
 * @param arDate AR presentation date (ISO string)
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

export const buildLaPosteSuiviUrl = (numeroSuivi: string | null | undefined): string => {
  const numero = (numeroSuivi || '').replace(/\s/g, '').toUpperCase()
  return numero
    ? `https://www.laposte.fr/outils/suivre-vos-envois?code=${encodeURIComponent(numero)}`
    : ''
}
