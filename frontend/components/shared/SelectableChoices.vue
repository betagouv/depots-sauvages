<template>
  <div class="selectable-choices decision-outcome fr-p-3w">
    <h5 v-if="legend" class="fr-h5 fr-mb-3w text-center">{{ legend }}</h5>
    
    <div :class="layoutClass">
      <div
        v-for="option in options"
        :key="option.value"
        :class="[itemWrapperClass, 'choice-item']"
      >
        <DsfrCheckbox
          :name="option.id"
          :label="option.label"
          :model-value="modelValue === option.value"
          class="choice-checkbox"
          :class="{ 'choice-checkbox--active': modelValue === option.value }"
          @update:modelValue="toggle(option.value)"
        />
      </div>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option {
  id: string
  label: string
  value: any
}

const props = defineProps<{
  options: Option[]
  modelValue: any
  legend?: string
  layout?: 'grid' | 'list'
}>()

const emit = defineEmits(['update:modelValue'])

const layoutClass = computed(() => {
  return props.layout === 'list' 
    ? 'choices-list' 
    : 'fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-grid-row--stretch'
})

const itemWrapperClass = computed(() => {
  return props.layout === 'list' ? '' : 'fr-col-12 fr-col-md-6'
})

const toggle = (val: any) => {
  const newValue = props.modelValue === val ? '' : val
  emit('update:modelValue', newValue)
}
</script>

<style scoped>
.choice-item {
  cursor: pointer;
}
.selectable-choices {
  display: block;
  width: 100%;
}

.decision-outcome {
  background-color: var(--background-alt-blue-france);
  border-radius: 12px;
  border: 1px solid var(--border-default-blue-france);
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
}

.text-center {
  text-align: center;
}

/* Layout List */
.choices-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Target the checkbox group container from DSFR */
:deep(.fr-checkbox-group) {
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-default-grey) !important;
  border-radius: 8px;
  margin-bottom: 0 !important;
  transition: all 0.2s ease;
  height: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

:deep(.fr-checkbox-group:hover) {
  background-color: var(--background-alt-grey-hover) !important;
}

/* Make the label cover the whole area */
:deep(.fr-checkbox-group label) {
  width: 100%;
  height: 100%;
  margin-bottom: 0;
  cursor: pointer;
  padding: 1rem 1.5rem 1rem 3.5rem !important; /* Adjust padding to leave space for the actual checkbox */
  display: flex;
  align-items: center;
}

/* Position the check mark correctly since we added padding to the label */
:deep(.fr-checkbox-group input[type='checkbox'] + label::before) {
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
}

/* Active State */
.choice-checkbox--active :deep(.fr-checkbox-group) {
  background-color: var(--background-alt-blue-france) !important;
  border-color: var(--border-default-blue-france) !important;
  box-shadow: inset 0 0 0 1px var(--border-default-blue-france);
}

.choice-checkbox--active :deep(label) {
  font-weight: bold;
  color: var(--text-label-blue-france);
}
</style>
