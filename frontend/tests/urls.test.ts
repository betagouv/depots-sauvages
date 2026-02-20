import { describe, expect, it } from 'vitest'
import { getDnModifyUrl, getSignalementDocumentsUrl } from '../services/urls'

describe('Services URLs', () => {
  describe('getDnModifyUrl', () => {
    it('doit générer l’URL de modification pour un numéro de dossier donné', () => {
      const numeroDossier = '12345'
      const url = getDnModifyUrl(numeroDossier)
      expect(url).toContain('/dossiers/12345/modifier')
    })
  })

  describe('getSignalementDocumentsUrl', () => {
    it('doit générer l’URL interne pour les documents d’un signalement', () => {
      const id = 42
      const url = getSignalementDocumentsUrl(id)
      expect(url).toBe('/signalements-dn/42')
    })

    it('doit gérer les IDs sous forme de chaîne', () => {
      const id = '42'
      const url = getSignalementDocumentsUrl(id)
      expect(url).toBe('/signalements-dn/42')
    })
  })
})
