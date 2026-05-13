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
    @click="handleClick"
  >
    {{ label }}
  </button>
</template>

<script setup lang="ts">
import { openTallyPopup, type TallyPopupOptions } from '@/utils/tally'
import { useRouter } from 'vue-router'

const props = withDefaults(
  defineProps<{
    formId: string
    label: string
    variant?: 'primary' | 'secondary'
    size?: 'sm' | 'md' | 'lg'
    icon?: string
    to?: string
    tallyOptions?: TallyPopupOptions
  }>(),
  {
    variant: 'primary',
    size: 'md',
    icon: '',
    tallyOptions: () => ({ layout: 'modal', width: 900 }),
  }
)

const router = useRouter()

const handleClick = () => {
  if (props.to) {
    router.push(props.to)
    return
  }
  openPopup()
}

const openPopup = () => {
  openTallyPopup(props.formId, {
    layout: 'modal', // Force layout modal pour une bonne UX
    ...props.tallyOptions,
  })
}
</script>

<style scoped></style>
