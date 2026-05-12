import camelcaseKeys from 'camelcase-keys'
import snakecaseKeys from 'snakecase-keys'

// Options for form fields
export const ConstatantOptions = [
  { value: 'maire', text: 'Maire' },
  { value: 'adjoint au maire', text: 'Adjoint au maire' },
  { value: 'conseiller municipal', text: 'Conseiller municipal' },
  { value: 'policier municipal', text: 'Policier municipal' },
  { value: 'garde champêtre', text: 'Garde champêtre' },
  { value: 'agent commissionné', text: 'Agent commissionné' },
  { value: 'agent assermenté', text: 'Agent assermenté' },
  { value: 'president ECPI', text: "Président de l'EPCI" },
  { value: 'conseiller communautaire', text: 'Conseiller communautaire' },
  { value: 'agent communautaire', text: 'Agent communautaire' },
  { value: 'autre', text: 'Entrer une autre option' },
] as const

export const VolumeOptions = [
  { label: 'Moins de 1m3', value: 'Moins de 1m3', id: 'vol-1' },
  { label: 'Entre 1 et 3m3', value: 'Entre 1 et 3m3', id: 'vol-2' },
  { label: 'Entre 3 et 10m3', value: 'Entre 3 et 10m3', id: 'vol-3' },
  { label: 'Entre 10 et 100m3', value: 'Entre 10 et 100m3', id: 'vol-4' },
  { label: 'Plus de 100m3', value: 'Plus de 100m3', id: 'vol-5' },
] as const

export const TypeDepotOptions = [
  { label: 'Amiante', value: 'Amiante', id: 'type-amiante' },
  { label: 'Carrelage', value: 'Carrelage', id: 'type-carrelage' },
  { label: 'Déchets automobiles', value: 'Déchets automobiles', id: 'type-automobiles' },
  { label: 'Déchets de construction', value: 'Déchets de construction', id: 'type-construction' },
  {
    label: 'Déchets électriques et électroniques',
    value: 'Déchets électriques et électroniques',
    id: 'type-elec',
  },
  { label: 'Déchets médicaux', value: 'Déchets médicaux', id: 'type-medicaux' },
  { label: 'Déchets verts', value: 'Déchets verts', id: 'type-verts' },
  { label: 'Électroménager', value: 'Électroménager', id: 'type-electromenager' },
  { label: 'Encombrants', value: 'Encombrants', id: 'type-encombrants' },
  { label: 'Emballages et cartons', value: 'Emballages et cartons', id: 'type-emballages' },
  { label: 'Gravats', value: 'Gravats', id: 'type-gravats' },
  { label: 'Huiles', value: 'Huiles', id: 'type-huiles' },
  { label: 'Ordures ménagères', value: 'Ordures ménagères', id: 'type-ordures' },
  { label: 'Peintures et essences', value: 'Peintures et essences', id: 'type-peintures' },
  { label: 'Pneus', value: 'Pneus', id: 'type-pneus' },
  { label: 'Textiles', value: 'Textiles', id: 'type-textiles' },
  { label: 'Tuiles', value: 'Tuiles', id: 'type-tuiles' },
  { label: 'Autre', value: 'Autre', id: 'type-autre' },
] as const

export const NatureTerrainOptions = [
  { label: 'Terrain public', id: 'terrain-public', value: 'Terrain public' },
  { label: 'Forêt domaniale', id: 'foret-domaniale', value: 'Forêt domaniale' },
  { label: 'Terrain privé', id: 'terrain-prive', value: 'Terrain privé' },
  { label: 'Je ne sais pas', id: 'je-ne-sais-pas', value: 'Je ne sais pas' },
] as const

export const InfoAuteurOptions = [
  { label: 'Nom et prénom', value: 'Nom et prénom', id: 'info-nom-prenom' },
  { label: 'Adresse postale', value: 'Adresse postale', id: 'info-adresse' },
  { label: "Plaque d'immatriculation", value: "Plaque d'immatriculation", id: 'info-plaque' },
  { label: "Je ne dispose d'aucune de ces informations", value: 'Aucune', id: 'info-aucune' },
] as const

export const IndicesOptions = [
  { label: 'Documents (factures, colis, courriers, etc.)', value: 'Documents', id: 'indice-doc' },
  { label: 'Caméra de vidéo-surveillance', value: 'Video', id: 'indice-cam' },
  { label: 'Pièges photographiques', value: 'Pieges', id: 'indice-piege' },
  { label: 'Témoignages', value: 'Témoignages', id: 'indice-tem' },
  {
    label: 'Activités liées au dépôt constaté (travaux à proximité, produits similaires détenus)',
    value: 'Activités',
    id: 'indice-act',
  },
  {
    label: "Il ne semble y avoir aucun moyen d'identifier l'auteur présumé",
    value: 'Aucun',
    id: 'indice-aucun',
  },
] as const

export const PlainteOptions = [
  { label: 'Une plainte a déjà été déposée', value: 'Déposée', id: 'plainte-faite' },
  { label: 'Une plainte sera déposée', value: 'Sera déposée', id: 'plainte-future' },
  { label: 'Aucune plainte ne sera déposée', value: 'Aucune', id: 'plainte-aucune' },
] as const

export const CiviliteOptions = [
  { value: 'M.', label: 'Monsieur' },
  { value: 'Mme', label: 'Madame' },
] as const

export type ConstatantRole = (typeof ConstatantOptions)[number]['value']
export type VolumeDepot = (typeof VolumeOptions)[number]['value'] | ''
export type TypeDepot = (typeof TypeDepotOptions)[number]['value']
export type NatureTerrain = (typeof NatureTerrainOptions)[number]['value']
export type InfoAuteur = (typeof InfoAuteurOptions)[number]['value']
export type MoyenIdentification = (typeof IndicesOptions)[number]['value']
export type StatutPlainte = (typeof PlainteOptions)[number]['value'] | ''

// Single interface for both API and form data
export interface Constatation {
  // Localisation
  commune: string
  localisationDepot: string
  dateConstat: string
  heureConstat: string
  natureTerrain: NatureTerrain[]
  proprietaireTerrainPrive: string

  // Constatation
  constatantCivilite: string
  constatantRole: ConstatantRole
  constatantRoleAutre: string
  constatantNom: string
  constatantPrenom: string
  constatantEstUtilisateurConnecte: boolean

  // Description
  volumeDepot: VolumeDepot
  risqueEcoulement: boolean
  typesDepot: TypeDepot[]
  precisionsDepot: string
  photoDispo: boolean

  // Responsable
  auteurIdentifie: boolean | null
  statutAuteur: string
  auteurCivilite: string
  auteurNom: string
  auteurPrenom: string
  auteurAdresse: string
  auteurSiret: string
  entrepriseFrancaise: boolean | null
  informationsAuteur: InfoAuteur[]
  plainteEtat: StatutPlainte
  indicesDisponibles: MoyenIdentification[]
  precisionsIndices: string

  // Prejudice
  montantForfaitEnlevement: number
  prejudiceMontantConnu: boolean | null
  prejudiceMontant: number
  prejudiceNombrePersonnes: number
  prejudiceNombreHeures: number
  prejudiceNombreVehicules: number
  prejudiceKilometrage: number
  prejudiceAutresCouts: number

  // Contact
  contactNom: string
  contactPrenom: string
  contactEmail: string
  contactTelephone: string
  accepteAccompagnement: boolean
  ceciEstUnTest: boolean | null

  // Management fields
  docConstatShouldGenerate: boolean
  lettreInfoShouldGenerate: boolean
}

// Simple conversion functions using libraries
export const toApiFormat = (data: Constatation) => snakecaseKeys(data)
export const fromApiFormat = (data: any): Constatation => camelcaseKeys(data)

// Factory function to create an empty Constatation
export const createEmptyConstatation = (): Constatation => ({
  commune: '',
  localisationDepot: '',
  dateConstat: '',
  heureConstat: '',
  natureTerrain: [],
  proprietaireTerrainPrive: '',
  constatantCivilite: '',
  constatantNom: '',
  constatantPrenom: '',
  constatantRole: '',
  constatantRoleAutre: '',
  constatantEstUtilisateurConnecte: true,
  volumeDepot: '',
  risqueEcoulement: false,
  typesDepot: [],
  precisionsDepot: '',
  photoDispo: false,
  auteurIdentifie: null,
  statutAuteur: '',
  auteurCivilite: '',
  auteurNom: '',
  auteurPrenom: '',
  auteurAdresse: '',
  auteurSiret: '',
  entrepriseFrancaise: null,
  informationsAuteur: [],
  plainteEtat: '',
  indicesDisponibles: [],
  precisionsIndices: '',
  montantForfaitEnlevement: 0,
  prejudiceMontantConnu: null,
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
  ceciEstUnTest: null,

  // Management fields
  docConstatShouldGenerate: true,
  lettreInfoShouldGenerate: true,
})
