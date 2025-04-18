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
  natureTerrain: string
  volumeDepot: string
  typesDepot: string[]
  precisionsDepot: string
  photoDispo: boolean

  // Step 2
  auteurIdentifie: boolean
  souhaitePorterPlainte: boolean
  indicesDisponibles: string[]
  precisionsIndices: string
  arreteMunicipalExiste: boolean
  prejudiceMontantConnu: boolean
  prejudiceMontant: number
  prejudiceNombrePersonnes: number
  prejudiceNombreHeures: number
  prejudiceNombreVehicules: number
  prejudiceKilometrage: number
  prejudiceAutresCouts: number
  generate_doc: boolean
}

// Simple conversion functions using libraries
export const toApiFormat = (data: Signalement) => snakecaseKeys(data)
export const fromApiFormat = (data: any): Signalement => camelcaseKeys(data)
