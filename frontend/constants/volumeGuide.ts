export interface VolumeItem {
  label: string
  values: number[]
  extra?: string
  separator?: string
}

export interface VolumeCategory {
  title: string
  items: VolumeItem[]
}

export const volumeReferenceCategories: VolumeCategory[] = [
  {
    title: 'Petits contenants & ménager',
    items: [
      { label: 'Sac poubelle standard', values: [0.1], extra: '100 L' },
      { label: 'Bac roulant (120 / 240 / 660 L)', values: [0.12, 0.24, 0.66], separator: '/' },
      { label: 'Bac d’immeuble (1 100 L)', values: [1.1] },
    ],
  },
  {
    title: 'Mobilier & Électroménager',
    items: [
      { label: 'Réfrigérateur, lave-linge', values: [0.3, 0.5] },
      { label: 'Matelas 2 places', values: [0.5, 1.0] },
      { label: 'Canapé 3 places', values: [1.5, 2.5] },
      { label: 'Palette chargée en hauteur', values: [1.0] },
    ],
  },
  {
    title: 'Véhicules légers',
    items: [
      { label: 'Coffre de voiture', values: [0.3, 0.5] },
      { label: 'Remorque de voiture', values: [1.0, 2.0] },
      { label: 'Utilitaire léger', values: [3.0, 7.0] },
    ],
  },
  {
    title: 'Gros volumes & Bennes',
    items: [
      { label: 'Fourgon', values: [8.0, 16.0] },
      { label: 'Camion de déménagement', values: [20.0] },
      { label: 'Benne ou caisson amovible', values: [8.0, 15.0, 30.0], separator: ',' },
      { label: 'Semi-remorque', values: [80.0, 100.0] },
    ],
  },
]
