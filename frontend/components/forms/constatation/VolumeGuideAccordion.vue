<template>
  <DsfrAccordion
    title="Repères d'aide à l'estimation du volume (1 m³ = 1 000 L)"
    title-tag="h4"
  >
    <p class="fr-text--xs fr-text-mention--grey fr-mb-2w">
      Cliquez sur un volume pour le renseigner automatiquement.
    </p>

    <VolumeGuideGrid
      :current-volume-m3="currentVolumeM3"
      @select-volume="(val) => emit('select-volume', val)"
    />
  </DsfrAccordion>
</template>

<script setup lang="ts">
import { DsfrAccordion } from '@gouvminint/vue-dsfr'
import VolumeGuideGrid from '@/components/shared/VolumeGuideGrid.vue'

withDefaults(
  defineProps<{
    currentVolumeM3?: number | null
  }>(),
  {
    currentVolumeM3: null,
  }
)

const emit = defineEmits<{
  (e: 'select-volume', val: number): void
}>()
</script>
