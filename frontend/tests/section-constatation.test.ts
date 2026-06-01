import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, waitFor } from '@testing-library/vue'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import SectionConstatation from '../components/forms/constatation/SectionConstatation.vue'
import * as api from '../services/api'
import { useConstatationStore } from '../stores/constatation'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    getUserInfo: vi.fn(),
  }
})

describe('SectionConstatation', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('doit remplir automatiquement le prénom et le nom si constatantEstUtilisateurConnecte est true', async () => {
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: true,
      proconnect_enabled: true,
      first_name: 'Jean',
      last_name: 'Dupont',
    })

    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)
    store.formData.constatantEstUtilisateurConnecte = true

    render(SectionConstatation, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrRadioButtonSet: true,
          DsfrSelect: true,
          DsfrInputGroup: true,
          DsfrAlert: true,
          RouterLink: true,
        },
      },
    })

    await waitFor(() => {
      expect(api.getUserInfo).toHaveBeenCalled()
      expect(store.formData.constatantPrenom).toBe('Jean')
      expect(store.formData.constatantNom).toBe('Dupont')
    })
  })

  it('ne doit pas écraser les saisies si constatantEstUtilisateurConnecte est false', async () => {
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: true,
      proconnect_enabled: true,
      first_name: 'Jean',
      last_name: 'Dupont',
    })

    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)
    store.formData.constatantEstUtilisateurConnecte = false
    store.formData.constatantPrenom = 'Alice'
    store.formData.constatantNom = 'Martin'

    render(SectionConstatation, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrRadioButtonSet: true,
          DsfrSelect: true,
          DsfrInputGroup: true,
          DsfrAlert: true,
          RouterLink: true,
        },
      },
    })

    await new Promise((resolve) => setTimeout(resolve, 50))
    expect(api.getUserInfo).not.toHaveBeenCalled()
    expect(store.formData.constatantPrenom).toBe('Alice')
    expect(store.formData.constatantNom).toBe('Martin')
  })
})
