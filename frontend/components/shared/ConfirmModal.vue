<template>
  <DsfrModal :opened="opened" :title="title" :actions="modalActions" @close="emit('close')">
    <div class="fr-p-1w">
      <p class="fr-text" v-html="message"></p>
    </div>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    opened: boolean
    title?: string
    message: string
    confirmButtonLabel?: string
    cancelButtonLabel?: string
    isDanger?: boolean
  }>(),
  {
    title: 'Confirmation',
    confirmButtonLabel: 'Confirmer',
    cancelButtonLabel: 'Annuler',
    isDanger: false,
  }
)

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'confirm'): void
}>()

const modalActions = computed(() => [
  {
    label: props.confirmButtonLabel,
    onClick: () => emit('confirm'),
  },
  {
    label: props.cancelButtonLabel,
    secondary: true,
    onClick: () => emit('close'),
  },
])
</script>
