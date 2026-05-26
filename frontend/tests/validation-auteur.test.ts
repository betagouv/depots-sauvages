import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import SectionAuteurDepot from '../components/forms/constatation/SectionAuteurDepot.vue'
import { useConstatationStore } from '../stores/constatation'

describe('SectionAuteurDepot - Validation indicesDisponibles', () => {
  it('doit valider et afficher le message d\'erreur pour les indices disponibles', async () => {
    const pinia = createTestingPinia({
      stubActions: false, // On veut tester la vraie méthode validate()
    })

    const store = useConstatationStore(pinia)

    // Configuration des données : auteurIdentifie !== null
    store.formData.auteurIdentifie = false // L'auteur présumé n'est pas identifié (mais auteurIdentifie !== null)
    store.formData.indicesDisponibles = [] // Aucun indice coché
    store.formData.precisionsIndices = 'Quelques précisions'
    store.formData.plainteEtat = 'Aucune'

    // 1. Vérification de la validation dans le store
    const isValid = store.validate()
    expect(isValid).toBe(false)
    expect(store.errors.indicesDisponibles).toBe('Veuillez cocher au moins une option')

    // 2. Vérification que le message d'erreur est bien affiché dans le composant
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

    // Le message d'erreur doit être présent dans le DOM
    expect(screen.getByText('Veuillez cocher au moins une option')).toBeInTheDocument()
  })

  it('ne doit pas afficher d\'erreur si au moins une option est sélectionnée', async () => {
    const pinia = createTestingPinia({
      stubActions: false,
    })

    const store = useConstatationStore(pinia)

    // Configuration des données : au moins un indice
    store.formData.auteurIdentifie = false
    store.formData.indicesDisponibles = ['Documents']
    store.formData.precisionsIndices = 'Quelques précisions'
    store.formData.plainteEtat = 'Aucune'

    // 1. Vérification de la validation dans le store
    const isValid = store.validate()
    expect(store.errors.indicesDisponibles).toBeUndefined()

    // 2. Vérification dans le composant
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

    // L'erreur ne doit pas être affichée
    expect(screen.queryByText('Veuillez cocher au moins une option')).not.toBeInTheDocument()
  })
})
