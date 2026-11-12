<template>
  <DsfrModal
    :opened="opened"
    title="Aide à l'évaluation du volume (1 m³ = 1 000 L)"
    size="lg"
    @close="emit('close')"
  >
    <div class="fr-container--fluid fr-p-0">
      <p class="fr-text--sm fr-text-mention--grey fr-mb-2w">
        Sélectionnez une estimation parmi les repères visuels officiels ci-dessous :
      </p>

      <VolumeGuideGrid
        :current-volume-m3="currentVolumeM3"
        @select-volume="handleSelect"
      />
    </div>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import VolumeGuideGrid from './VolumeGuideGrid.vue'

withDefaults(
  defineProps<{
    opened: boolean
    currentVolumeM3?: number | null
  }>(),
  {
    currentVolumeM3: null,
  }
)

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'select-volume', val: number, label: string): void
}>()

const handleSelect = (val: number, label: string) => {
  emit('select-volume', val, label)
  emit('close')
}
</script>
