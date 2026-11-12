<template>
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
          <div class="volume-guide-item-header">
            <span class="volume-guide-label">{{ item.label }}</span>
            <span v-if="item.extra" class="volume-extra">
              ({{ item.extra }})
            </span>
          </div>
          <div class="volume-guide-values">
            <template v-for="(val, vIdx) in item.values" :key="val">
              <span v-if="vIdx > 0" class="volume-separator">
                {{ item.separator ?? 'à' }}
              </span>
              <button
                type="button"
                class="fr-tag fr-tag--sm volume-tag"
                :class="{ 'volume-tag--selected': currentVolumeM3 === val }"
                :title="`Sélectionner ${val} m³`"
                @click="emit('select-volume', val, item.label)"
              >
                <span
                  v-if="currentVolumeM3 === val"
                  class="fr-icon-check-line fr-icon--xs fr-mr-1v text-primary"
                  aria-hidden="true"
                ></span>
                {{ val }} m³
              </button>
            </template>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { volumeReferenceCategories } from '@/constants/volumeGuide'

withDefaults(
  defineProps<{
    currentVolumeM3?: number | null
  }>(),
  {
    currentVolumeM3: null,
  }
)

const emit = defineEmits<{
  (e: 'select-volume', val: number, label: string): void
}>()
</script>

<style scoped>
.volume-guide-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.volume-guide-category {
  background-color: var(--background-contrast-grey, #f6f6f6);
  border-radius: 6px;
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
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--border-default-grey, #e5e5e5);
}

.volume-guide-item:last-child {
  border-bottom: none;
}

.volume-guide-item-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.volume-guide-label {
  font-size: 0.875rem;
  color: var(--text-default-grey, #161616);
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
  color: var(--text-mention-grey, #666666);
  display: inline-flex;
  align-items: center;
  margin: 0 0.15rem;
}

.volume-extra {
  font-size: 0.75rem;
  color: var(--text-mention-grey, #666666);
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

.volume-tag--selected {
  background-color: var(--background-action-low-blue-france, #e3e3fd) !important;
  color: var(--text-action-high-blue-france, #000091) !important;
  font-weight: 600;
  border: 1px solid var(--border-action-high-blue-france, #000091);
}
</style>
