<template>
  <DsfrAccordion
    title="Repères d'aide à l'estimation du volume (1 m³ = 1 000 L)"
    title-tag="h4"
  >
    <p class="fr-text--xs fr-text-mention--grey fr-mb-2w">
      Cliquez sur un volume pour le renseigner automatiquement.
    </p>

    <div class="volume-guide-grid">
      <div
        v-for="cat in volumeReferenceCategories"
        :key="cat.title"
        class="volume-guide-category"
      >
        <h5 class="fr-text--sm fr-text--bold fr-mb-1w fr-mt-0">
          {{ cat.title }}
        </h5>
        <ul class="volume-guide-list">
          <li
            v-for="item in cat.items"
            :key="item.label"
            class="volume-guide-item"
          >
            <span class="volume-guide-label">{{ item.label }}</span>
            <div class="volume-guide-values">
              <template v-for="(val, vIdx) in item.values" :key="val">
                <span v-if="vIdx > 0" class="volume-separator">
                  {{ item.separator ?? 'à' }}
                </span>
                <button
                  type="button"
                  class="fr-tag fr-tag--sm volume-tag"
                  :title="`Appliquer ${val} m³`"
                  @click="emit('select-volume', val)"
                >
                  {{ val }} m³
                </button>
              </template>
              <span v-if="item.extra" class="volume-extra">
                ({{ item.extra }})
              </span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </DsfrAccordion>
</template>

<script setup lang="ts">
import { DsfrAccordion } from '@gouvminint/vue-dsfr'

interface VolumeItem {
  label: string
  values: number[]
  extra?: string
  separator?: string
}

interface VolumeCategory {
  title: string
  items: VolumeItem[]
}

const emit = defineEmits<{
  (e: 'select-volume', val: number): void
}>()

const volumeReferenceCategories: VolumeCategory[] = [
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
</script>

<style scoped>
.volume-guide-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.volume-guide-category {
  background-color: var(--background-contrast-grey);
  border-radius: 4px;
  padding: 0.75rem 1rem;
}

.volume-guide-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.volume-guide-item {
  display: flex;
  flex-direction: column;
  padding: 0.35rem 0;
  border-bottom: 1px solid var(--border-default-grey);
}

.volume-guide-item:last-child {
  border-bottom: none;
}

.volume-guide-label {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  color: var(--text-default-grey);
}

.volume-guide-values {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.35rem;
}

.volume-separator {
  font-size: 0.75rem;
  line-height: 1.5rem;
  color: var(--text-mention-grey);
  display: inline-flex;
  align-items: center;
  margin: 0 0.15rem;
}

.volume-extra {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  margin-left: 0.25rem;
}

.volume-tag {
  margin: 0 !important;
  cursor: pointer;
  transition: background-color 0.15s ease, transform 0.1s ease;
  user-select: none;
}

.volume-tag:hover {
  background-color: var(--background-action-low-blue-france-hover, #dbe1f7);
  transform: translateY(-1px);
}

.volume-tag:active {
  transform: translateY(0);
}
</style>
