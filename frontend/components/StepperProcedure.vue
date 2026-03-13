<template>
  <div class="procedural-stepper">
    <div
      v-for="(step, index) in steps"
      :key="index"
      class="step-item"
      :class="{
        'step--active': currentStep === index,
        'step--completed': index < currentStep,
        'step--pending': index > currentStep,
        'step--optional': step.optional,
      }"
    >
      <div class="step-sidebar">
        <div class="step-icon-container" @click="$emit('update:currentStep', index)">
          <div v-if="currentStep === index" class="step-icon step-icon--active">
            {{ index + 1 }}
          </div>
          <div v-else class="step-icon step-icon--pending">
            {{ index + 1 }}
          </div>
        </div>
        <div v-if="index < steps.length - 1" class="step-line"></div>
      </div>

      <div class="step-content">
        <header class="step-header fr-mb-1w" @click="$emit('update:currentStep', index)">
          <div class="step-header-container">
            <h3 class="step-title fr-h6 fr-mb-0">{{ step.title }}</h3>
            <div class="step-badges">
              <span
                v-if="step.optional"
                class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon"
                >Optionnel</span
              >
              <span
                v-if="currentStep === index"
                class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon"
                >En cours</span
              >
            </div>
          </div>
          <p class="fr-text--xs fr-mb-0 fr-mt-1v fr-text-mention--grey">{{ step.description }}</p>
        </header>

        <transition name="expand">
          <div v-if="currentStep === index" class="step-details fr-mt-2w">
            <slot :name="`step-${index}`"></slot>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface Step {
  title: string
  description: string
  optional?: boolean
}

defineProps<{
  steps: Step[]
  currentStep: number
}>()

defineEmits(['update:currentStep'])
</script>

<style scoped>
.procedural-stepper {
  display: flex;
  flex-direction: column;
}

.step-item {
  display: flex;
  gap: 1.25rem;
}

.step-sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  width: 28px;
}

.step-icon-container {
  z-index: 1;
  cursor: pointer;
  margin-top: 0.25rem; /* Align with title text better */
}

.step-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.step-icon--completed {
  background-color: var(--background-flat-success);
  color: var(--text-inverted-grey);
}

.step-icon--active {
  background-color: var(--background-active-blue-france);
  color: var(--text-inverted-grey);
  box-shadow: 0 0 0 4px var(--background-active-blue-france-hover);
  transform: scale(1.1);
}

.step-icon--pending {
  background-color: var(--background-alt-grey);
  color: var(--text-mention-grey);
  border: 1px solid var(--border-default-grey);
}

.step-line {
  flex-grow: 1;
  width: 2px;
  background-color: var(--border-default-grey);
  margin-top: 5px;
  margin-bottom: 5px;
}

.step--active .step-line {
  background-color: var(--border-active-blue-france);
}

.step-content {
  flex-grow: 1;
  padding-bottom: 2.5rem;
}

.step-header {
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  margin-left: -0.75rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.step-header:hover {
  background-color: var(--background-alt-blue-france);
}

.step-title {
  color: var(--text-title-grey);
  font-size: 1.125rem;
  line-height: normal;
}

.step-header-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  width: 100%;
}

.step-badges {
  display: flex;
  gap: 0.5rem;
}

.step--active .step-title {
  color: var(--text-active-blue-france);
  font-weight: 700;
}

.step-details {
  border-radius: 12px;
  border-left: 3px solid var(--border-active-blue-france);
  background-color: white;
  padding-left: 1.5rem;
}

/* Transitions */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 1000px;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}
</style>
