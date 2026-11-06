<template>
  <div class="assistant-volume-guide fr-mt-2w">
    <button
      type="button"
      class="volume-guide-toggle-btn"
      :aria-expanded="isExpanded"
      @click="isExpanded = !isExpanded"
    >
      <span class="fr-icon-ruler-line fr-icon--sm fr-mr-1w text-primary" aria-hidden="true"></span>
      <span class="guide-toggle-text">
        <strong>Aide visuelle à l'évaluation du volume</strong> (1 m³ = 1 000 L)
      </span>
      <span
        class="fr-icon--sm fr-ml-auto toggle-chevron"
        :class="isExpanded ? 'fr-icon-arrow-up-s-line' : 'fr-icon-arrow-down-s-line'"
        aria-hidden="true"
      ></span>
    </button>

    <div v-if="isExpanded" class="volume-guide-content fr-p-2w fr-mt-1w">
      <p class="fr-text--xs fr-text-mention--grey fr-mb-2w guide-subtitle">
        {{ interactive ? "Cliquez sur une valeur pour l'appliquer au brouillon ou la transmettre dans le chat :" : "Repères officiels de volumétrie utilisés sur la plateforme :" }}
      </p>

      <div class="volume-cards-grid">
        <div
          v-for="cat in volumeReferenceCategories"
          :key="cat.title"
          class="volume-category-card"
        >
          <div class="category-header">
            <span class="category-title">{{ cat.title }}</span>
          </div>

          <ul class="category-items-list">
            <li
              v-for="item in cat.items"
              :key="item.label"
              class="category-item-row"
            >
              <div class="item-name-row">
                <span class="item-label">{{ item.label }}</span>
                <span v-if="item.extra" class="item-extra">({{ item.extra }})</span>
              </div>

              <div class="item-values-row">
                <template v-for="(val, vIdx) in item.values" :key="val">
                  <span v-if="vIdx > 0" class="value-separator">
                    {{ item.separator ?? 'à' }}
                  </span>
                  <button
                    type="button"
                    class="volume-pill-btn"
                    :class="{ 'volume-pill-btn--selected': currentVolumeM3 === val }"
                    :title="`Sélectionner ${val} m³`"
                    @click="onSelect(val, item.label)"
                  >
                    <span class="fr-icon-check-line fr-icon--xs fr-mr-1v" v-if="currentVolumeM3 === val" aria-hidden="true"></span>
                    {{ val }} m³
                  </button>
                </template>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { volumeReferenceCategories } from '@/constants/volumeGuide'

const props = withDefaults(
  defineProps<{
    currentVolumeM3?: number | null
    interactive?: boolean
    defaultExpanded?: boolean
  }>(),
  {
    currentVolumeM3: null,
    interactive: true,
    defaultExpanded: false,
  }
)

const emit = defineEmits<{
  (e: 'select-volume', val: number, label: string): void
}>()

const isExpanded = ref(props.defaultExpanded)

const onSelect = (val: number, label: string) => {
  emit('select-volume', val, label)
}
</script>

<style scoped>
.assistant-volume-guide {
  border: 1px solid var(--border-default-blue-france, #000091);
  background: var(--background-alt-blue-france, #f5f5fe);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.volume-guide-toggle-btn {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.65rem 0.85rem;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  font-size: 0.825rem;
  color: var(--text-title-blue-france, #000091);
  transition: background 0.15s ease;
}

.volume-guide-toggle-btn:hover {
  background: rgba(0, 0, 145, 0.05);
}

.guide-toggle-text {
  line-height: 1.3;
}

.toggle-chevron {
  color: var(--text-title-blue-france, #000091);
}

.volume-guide-content {
  background: var(--background-default-grey, #fff);
  border-top: 1px solid var(--border-contrast-grey, #eee);
}

.guide-subtitle {
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.volume-cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.65rem;
}

@media (min-width: 480px) {
  .volume-cards-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.volume-category-card {
  background: var(--background-contrast-grey, #f6f6f6);
  border-radius: 6px;
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--border-default-grey, #ddd);
}

.category-header {
  margin-bottom: 0.35rem;
}

.category-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-title-grey, #161616);
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.category-items-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item-row {
  padding: 0.3rem 0;
  border-bottom: 1px dashed var(--border-default-grey, #e5e5e5);
}

.category-item-row:last-child {
  border-bottom: none;
}

.item-name-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.2rem;
}

.item-label {
  font-size: 0.75rem;
  color: var(--text-default-grey, #3a3a3a);
}

.item-extra {
  font-size: 0.7rem;
  color: var(--text-mention-grey, #666);
  margin-left: 0.25rem;
}

.item-values-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.3rem;
}

.value-separator {
  font-size: 0.7rem;
  color: var(--text-mention-grey, #888);
}

.volume-pill-btn {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--border-action-high-blue-france, #000091);
  background: #fff;
  color: var(--text-action-high-blue-france, #000091);
  font-size: 0.725rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  line-height: 1.2;
}

.volume-pill-btn:hover {
  background: var(--background-action-low-blue-france, #e3e3fd);
  transform: translateY(-1px);
}

.volume-pill-btn--selected {
  background: var(--background-action-high-blue-france, #000091) !important;
  color: #fff !important;
  border-color: var(--background-action-high-blue-france, #000091) !important;
}
</style>
