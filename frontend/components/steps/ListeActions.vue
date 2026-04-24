<template>
  <div class="action-list fr-mt-2w">
    <div class="premium-action-bracket fr-py-1w">
      <div v-for="(action, index) in actions" :key="index" class="action-row">
        <div class="premium-action-item" :class="{ 'is-completed': action.completed }">
          <DsfrCheckbox
            v-if="!action.readonly"
            :model-value="action.completed"
            :name="`${stepId}-action-${index}`"
            class="premium-action-content"
            @update:model-value="(val: boolean) => $emit('update-case', action, val)"
          >
            <template #label>
              <div class="fr-display-flex fr-align-items-center fr-ml-1w">
                <span class="action-label" v-html="action.label"></span>
                <span
                  v-if="action.icon"
                  :class="[action.icon, 'fr-ml-1w', 'extra-icon']"
                  aria-hidden="true"
                ></span>
              </div>
            </template>
          </DsfrCheckbox>

          <div v-else class="premium-action-readonly">
            <span
              class="fr-icon-checkbox-circle-line fr-mr-1w action-icon"
              aria-hidden="true"
            ></span>
            <span class="action-label" v-html="action.label"></span>
          </div>
        </div>

        <transition name="slide-up">
          <div
            v-if="action.completed && ($slots[`extra-${action.id}`] || $slots[`extra-${index}`])"
            class="action-details fr-p-3w"
          >
            <slot :name="action.id ? `extra-${action.id}` : `extra-${index}`"></slot>
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
  id?: string
  label: string
  completed?: boolean
  readonly?: boolean
  icon?: string
}

defineProps<{
  stepId: string
  actions: Action[]
}>()

defineEmits(['update-case'])
</script>

<style scoped>
.action-row {
  display: flex;
  flex-direction: column;
}

.action-details {
  margin-top: -1px;
  margin-left: 1.5rem; /* Center of the checkbox: 0.75 (left) + 0.75 (half width) */
  padding-left: 1rem !important; /* Content offset: 2.5 - 1.5 = 1.0 */
  border-left: 2px solid var(--border-default-blue-france);
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
