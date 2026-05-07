<template>
  <DsfrRadioButtonSet
    v-model="stringValue"
    :legend="legend"
    :required="required"
    :error-message="errorMessage"
    :inline="inline"
    :options="[
      { label: 'Oui', value: 'oui', id: `${idPrefix}-oui` },
      { label: 'Non', value: 'non', id: `${idPrefix}-non` },
    ]"
  />
</template>

<script setup lang="ts">
import { DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const props = defineProps<{
  modelValue?: boolean | null
  legend: string
  idPrefix: string
  required?: boolean
  errorMessage?: string
  inline?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const stringValue = computed({
  get: () => {
    if (props.modelValue === true) return 'oui'
    if (props.modelValue === false) return 'non'
    return undefined
  },
  set: (val: string | undefined) => {
    emit('update:modelValue', val === 'oui')
  },
})
</script>
