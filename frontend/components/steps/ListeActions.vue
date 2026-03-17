<template>
  <div class="action-list fr-mt-2w">
    <div class="action-checkboxes">
      <div
        v-for="(action, index) in actions"
        :key="index"
        class="action-item fr-checkbox-group fr-checkbox-group--sm"
      >
        <input
          type="checkbox"
          :id="`action-${stepId}-${index}`"
          :checked="action.completed"
          disabled
        />
        <label class="fr-label fr-display-flex fr-flex-center" :for="`action-${stepId}-${index}`">
          {{ action.label }}
          <span
            v-if="action.icon"
            :class="[action.icon, 'fr-ml-1w', 'action-icon']"
            aria-hidden="true"
          ></span>
        </label>
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

.action-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-left: 1.5rem;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  border-left: 3px solid var(--border-active-blue-france);
  border-radius: 12px;
}

.action-item {
  margin-bottom: 0 !important;
  padding: 0.75rem 1rem;
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.action-item:hover {
  background-color: var(--background-alt-grey-hover);
  border-color: var(--border-default-blue-france);
}

.action-item .fr-label {
  margin-bottom: 0;
  cursor: pointer;
}

.action-item input[type='checkbox']:disabled + .fr-label {
  cursor: default;
  color: var(--text-default-grey);
}

.action-item input[type='checkbox']:disabled {
  cursor: default;
}

.action-icon {
  font-size: 0.9rem;
  color: var(--text-active-blue-france);
}
</style>
