import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import NotificationStep from '../components/steps/Notification.vue'
import * as matomo from '../services/matomo'
import { buildLaPosteSuiviUrl } from '../utils/procedure'

vi.mock('../services/matomo', () => ({
  trackAndOpenLink: vi.fn(),
  trackEvent: vi.fn(),
}))

vi.mock('../services/tracking', () => ({
  trackUserAction: vi.fn(),
}))

describe('Notification.vue & Suivi La Poste', () => {
  describe('buildLaPosteSuiviUrl', () => {
    it('retourne une URL La Poste avec le numéro nettoyé d’espaces et en majuscules', () => {
      expect(buildLaPosteSuiviUrl('1a 009 158 2038 0')).toBe(
        'https://www.laposte.fr/outils/suivre-vos-envois?code=1A00915820380'
      )
    })

    it('retourne une chaîne vide si aucun numéro n’est fourni', () => {
      expect(buildLaPosteSuiviUrl('')).toBe('')
      expect(buildLaPosteSuiviUrl('   ')).toBe('')
      expect(buildLaPosteSuiviUrl(null)).toBe('')
      expect(buildLaPosteSuiviUrl(undefined)).toBe('')
    })

    it('utilise une base URL personnalisée si fournie', () => {
      expect(buildLaPosteSuiviUrl('1A009', 'https://custom.laposte.fr/suivi')).toBe(
        'https://custom.laposte.fr/suivi?code=1A009'
      )
    })
  })

  describe('Composant Notification', () => {
    const makeSuivi = (numeroSuivi = '') => ({
      etape_en_cours: 2,
      preuves_fournies: true,
      constatation_signee: true,
      lettre_signe: true,
      lettre_envoyee: true,
      lettre_envoyee_date: '2026-10-14',
      numero_suivi_lettre: numeroSuivi,
      copie_archives: false,
      ar_recu: false,
      ar_statut: '',
      ar_presentation_date: '',
      montant_fixe: false,
      arrete_redige: false,
      titre_recette_emis: false,
      notification_sanction_envoyee: false,
      notification_abandon_envoyee: false,
      decision_poursuite: '',
      souhaite_notifier_abandon: null,
      montant_amende: null,
      motif_abandon: '',
      date_recouvrement_effective: '',
      nettoyage_fait: null,
      nettoyage_par: '',
      observations_internes: '',
      titre_recette_confirme: false,
      montant_recouvre: false,
      dossier_archive: false,
      identification_reussie: true,
    })

    it('affiche le lien de suivi La Poste lorsque le numéro est renseigné', async () => {
      const wrapper = mount(NotificationStep, {
        props: {
          suivi: makeSuivi('1A00915820380'),
          lettreInfoUrl: '/api/lettre-info/1',
          constatationId: 1,
        },
        global: {
          stubs: {
            DsfrAlert: true,
            DsfrButton: true,
            DsfrInput: true,
            DsfrSelect: true,
            ListeActions: {
              template: '<div><slot name="extra-lettre_envoyee" /></div>',
            },
          },
        },
      })

      const link = wrapper.find('a[href*="laposte.fr"]')
      expect(link.exists()).toBe(true)
      expect(link.attributes('href')).toBe(
        'https://www.laposte.fr/outils/suivre-vos-envois?code=1A00915820380'
      )
      expect(link.attributes('target')).toBe('_blank')

      await link.trigger('click')
      expect(matomo.trackEvent).toHaveBeenCalledWith('Procédures', 'Suivi_Recommande_LaPoste')
    })

    it('masque le lien La Poste si aucun numéro n’est renseigné', () => {
      const wrapper = mount(NotificationStep, {
        props: {
          suivi: makeSuivi(''),
          lettreInfoUrl: '/api/lettre-info/1',
          constatationId: 1,
        },
        global: {
          stubs: {
            DsfrAlert: true,
            DsfrButton: true,
            DsfrInput: true,
            DsfrSelect: true,
            ListeActions: {
              template: '<div><slot name="extra-lettre_envoyee" /></div>',
            },
          },
        },
      })

      const link = wrapper.find('a[href*="laposte.fr"]')
      expect(link.exists()).toBe(false)
    })
  })
})
