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

  it('doit valider le montant si connu et rejeter les valeurs négatives', () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.plainteEtat = 'Déposée'
    store.formData.prejudiceMontantConnu = true

    // Blank amount
    store.formData.prejudiceMontant = '' as any
    store.validate()
    expect(store.errors.prejudiceMontant).toBe('Le montant du préjudice est obligatoire')

    // Negative amount
    store.formData.prejudiceMontant = -10
    store.validate()
    expect(store.errors.prejudiceMontant).toBe('La valeur doit être supérieure ou égale à 0')

    // Valid positive amount
    store.formData.prejudiceMontant = 150
    store.validate()
    expect(store.errors.prejudiceMontant).toBeUndefined()
  })

  it('doit autoriser les valeurs vides pour les détails du préjudice mais rejeter les négatifs', () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.plainteEtat = 'Déposée'
    store.formData.prejudiceMontantConnu = false

    // All empty/blank should be allowed now (Option 1)
    store.formData.prejudiceNombrePersonnes = '' as any
    store.formData.prejudiceNombreHeures = undefined as any
    store.formData.prejudiceNombreVehicules = null as any
    store.formData.prejudiceKilometrage = '' as any
    store.formData.prejudiceAutresCouts = '' as any

    store.validate()
    expect(store.errors.prejudiceNombrePersonnes).toBeUndefined()
    expect(store.errors.prejudiceNombreHeures).toBeUndefined()
    expect(store.errors.prejudiceNombreVehicules).toBeUndefined()
    expect(store.errors.prejudiceKilometrage).toBeUndefined()
    expect(store.errors.prejudiceAutresCouts).toBeUndefined()

    // Negative value should be blocked
    store.formData.prejudiceNombrePersonnes = -5
    store.validate()
    expect(store.errors.prejudiceNombrePersonnes).toBe(
      'La valeur doit être supérieure ou égale à 0'
    )
  })

  it('doit convertir les valeurs vides/nulles en 0 pour les détails lors de la sauvegarde', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    store.formData.plainteEtat = 'Déposée'
    store.formData.prejudiceMontantConnu = false
    store.formData.prejudiceNombrePersonnes = '' as any
    store.formData.prejudiceNombreHeures = null as any
    store.formData.prejudiceNombreVehicules = 2
    store.formData.prejudiceKilometrage = undefined as any
    store.formData.prejudiceAutresCouts = 100
    ;(api.createResource as any).mockResolvedValue({ id: 42 })

    await store.saveFormData()

    expect(api.createResource).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        prejudice_nombre_personnes: 0,
        prejudice_nombre_heures: 0,
        prejudice_nombre_vehicules: 2,
        prejudice_kilometrage: 0,
        prejudice_autres_couts: 100,
      })
    )
  })

  it('doit remplacer les valeurs nulles par 0 lors du chargement', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    const apiResponse = {
      id: 123,
      prejudice_nombre_personnes: null,
      prejudice_nombre_heures: 5,
      prejudice_nombre_vehicules: null,
      prejudice_kilometrage: 10,
      prejudice_autres_couts: null,
    }
    vi.spyOn(api, 'fetchResource').mockResolvedValue(apiResponse)

    await store.loadConstatation(123)

    expect(store.formData.prejudiceNombrePersonnes).toBe(0)
    expect(store.formData.prejudiceNombreHeures).toBe(5)
    expect(store.formData.prejudiceNombreVehicules).toBe(0)
    expect(store.formData.prejudiceKilometrage).toBe(10)
    expect(store.formData.prejudiceAutresCouts).toBe(0)
  })

  it('doit permettre de modifier une constatation et de passer de montant inconnu à montant connu sans erreur', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    const apiResponse = {
      id: 123,
      commune: 'Paris',
      localisation_depot: '123 Rue de Rivoli',
      nature_terrain: ['Terrain public'],
      constatant_role: 'maire',
      constatant_est_utilisateur_connecte: true,
      date_constat: '2026-06-29',
      heure_constat: '12:00',
      volume_depot: 'Moins de 1m3',
      types_depot: ['Encombrants'],
      precisions_depot: 'Dépôt sur le trottoir',
      auteur_identifie: false,
      indices_disponibles: ['Documents'],
      precisions_indices: 'des enveloppes',
      ceci_est_un_test: true,
      accepte_accompagnement: true,
      plainte_etat: 'Déposée',
      prejudice_montant_connu: false,
      prejudice_nombre_personnes: 5,
      prejudice_nombre_heures: 2,
      prejudice_nombre_vehicules: 1,
      prejudice_kilometrage: 10,
      prejudice_autres_couts: 50,
    }
    vi.spyOn(api, 'fetchResource').mockResolvedValue(apiResponse)
    vi.spyOn(api, 'updateResource').mockResolvedValue({ id: 123 })

    await store.loadConstatation(123)

    // User changes prejudiceMontantConnu to true (Oui)
    store.formData.prejudiceMontantConnu = true
    store.formData.prejudiceMontant = 500

    const isValid = store.validate()
    console.log('VALIDATION ERRORS:', store.errors)
    expect(isValid).toBe(true)

    await store.saveFormData()

    expect(api.updateResource).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        prejudice_montant_connu: true,
        prejudice_montant: 500,
        prejudice_nombre_personnes: null,
        prejudice_nombre_heures: null,
        prejudice_nombre_vehicules: null,
        prejudice_kilometrage: null,
        prejudice_autres_couts: null,
      })
    )
  })

  it('doit permettre de modifier une constatation et de passer de montant connu à montant inconnu en réinitialisant le montant global', async () => {
    const pinia = createTestingPinia({ stubActions: false })
    const store = useConstatationStore(pinia)

    const apiResponse = {
      id: 123,
      commune: 'Paris',
      localisation_depot: '123 Rue de Rivoli',
      nature_terrain: ['Terrain public'],
      constatant_role: 'maire',
      constatant_est_utilisateur_connecte: true,
      date_constat: '2026-06-29',
      heure_constat: '12:00',
      volume_depot: 'Moins de 1m3',
      types_depot: ['Encombrants'],
      precisions_depot: 'Dépôt sur le trottoir',
      auteur_identifie: false,
      indices_disponibles: ['Documents'],
      precisions_indices: 'des enveloppes',
      ceci_est_un_test: true,
      accepte_accompagnement: true,
      plainte_etat: 'Déposée',
      prejudice_montant_connu: true,
      prejudice_montant: 850.0,
      prejudice_nombre_personnes: null,
      prejudice_nombre_heures: null,
      prejudice_nombre_vehicules: null,
      prejudice_kilometrage: null,
      prejudice_autres_couts: null,
    }
    vi.spyOn(api, 'fetchResource').mockResolvedValue(apiResponse)
    vi.spyOn(api, 'updateResource').mockResolvedValue({ id: 123 })

    await store.loadConstatation(123)

    // User changes prejudiceMontantConnu to false (Non)
    store.formData.prejudiceMontantConnu = false
    // User enters detailed estimation fields
    store.formData.prejudiceNombrePersonnes = 3
    store.formData.prejudiceNombreHeures = 4
    store.formData.prejudiceNombreVehicules = 1
    store.formData.prejudiceKilometrage = 20
    store.formData.prejudiceAutresCouts = 100

    const isValid = store.validate()
    expect(isValid).toBe(true)

    await store.saveFormData()

    expect(api.updateResource).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        prejudice_montant_connu: false,
        prejudice_montant: null,
        prejudice_nombre_personnes: 3,
        prejudice_nombre_heures: 4,
        prejudice_nombre_vehicules: 1,
        prejudice_kilometrage: 20,
        prejudice_autres_couts: 100,
      })
    )
  })
})
