<template>
  <div class="premium-choices-container fr-mt-2w fr-p-2w" :class="{ 'is-disabled-choices': disabled }">
    <h5 v-if="legend" class="fr-h5 fr-mb-3w text-center">{{ legend }}</h5>

    <div :class="layoutClass">
      <div
        v-for="option in options"
        :key="option.value"
        :class="[
          itemWrapperClass,
          'premium-choice-card',
          { 'choice-active': modelValue === option.value },
        ]"
      >
        <DsfrCheckbox
          :name="option.id"
          :model-value="modelValue === option.value"
          :disabled="disabled"
          @update:modelValue="toggle(option.value)"
        >
          <template #label>
            <span class="fr-ml-1w">{{ option.label }}</span>
          </template>
        </DsfrCheckbox>
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
  disabled?: boolean
}>()

const emit = defineEmits(['update:modelValue'])

const layoutClass = computed(() => {
  return props.layout === 'list'
    ? 'premium-choices-list'
    : 'fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-grid-row--stretch'
})

const itemWrapperClass = computed(() => {
  return props.layout === 'list' ? '' : 'fr-col-12 fr-col-md-6'
})

const toggle = (val: any) => {
  if (props.disabled) return
  const newValue = props.modelValue === val ? '' : val
  emit('update:modelValue', newValue)
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
.is-disabled-choices {
  opacity: 0.72;
}

.is-disabled-choices :deep(.premium-choice-card .fr-checkbox-group) {
  background-color: var(--background-alt-grey) !important;
  border-color: var(--border-default-grey) !important;
  box-shadow: none !important;
  cursor: not-allowed !important;
}
</style>
