<template>
  <div class="fr-container--sm fr-mb-3w">
    <DsfrStepper
      :title="'Signalement d\'un dépôt sauvage'"
      :steps="STEPS"
      :current-step="store.currentStep"
    />

    <div class="fr-container--fluid" :class="{ 'fr-text--center': isLastStep }">
      <div class="fr-container--sm">
        <Step1 v-if="store.currentStep === 1" />
        <Step2 v-if="store.currentStep === 2" />
        <Step3 v-if="store.currentStep === 3" @restart="resetForm" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useScroll } from '@/composables/useScroll'
import { computed, watch } from 'vue'
import { useSignalementStore } from '../stores/signalement'
import { STEPS } from './form-steps/form-data'
import Step1 from './form-steps/step-1.vue'
import Step2 from './form-steps/step-2.vue'
import Step3 from './form-steps/step-3.vue'

const store = useSignalementStore()
const isLastStep = computed(() => store.currentStep === STEPS.length)
const { scrollToTop } = useScroll()

// Watch for step changes and scroll to top
watch(
  () => store.currentStep,
  () => {
    scrollToTop()
  }
)

const resetForm = () => {
  store.resetStore()
  scrollToTop()
}

defineEmits(['stepChange'])
</script>

<style scoped></style>
