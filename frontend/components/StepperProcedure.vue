<template>
  <div class="procedural-stepper">
    <div
      v-for="(step, index) in steps"
      :key="index"
      class="step-item"
      :class="{
        'step--active': currentStep === index,
        'step--completed': step.completed,
        'step--pending': index !== currentStep && !step.completed,
        'step--optional': step.optional,
        'step--locked': step.locked,
      }"
    >
      <div class="step-sidebar">
        <div class="step-icon-container" @click="selectStep(index)">
          <div v-if="step.completed" class="step-icon step-icon--completed">
            <span class="fr-icon-check-line fr-icon--sm" aria-hidden="true"></span>
          </div>
          <div v-else-if="currentStep === index" class="step-icon step-icon--active">
            {{ index }}
          </div>
          <div v-else-if="step.locked" class="step-icon step-icon--locked">
            <span class="fr-icon-lock-line fr-icon--sm" aria-hidden="true"></span>
          </div>
          <div v-else class="step-icon step-icon--pending">
            {{ index }}
          </div>
        </div>
        <div class="step-line"></div>
      </div>

      <div class="step-content">
        <header class="step-header fr-mb-1w" @click="selectStep(index)">
          <div class="step-header-container">
            <h3 class="step-title fr-h6 fr-mb-0" tabindex="-1">{{ step.title }}</h3>
            <div class="step-badges">
              <span
                v-if="step.optional"
                class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon"
                >Optionnel</span
              >
              <span
                v-if="step.completed"
                class="fr-badge fr-badge--sm fr-badge--success fr-badge--no-icon"
                >Fait</span
              >
              <span
                v-else-if="step.locked"
                class="fr-badge fr-badge--sm fr-badge--warning fr-badge--no-icon"
                >En attente des étapes précédentes</span
              >
            </div>
          </div>
          <p v-if="step.description" class="fr-text--xs fr-mb-0 fr-mt-1v fr-text-mention--grey">
            {{ step.description }}
          </p>
        </header>

        <div
          v-if="currentStep === index"
          :key="index"
          class="step-details fr-mt-2w"
          :class="{ 'step-details--locked': step.locked }"
        >
          <slot :name="`step-${index}`" :locked="step.locked"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick } from 'vue'

export interface Step {
  title: string
  description?: string
  completed?: boolean
  optional?: boolean
  locked?: boolean
  showBracket?: boolean
}

const props = defineProps<{
  steps: Step[]
  currentStep: number
}>()

const emit = defineEmits(['update:currentStep'])

const selectStep = async (index: number) => {
  emit('update:currentStep', index)

  await nextTick()

  // Wait a short frame for the accordion content to start rendering/expanding
  window.requestAnimationFrame(() => {
    const activeElement = document.querySelector<HTMLElement>('.step--active')
    if (activeElement) {
      const rect = activeElement.getBoundingClientRect()
      // If the top of the newly opened step is not comfortably in view (e.g. above header or too low)
      const topOffset = 80 // offset to leave comfortable breathing room below sticky header / top
      const targetScrollY = window.scrollY + rect.top - topOffset

      window.scrollTo({
        top: Math.max(0, targetScrollY),
        behavior: 'smooth',
      })
    }
  })
}
</script>

<style scoped>
.procedural-stepper {
  display: flex;
  flex-direction: column;
}

.step-item {
  display: flex;
  scroll-margin-top: 5rem;
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
  background-color: white;
  color: var(--text-active-blue-france);
  border: 1px solid var(--border-active-blue-france);
}

.step-icon--locked {
  background-color: var(--background-contrast-grey);
  color: var(--text-mention-grey);
  border: 1px solid var(--border-default-grey);
}

.step-line {
  flex-grow: 1;
  width: 2px;
  background-color: var(--border-default-grey);
  margin-top: 5px;
  margin-bottom: 5px;
  border-radius: 4px;
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

.step--active .step-header-container {
  display: grid;
  grid-template-rows: auto 1.125rem; /* Reserve space for the badge row */
  gap: 0.25rem;
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
  background-color: white;
  transition: all 0.25s ease-in-out;
}

.step-details--locked {
  position: relative;
  background: linear-gradient(180deg, rgba(246, 246, 246, 0.4) 0%, rgba(240, 242, 248, 0.25) 100%);
  border: 1px dashed var(--border-default-grey);
  border-radius: 12px;
  padding: 1.25rem 1rem 0.5rem 1rem;
}

.step-details--locked::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: repeating-linear-gradient(
    -45deg,
    var(--border-default-grey),
    var(--border-default-grey) 8px,
    transparent 8px,
    transparent 16px
  );
  opacity: 0.6;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}
</style>
