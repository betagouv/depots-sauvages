<template>
  <button
    type="button"
    :class="[
      'fr-btn',
      variant === 'secondary' ? 'fr-btn--secondary' : '',
      size === 'sm' ? 'fr-btn--sm' : '',
      size === 'lg' ? 'fr-btn--lg' : '',
      icon ? `${icon} fr-btn--icon-left` : '',
    ]"
    @click="openPopup"
  >
    {{ label }}
  </button>
</template>

<script setup lang="ts">
import { openTallyPopup, type TallyPopupOptions } from '@/utils/tally'

const props = withDefaults(
  defineProps<{
    formId: string
    label: string
    variant?: 'primary' | 'secondary'
    size?: 'sm' | 'md' | 'lg'
    icon?: string
    tallyOptions?: TallyPopupOptions
    trackingCategory?: string
    trackingAction?: string
    trackingName?: string
  }>(),
  {
    variant: 'primary',
    size: 'md',
    icon: '',
    tallyOptions: () => ({ layout: 'modal', width: 900 }),
  }
)

const openPopup = () => {
  if (props.trackingCategory && props.trackingAction) {
    if (typeof window !== 'undefined' && (window as any)._paq) {
      const eventArgs = ['trackEvent', props.trackingCategory, props.trackingAction]
      if (props.trackingName) {
        eventArgs.push(props.trackingName)
      }
      ;(window as any)._paq.push(eventArgs)
    }
  }

  openTallyPopup(props.formId, {
    layout: 'modal', // Force layout modal pour une bonne UX
    ...props.tallyOptions,
  })
}
</script>

<style scoped></style>
