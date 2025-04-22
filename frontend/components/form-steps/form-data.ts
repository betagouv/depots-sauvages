export const STEPS = [
  'Information sur le dépôt de déchets',
  'Procédure et préjudice',
  'Et maintenant ?',
]

export const volumeOptions = [
  { text: 'Sélectionner une option', value: '', disabled: true },
  { text: 'Moins de 1m³', value: 'moins1m3' },
  { text: 'Entre 1 et 3m³', value: '1a3m3' },
  { text: 'Plus de 3m³', value: 'plus3m3' },
]

export const natureTerrainOptions = [
  {
    label: 'Privé',
    value: 'prive',
    id: 'terrain-prive',
    hint: '',
  },
  {
    label: 'Public',
    value: 'public',
    id: 'terrain-public',
  },
  {
    label: 'Je ne sais pas',
    value: 'inconnu',
    id: 'terrain-inconnu',
  },
]

export const typesDepotOptions = [
  {
    label: 'Tuiles',
    value: 'tuiles',
    id: 'depot-tuiles',
    name: 'types-depot',
  },
  {
    label: 'Carrelage',
    value: 'carrelage',
    id: 'depot-carrelage',
    name: 'types-depot',
  },
  {
    label: 'Encombrants',
    value: 'encombrants',
    id: 'dechets-encombrants',
    name: 'types-dechets',
  },
  {
    label: 'Déchets verts',
    value: 'dechetsVerts',
    id: 'dechets-verts',
    name: 'types-dechets',
  },
  {
    label: 'Gravats',
    value: 'gravats',
    id: 'dechets-gravats',
    name: 'types-dechets',
  },
  {
    label: 'Pneus',
    value: 'pneus',
    id: 'dechets-pneus',
    name: 'types-dechets',
  },
  {
    label: 'Électroménager',
    value: 'electromenager',
    id: 'dechets-electromenager',
    name: 'types-dechets',
  },
  {
    label: 'Ordures ménagères',
    value: 'orduresMenageres',
    id: 'dechets-ordures',
    name: 'types-dechets',
  },
  {
    label: 'Amiante',
    value: 'amiante',
    id: 'dechets-amiante',
    name: 'types-dechets',
  },
  {
    label: 'Déchets de construction',
    value: 'dechetsConstruction',
    id: 'dechets-construction',
    name: 'types-dechets',
  },
  {
    label: 'Déchets médicaux',
    value: 'dechetsMedicaux',
    id: 'dechets-medicaux',
    name: 'types-dechets',
  },
  {
    label: 'Huiles',
    value: 'huiles',
    id: 'dechets-huiles',
    name: 'types-dechets',
  },
  {
    label: 'Peintures et essences',
    value: 'peinturesEtEssences',
    id: 'dechets-peintures',
    name: 'types-dechets',
  },
  {
    label: 'Textiles',
    value: 'textiles',
    id: 'dechets-textiles',
    name: 'types-dechets',
  },
  {
    label: 'Autre',
    value: 'autre',
    id: 'dechets-autre',
    name: 'types-dechets',
  },
]

export const indicesDisponiblesOptions = [
  {
    label: 'Caméra de vidéo-surveillance',
    value: 'camera',
    id: 'indices-camera',
    name: 'indices-disponibles',
  },
  {
    label: 'Piège photographique',
    value: 'piegePhoto',
    id: 'indices-piege-photo',
    name: 'indices-disponibles',
  },
  {
    label: 'Témoignages',
    value: 'temoignages',
    id: 'indices-temoignages',
    name: 'indices-disponibles',
  },
  {
    label: 'Documents (factures, colis, courriers)',
    value: 'documents',
    id: 'indices-documents',
    name: 'indices-disponibles',
  },
  {
    label: 'Activités liées aux faits constatés',
    value: 'activitesLiees',
    id: 'indices-activites',
    name: 'indices-disponibles',
  },
]

export const yesNoOptions = [
  { label: 'Oui', value: 'oui' },
  { label: 'Non', value: 'non' },
]

export const auteurOptions = [
  { text: 'Sélectionner', value: '', disabled: true },
  { text: 'Le maire', value: 'maire' },
  { text: 'La gendarmerie', value: 'gendarmerie' },
  { text: 'Un agent de police municipale', value: 'police-municipale' },
  { text: "Un agent de l'ONF", value: 'onf' },
  { text: "Un agent de l'OFB", value: 'ofb' },
  { text: 'Autre', value: 'autre' },
]
