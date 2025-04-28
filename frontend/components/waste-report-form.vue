<template>
  <div class="waste-report">
    <DsfrStepper
      :title="'Signalement d\'un dépôt sauvage'"
      :steps="STEPS"
      :current-step="store.currentStep"
    />

    <div class="form-wrapper" :class="{ 'confirmation-step': isLastStep }">
      <div class="form-content">
        <Step1 v-if="store.currentStep === 1" />
        <Step2 v-if="store.currentStep === 2" />
        <Step3 v-if="store.currentStep === 3" @restart="resetForm" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSignalementStore } from '../stores/signalement'
import { STEPS } from './form-steps/form-data'
import Step1 from './form-steps/step-1.vue'
import Step2 from './form-steps/step-2.vue'
import Step3 from './form-steps/step-3.vue'

const store = useSignalementStore()
const isLastStep = computed(() => store.currentStep === STEPS.length)

const resetForm = () => {
  store.resetStore()
}

defineEmits(['stepChange'])
</script>

<style scoped>
.waste-report {
  margin: 0 auto 2rem;
  padding: 0 1rem;
}

.form-wrapper {
  margin: 0;
  max-width: 800px;
}

.form-content {
  min-height: 200px;
  margin: 2rem 0;
}

.confirmation-step {
  text-align: center;
}

.success-icon {
  color: var(--text-default-success);
  margin-bottom: 1rem;
  font-size: 2rem;
}

@media (min-width: 768px) {
  .waste-report {
    padding: 0;
  }
}
</style>
