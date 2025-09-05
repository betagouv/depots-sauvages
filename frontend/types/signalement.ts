import camelcaseKeys from 'camelcase-keys'
import snakecaseKeys from 'snakecase-keys'

// Single interface for both API and form data
export interface Signalement {
  // Step 1
  commune: string
  localisationDepot: string
  dateConstat: string
  heureConstat: string
  auteurSignalement: string
  natureTerrain: string[]

  // Step 2
  volumeDepot: string
  risqueEcoulement: boolean
  typesDepot: string[]
  precisionsDepot: string
  photoDispo: boolean

  // Step 3
  auteurIdentifie: boolean
  statutAuteur: string
  nomEntreprise: string
  numeroSiret: string
  nomParticulier: string
  prenomParticulier: string
  souhaitePorterPlainte: boolean
  indicesDisponibles: string[]
  precisionsIndices: string
  arreteMunicipalExiste: boolean
  montantForfaitEnlevement: number
  prejudiceMontantConnu: boolean
  prejudiceMontant: number
  prejudiceNombrePersonnes: number
  prejudiceNombreHeures: number
  prejudiceNombreVehicules: number
  prejudiceKilometrage: number
  prejudiceAutresCouts: number

  // Step 4 - Personne contact
  contactNom: string
  contactPrenom: string
  contactEmail: string
  contactTelephone: string
  accepteAccompagnement: boolean

  // Management fields
  docConstatShouldGenerate: boolean
  lettreInfoShouldGenerate: boolean
}

// Simple conversion functions using libraries
export const toApiFormat = (data: Signalement) => snakecaseKeys(data)
export const fromApiFormat = (data: any): Signalement => camelcaseKeys(data)

// Factory function to create an empty Signalement
export const createEmptySignalement = (): Signalement => ({
  commune: '',
  localisationDepot: '',
  dateConstat: '',
  heureConstat: '',
  auteurSignalement: '',
  natureTerrain: [],
  volumeDepot: '',
  risqueEcoulement: false,
  typesDepot: [],
  precisionsDepot: '',
  photoDispo: false,
  auteurIdentifie: false,
  statutAuteur: '',
  nomEntreprise: '',
  numeroSiret: '',
  nomParticulier: '',
  prenomParticulier: '',
  souhaitePorterPlainte: false,
  indicesDisponibles: [],
  precisionsIndices: '',
  arreteMunicipalExiste: false,
  montantForfaitEnlevement: 0,
  prejudiceMontantConnu: false,
  prejudiceMontant: 0,
  prejudiceNombrePersonnes: 0,
  prejudiceNombreHeures: 0,
  prejudiceNombreVehicules: 0,
  prejudiceKilometrage: 0,
  prejudiceAutresCouts: 0,
  contactNom: '',
  contactPrenom: '',
  contactEmail: '',
  contactTelephone: '',
  accepteAccompagnement: false,

  // Management fields
  docConstatShouldGenerate: false,
  lettreInfoShouldGenerate: false,
})
