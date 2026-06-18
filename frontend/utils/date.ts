import dayjs from 'dayjs'
import 'dayjs/locale/fr'

dayjs.locale('fr')

export const formatDate = (dateStr?: string | null) => {
  if (!dateStr) return 'Date inconnue'
  const d = dayjs(dateStr)
  return d.isValid() ? d.format('D MMMM YYYY [à] HH:mm') : 'Date invalide'
}

export const formatConstatationDate = (dateStr?: string | null, timeStr?: string | null) => {
  if (!dateStr) return 'Date inconnue'

  const hasTime = !!timeStr || dateStr.includes('T')
  const dateTimeStr = dateStr.includes('T')
    ? dateStr
    : timeStr
      ? `${dateStr}T${timeStr}`
      : `${dateStr}T00:00`

  const d = dayjs(dateTimeStr)
  if (!d.isValid()) return 'Date invalide'

  return d.format(hasTime ? 'D MMMM YYYY [à] HH:mm' : 'D MMMM YYYY')
}

export const shouldShowModificationDate = (
  creationDate?: string | null,
  modificationDate?: string | null
) => {
  if (!creationDate || !modificationDate) return false
  const creation = dayjs(creationDate)
  const modification = dayjs(modificationDate)
  return modification.diff(creation) > 60000 // 1 minute
}

export const getTodayISOString = () => {
  return dayjs().format('YYYY-MM-DD')
}
