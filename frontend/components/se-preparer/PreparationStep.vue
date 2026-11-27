<template>
  <div class="preparation-step fr-py-3w">
    <DsfrCheckbox
      :id="`etape-${step.id}`"
      :name="`etape-${step.id}`"
      :label="step.label"
      :model-value="done"
      @update:model-value="(value: boolean) => emit('update:done', value)"
    />
    <div class="preparation-step__content">
      <p v-if="step.description" class="fr-text--sm fr-mt-1w fr-mb-1w">{{ step.description }}</p>
      <PreparationResourceLink :link="step.link" class="fr-mt-1w" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCheckbox } from '@gouvminint/vue-dsfr'
import PreparationResourceLink from '@/components/se-preparer/PreparationResourceLink.vue'
import type { PreparationStep } from '@/constants/preparation-steps'

defineProps<{
  step: PreparationStep
  done: boolean
}>()

const emit = defineEmits<{
  'update:done': [value: boolean]
}>()
</script>

<style scoped>
.preparation-step + .preparation-step {
  border-top: 1px solid var(--border-default-grey);
}
/* Aligns the description and link with the checkbox label rather than the box. */
.preparation-step__content {
  padding-left: 2rem;
}
</style>
