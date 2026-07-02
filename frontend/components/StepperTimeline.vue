<template>
  <div class="bo-stepper">
    <div
      v-for="step in stepCount"
      :key="step"
      class="bo-step"
      :class="{
        'bo-step--completed': currentStep > step,
        'bo-step--active': currentStep === step,
      }"
    >
      <div class="bo-step-num">{{ step }}</div>
      <div class="bo-step-lbl">{{ getStepLabel(step) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getStepLabel } from '@/utils/backoffice'

withDefaults(
  defineProps<{
    currentStep: number
    stepCount?: number
  }>(),
  {
    stepCount: 5,
  }
)
</script>

<style scoped>
.bo-stepper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: var(--background-default-grey);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-default-grey);
  position: relative;
}

.bo-stepper::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 5%;
  right: 5%;
  height: 2px;
  background-color: var(--border-default-grey);
  z-index: 1;
  transform: translateY(-50%);
}

.bo-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  background: var(--background-default-grey);
  padding: 0 10px;
  min-width: 80px;
}

.bo-step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  border: 2px solid var(--border-default-grey);
  color: var(--text-mention-grey);
  transition: all 0.2s ease;
}

.bo-step--completed .bo-step-num {
  background-color: var(--border-active-blue-france);
  border-color: var(--border-active-blue-france);
  color: white;
}

.bo-step--active .bo-step-num {
  border-color: var(--border-active-blue-france);
  color: var(--border-active-blue-france);
  box-shadow: 0 0 0 4px var(--background-alt-blue-france);
}

.bo-step-lbl {
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.35rem;
  color: var(--text-mention-grey);
}

.bo-step--active .bo-step-lbl,
.bo-step--completed .bo-step-lbl {
  color: var(--text-label-grey);
}
</style>
