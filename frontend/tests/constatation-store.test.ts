import { createTestingPinia } from '@pinia/testing'
import { describe, expect, it, vi } from 'vitest'
import * as api from '../services/api'
import { useConstatationStore } from '../stores/constatation'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    createResource: vi.fn(),
    updateResource: vi.fn(),
  }
})

describe('ConstatationStore - Prejudice Logic', () => {
  it('doit effacer les champs détaillés si le montant est connu', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.plainteEtat = 'Déposée'
    store.formData.prejudiceMontantConnu = true
    store.formData.prejudiceMontant = 1500

    // Fill in detailed fields
    store.formData.prejudiceNombrePersonnes = 5
    store.formData.prejudiceNombreHeures = 10
    store.formData.prejudiceNombreVehicules = 2
    store.formData.prejudiceKilometrage = 150
    store.formData.prejudiceAutresCouts = 200
    ;(api.createResource as any).mockResolvedValue({ id: 42 })

    await store.saveFormData()

    expect(api.createResource).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        prejudice_montant_connu: true,
        prejudice_montant: 1500,
        prejudice_nombre_personnes: null,
        prejudice_nombre_heures: null,
        prejudice_nombre_vehicules: null,
        prejudice_kilometrage: null,
        prejudice_autres_couts: null,
      })
    )
  })

  it('doit effacer le montant direct si le montant est inconnu', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.plainteEtat = 'Déposée'
    store.formData.prejudiceMontantConnu = false
    store.formData.prejudiceMontant = 1500

    // Fill in detailed fields
    store.formData.prejudiceNombrePersonnes = 5
    store.formData.prejudiceNombreHeures = 10
    store.formData.prejudiceNombreVehicules = 2
    store.formData.prejudiceKilometrage = 150
    store.formData.prejudiceAutresCouts = 200
    ;(api.createResource as any).mockResolvedValue({ id: 42 })

    await store.saveFormData()

    expect(api.createResource).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        prejudice_montant_connu: false,
        prejudice_montant: null,
        prejudice_nombre_personnes: 5,
        prejudice_nombre_heures: 10,
        prejudice_nombre_vehicules: 2,
        prejudice_kilometrage: 150,
        prejudice_autres_couts: 200,
      })
    )
  })
})
