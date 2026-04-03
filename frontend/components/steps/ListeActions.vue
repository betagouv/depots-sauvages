<template>
  <div class="action-list fr-mt-2w">
    <div class="action-bracket fr-pl-3w fr-py-1v">
      <div v-for="(action, index) in actions" :key="index" class="action-row">
        <div
          class="action-item fr-display-flex fr-p-2w"
          :class="{ 'is-completed': action.completed, 'is-readonly': action.readonly }"
        >
          <DsfrCheckbox
            v-if="!action.readonly"
            :model-value="action.completed"
            :name="`${stepId}-action-${index}`"
            @update:model-value="(val: boolean) => $emit('updateCase', action, val)"
          >
            <template #label>
              <span class="action-label" v-html="action.label"></span>
              <span
                v-if="action.icon"
                :class="[action.icon, 'fr-ml-1w', 'extra-icon']"
                aria-hidden="true"
              ></span>
            </template>
          </DsfrCheckbox>

          <div v-else class="fr-display-flex fr-align-items-center">
            <span class="fr-icon-checkbox-circle-line fr-mr-1w action-icon" aria-hidden="true"></span>
            <span class="action-label" v-html="action.label"></span>
          </div>
        </div>

        <transition name="slide-up">
          <div v-if="action.completed && $slots[`extra-${index}`]" class="action-details fr-p-3w">
            <slot :name="`extra-${index}`"></slot>
          </div>
        </transition>
      </div>
    </div>

    <div v-if="$slots.actions" class="fr-mt-3w fr-display-flex fr-gap-1w fr-flex-wrap">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface Action {
  label: string
  completed?: boolean
  readonly?: boolean
  icon?: string
}

defineProps<{
  stepId: string
  actions: Action[]
}>()

defineEmits(['updateCase'])
</script>

<style scoped>
.action-list {
  display: flex;
  flex-direction: column;
}

.action-bracket {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  border-left: 3px solid var(--border-active-blue-france);
  border-radius: 12px;
}

.action-row {
  display: flex;
  flex-direction: column;
}

.action-item {
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out;
  border: 1px solid transparent;
}

.action-item:hover {
  background-color: var(--background-alt-grey-hover);
  border-color: var(--border-default-blue-france);
}

.action-item.is-completed {
  background-color: var(--background-alt-blue-france);
}

.action-details {
  margin-top: -0.5rem;
  margin-left: 2.5rem;
  background-color: var(--background-alt-grey);
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  border-top: 1px dashed var(--border-default-grey);
  border-left: 2px solid var(--border-default-blue-france);
}

.action-label {
  font-weight: 500;
  color: var(--text-label-grey);
}

.is-completed .action-label {
  color: var(--text-active-blue-france);
}

.action-icon {
  color: var(--text-active-blue-france);
  flex-shrink: 0;
}

.extra-icon {
  font-size: 0.9rem;
  color: var(--text-mention-grey);
}

/* Round Checkboxes Override */
:deep(.fr-checkbox-group input[type='checkbox'] + label::before) {
  border-radius: 50% !important;
  box-shadow: inset 0 0 0 1px var(--border-action-high-blue-france) !important;
}

:deep(.fr-checkbox-group input[type='checkbox']:checked + label::before) {
  background-color: var(--background-active-blue-france) !important;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23fff' d='M10 15.17l-3.29-3.3a1 1 0 00-1.42 1.41l4 4a1 1 0 001.42 0l8-8a1 1 0 10-1.42-1.41L10 15.17z'/%3E%3C/svg%3E") !important;
  background-size: 1rem !important;
  background-position: center !important;
  box-shadow: none !important;
}

:deep(.fr-checkbox-group input[type='checkbox']:checked + label::after) {
  display: none !important;
}

:deep(.fr-checkbox-group input[type='checkbox'] + label) {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

/* Transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease-out;
  max-height: 500px;
  opacity: 1;
}

.slide-up-enter-from,
.slide-up-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
