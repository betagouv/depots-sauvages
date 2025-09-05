export const STEPS = [
  'Information sur le dépôt sauvage',
  'Description du dépôt',
  'Compléter les informations utiles pour le traitement',
  'Vos coordonnées',
  'Bravo ! Vous pouvez lancer la procédure',
]

export const volumeOptions = [
  { text: 'Sélectionner une option', value: '', disabled: true },
  { text: 'Moins de 1m³', value: 'moins de 1m³' },
  { text: 'Entre 1 et 3m³', value: 'entre 1 et 3m³' },
  { text: 'Plus de 3m³', value: 'plus de 3m³' },
]

export const natureTerrainOptions = [
  {
    label: 'Terrain public',
    value: 'terrain public',
    id: 'terrain-public',
  },
  {
    label: 'Forêt domaniale',
    value: 'forêt domaniale',
    id: 'terrain-foret-domaniale',
  },
  {
    label: 'Terrain privé',
    value: 'terrain privé',
    id: 'terrain-prive',
  },

  {
    label: 'Je ne sais pas',
    value: 'inconnu',
    id: 'terrain-inconnu',
  },
]

export const typesDepotOptions = [
  {
    label: 'Amiante',
    value: 'amiante',
    id: 'dechets-amiante',
    name: 'types-dechets',
  },
  {
    label: 'Carrelage',
    value: 'carrelage',
    id: 'depot-carrelage',
    name: 'types-depot',
  },
  {
    label: 'Déchets automobiles',
    value: 'déchets automobiles',
    id: 'dechets-automobile',
    name: 'types-dechets',
  },
  {
    label: 'Déchets de construction',
    value: 'déchets de construction',
    id: 'dechets-construction',
    name: 'types-dechets',
  },
  {
    label: 'Déchets électriques et électroniques',
    value: 'déchets électriques et électroniques',
    id: 'dechets-electriques-electroniques',
    name: 'types-dechets',
  },
  {
    label: 'Déchets médicaux',
    value: 'déchets médicaux',
    id: 'dechets-medicaux',
    name: 'types-dechets',
  },
  {
    label: 'Déchets verts',
    value: 'déchets verts',
    id: 'dechets-verts',
    name: 'types-dechets',
  },
  {
    label: 'Électroménager',
    value: 'électroménager',
    id: 'dechets-electromenager',
    name: 'types-dechets',
  },
  {
    label: 'Encombrants',
    value: 'encombrants',
    id: 'dechets-encombrants',
    name: 'types-dechets',
  },
  {
    label: 'Gravats',
    value: 'gravats',
    id: 'dechets-gravats',
    name: 'types-dechets',
  },
  {
    label: 'Huiles',
    value: 'huiles',
    id: 'dechets-huiles',
    name: 'types-dechets',
  },
  {
    label: 'Ordures ménagères',
    value: 'ordures ménagères',
    id: 'dechets-ordures',
    name: 'types-dechets',
  },
  {
    label: 'Peintures et essences',
    value: 'peintures et essences',
    id: 'dechets-peintures',
    name: 'types-dechets',
  },
  {
    label: 'Pneus',
    value: 'pneus',
    id: 'dechets-pneus',
    name: 'types-dechets',
  },
  {
    label: 'Textiles',
    value: 'textiles',
    id: 'dechets-textiles',
    name: 'types-dechets',
  },
  {
    label: 'Tuiles',
    value: 'tuiles',
    id: 'depot-tuiles',
    name: 'types-depot',
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
    label: 'Pièges photographiques',
    value: 'pièges photographiques',
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
    label: 'Documents (factures, colis, courriers, etc.)',
    value: 'documents (factures, colis, courriers, etc.)',
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

export const statutAuteurOptions = [
  { label: 'ENTREPRISE', value: 'entreprise' },
  { label: 'PARTICULIER', value: 'particulier' },
]

export const auteurOptions = [
  { text: 'Sélectionner', value: '', disabled: true },
  { text: 'Le maire', value: 'le maire' },
  { text: "Un agent de l'ONF", value: "un agent de l'ONF" },
  { text: 'La gendarmerie', value: 'la gendarmerie' },
  {
    text: 'Un agent assermenté (policier municipal, garde-champêtre, etc.)',
    value: 'un agent assermenté',
  },
  { text: 'Un autre agent de la mairie', value: 'un autre agent de la mairie' },
  { text: 'Autre', value: 'autre' },
]
