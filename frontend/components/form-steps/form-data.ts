export const STEPS = [
  'Information sur le dépôt de déchets',
  'Procédure et préjudice',
  'Et maintenant ?',
]

export const volumeOptions = [
  { text: 'Sélectionner une option', value: '', disabled: true },
  { text: 'Moins de 1m³', value: 'Moins de 1m³' },
  { text: 'Entre 1 et 3m³', value: 'Entre 1 et 3m³' },
  { text: 'Plus de 3m³', value: 'Plus de 3m³' },
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
    value: 'déchets verts',
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
    value: 'électroménager',
    id: 'dechets-electromenager',
    name: 'types-dechets',
  },
  {
    label: 'Ordures ménagères',
    value: 'ordures ménagères',
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
    value: 'déchets de construction',
    id: 'dechets-construction',
    name: 'types-dechets',
  },
  {
    label: 'Déchets médicaux',
    value: 'déchets médicaux',
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
    value: 'peintures et essences',
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
    value: 'caméra de vidéo-surveillance',
    id: 'indices-camera',
    name: 'indices-disponibles',
  },
  {
    label: 'Piège photographique',
    value: 'piège photographique',
    id: 'indices-piege-photo',
    name: 'indices-disponibles',
  },
  {
    label: 'Témoignages',
    value: 'témoignages',
    id: 'indices-temoignages',
    name: 'indices-disponibles',
  },
  {
    label: 'Documents (factures, colis, courriers)',
    value: 'documents (factures, colis, courriers)',
    id: 'indices-documents',
    name: 'indices-disponibles',
  },
  {
    label: 'Activités liées aux faits constatés',
    value: 'activités liées aux faits constatés',
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
  { text: 'Le maire', value: 'le maire' },
  { text: 'La gendarmerie', value: 'la gendarmerie' },
  { text: 'Un agent de police municipale', value: 'un agent de police municipale' },
  { text: "Un agent de l'ONF", value: "un agent de l'ONF" },
  { text: "Un agent de l'OFB", value: "un agent de l'OFB" },
  { text: 'Autre', value: 'autre' },
]
