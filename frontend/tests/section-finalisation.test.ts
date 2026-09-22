import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import SectionFinalisation from '../components/forms/constatation/SectionFinalisation.vue'
import { useConstatationStore } from '../stores/constatation'

const renderSection = (pinia: ReturnType<typeof createTestingPinia>) =>
  render(SectionFinalisation, {
    global: {
      plugins: [pinia],
      stubs: {
        DsfrCheckbox: true,
        DsfrInputGroup: true,
        DsfrRadioButtonSet: true,
      },
    },
  })

describe('SectionFinalisation', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("doit bloquer la validation tant que le traitement des données n'est pas reconnu", () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)
    store.formData.accepteTraitementDonnees = false

    store.validate()

    expect(store.errors.accepteTraitementDonnees).toBeTruthy()
  })

  it("ne doit pas exiger de demande d'accompagnement pour valider", () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)
    store.formData.accepteTraitementDonnees = true
    store.formData.besoinAccompagnement = false

    store.validate()

    expect(store.errors.accepteTraitementDonnees).toBeUndefined()
    expect(store.errors.besoinAccompagnement).toBeUndefined()
  })

  it("ne doit afficher le champ téléphone que si un accompagnement est demandé", async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)
    store.formData.besoinAccompagnement = false

    const { container } = renderSection(pinia)
    expect(container.querySelector('dsfr-input-group-stub')).toBeNull()

    store.formData.besoinAccompagnement = true
    await nextTick()

    expect(container.querySelector('dsfr-input-group-stub')).not.toBeNull()
  })
})
