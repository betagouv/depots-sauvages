<template>
  <DsfrModal
    :opened="opened"
    title="Modifier les chiffres clés"
    :is-alert="true"
    @close="$emit('close')"
  >
    <form @submit.prevent="submitForm" class="fr-container--fluid fr-p-0">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div
          v-for="(stat, index) in localStats"
          :key="index"
          class="fr-col-12 fr-col-md-6 fr-mb-2w"
        >
          <div class="stat-edit-card fr-p-2w">
            <h3 class="fr-text--lead fr-mb-1w">Chiffre {{ index + 1 }}</h3>
            <div class="fr-input-group fr-mb-2w">
              <label class="fr-label" :for="'stat-number-' + index">Nombre / Valeur</label>
              <input
                v-model="stat.number"
                class="fr-input"
                type="text"
                :id="'stat-number-' + index"
                required
                placeholder="Ex: 600 m³"
              />
            </div>
            <div class="fr-input-gbackend/site_content/backend/site_content/roup fr-mb-0">
              <label class="fr-label" :for="'stat-label-' + index">Description</label>
              <input
                v-model="stat.label"
                class="fr-input"
                type="text"
                :id="'stat-label-' + index"
                required
                placeholder="Ex: de déchets retirés"
              />
            </div>
          </div>
        </div>

        <div class="fr-col-12 fr-mt-3w text-right">
          <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
            <li>
              <button type="button" class="fr-btn fr-btn--secondary" @click="$emit('close')">
                Annuler
              </button>
            </li>
            <li>
              <button type="submit" class="fr-btn">Enregistrer</button>
            </li>
          </ul>
        </div>
      </div>
    </form>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import { ref, watch } from 'vue'

interface StatItem {
  number: string
  label: string
}

const props = defineProps<{
  opened: boolean
  stats: StatItem[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', stats: StatItem[]): void
}>()

const localStats = ref<StatItem[]>([])

watch(
  () => props.opened,
  (isOpened) => {
    if (isOpened) {
      // Deep copy to avoid mutating props
      localStats.value = props.stats.map((s) => ({ ...s }))
    }
  },
  { immediate: true }
)

const submitForm = () => {
  emit('save', localStats.value)
}
</script>

<style scoped>
.stat-edit-card {
  border: 1px solid var(--border-default-grey);
  border-radius: 4px;
  background-color: var(--background-alt-grey);
}
</style>
