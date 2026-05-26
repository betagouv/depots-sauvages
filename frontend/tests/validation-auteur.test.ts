import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import SectionAuteurDepot from '../components/forms/constatation/SectionAuteurDepot.vue'
import { useConstatationStore } from '../stores/constatation'

describe('SectionAuteurDepot - Validation indicesDisponibles', () => {
  it("doit valider et afficher le message d'erreur pour les indices disponibles", async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.auteurIdentifie = false
    store.formData.indicesDisponibles = []
    store.formData.precisionsIndices = 'Quelques précisions'
    store.formData.plainteEtat = 'Aucune'

    const isValid = store.validate()
    expect(isValid).toBe(false)
    expect(store.errors.indicesDisponibles).toBe('Veuillez cocher au moins une option')

    render(SectionAuteurDepot, {
      global: {
        plugins: [pinia],
        stubs: {
          AddressAutocomplete: true,
          BooleanRadioSet: true,
          DsfrCallout: true,
          DsfrCheckboxSet: {
            props: ['errorMessage', 'options', 'modelValue'],
            template: `
              <div class="dsfr-checkbox-set-stub">
                <slot name="legend" />
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
              </div>
            `,
          },
          DsfrInput: true,
          DsfrInputGroup: true,
          DsfrRadioButtonSet: true,
        },
      },
    })

    expect(screen.getByText('Veuillez cocher au moins une option')).toBeInTheDocument()
  })

  it("ne doit pas afficher d'erreur si au moins une option est sélectionnée", async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.auteurIdentifie = false
    store.formData.indicesDisponibles = ['Documents']
    store.formData.precisionsIndices = 'Quelques précisions'
    store.formData.plainteEtat = 'Aucune'

    const isValid = store.validate()
    expect(store.errors.indicesDisponibles).toBeUndefined()

    render(SectionAuteurDepot, {
      global: {
        plugins: [pinia],
        stubs: {
          AddressAutocomplete: true,
          BooleanRadioSet: true,
          DsfrCallout: true,
          DsfrCheckboxSet: {
            props: ['errorMessage', 'options', 'modelValue'],
            template: `
              <div class="dsfr-checkbox-set-stub">
                <slot name="legend" />
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
              </div>
            `,
          },
          DsfrInput: true,
          DsfrInputGroup: true,
          DsfrRadioButtonSet: true,
        },
      },
    })

    expect(screen.queryByText('Veuillez cocher au moins une option')).not.toBeInTheDocument()
  })
})

describe('SectionAuteurDepot - Validation Entreprise', () => {
  it("doit requérir le SIRET, le nom et l'adresse pour une entreprise française", async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.auteurIdentifie = true
    store.formData.statutAuteur = 'entreprise'
    store.formData.entrepriseFrancaise = true
    store.formData.auteurSiret = ''
    store.formData.auteurNom = ''
    store.formData.auteurAdresse = ''
    store.formData.indicesDisponibles = ['Documents']
    store.formData.precisionsIndices = 'Précisions'

    const isValid = store.validate()
    expect(isValid).toBe(false)
    expect(store.errors.auteurSiret).toBe(
      'Le numéro SIRET est obligatoire pour une entreprise française'
    )
    expect(store.errors.auteurNom).toBe("Le nom de l'entreprise est obligatoire")
    expect(store.errors.auteurAdresse).toBe("L'adresse de l'entreprise est obligatoire")
  })

  it("doit valider avec succès si le SIRET, le nom et l'adresse sont renseignés pour une entreprise française", async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    // Populate all globally required fields so that overall store validation passes
    store.formData.localisationDepot = '123 Rue de Paris'
    store.formData.commune = 'Paris'
    store.formData.natureTerrain = ['Terrain public']
    store.formData.constatantRole = 'maire'
    store.formData.dateConstat = '2026-05-26'
    store.formData.heureConstat = '10:00'
    store.formData.volumeDepot = 'Moins de 1m3'
    store.formData.typesDepot = ['Pneus']
    store.formData.precisionsDepot = 'Dépôt de pneus'
    store.formData.ceciEstUnTest = false
    store.formData.accepteAccompagnement = true

    store.formData.auteurIdentifie = true
    store.formData.statutAuteur = 'entreprise'
    store.formData.entrepriseFrancaise = true
    store.formData.auteurSiret = '12345678901234'
    store.formData.auteurNom = 'Entreprise Test'
    store.formData.auteurAdresse = '123 Rue de la Paix, Paris'
    store.formData.indicesDisponibles = ['Documents']
    store.formData.precisionsIndices = 'Précisions'

    const isValid = store.validate()
    expect(store.errors.auteurSiret).toBeUndefined()
    expect(store.errors.auteurNom).toBeUndefined()
    expect(store.errors.auteurAdresse).toBeUndefined()
    expect(isValid).toBe(true)
  })
})
