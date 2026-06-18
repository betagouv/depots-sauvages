import { describe, expect, it } from 'vitest'
import {
  getSuiviProcedureUrl,
  getDocConstatUrl,
  getLettreInfoUrl,
} from '../services/urls'

describe('Services URLs', () => {
  describe('getSuiviProcedureUrl', () => {
    it('doit générer l’URL interne pour le suivi de procédure', () => {
      const id = 42
      const url = getSuiviProcedureUrl(id)
      expect(url).toBe('/suivi-procedure/42')
    })
  })

  describe('getDocConstatUrl', () => {
    it('doit générer l’URL de téléchargement du rapport de constatation', () => {
      expect(getDocConstatUrl(42)).toContain('/api/constatations/42/documents/doc-constat/')
      expect(getDocConstatUrl(null)).toBe('')
    })
  })

  describe('getLettreInfoUrl', () => {
    it('doit générer l’URL de téléchargement de la lettre d’information', () => {
      expect(getLettreInfoUrl(42)).toContain('/api/constatations/42/documents/lettre-info/')
      expect(getLettreInfoUrl(null)).toBe('')
    })
  })
})

