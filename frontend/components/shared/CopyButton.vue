<template>
  <button
    class="fr-btn fr-btn--tertiary-no-outline"
    :class="isCopied ? 'fr-icon-check-line' : 'fr-icon-link'"
    :title="isCopied ? copiedTitle : title"
    :aria-label="isCopied ? copiedTitle : title"
    @click.stop="copyText"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    text: string
    title?: string
    copiedTitle?: string
  }>(),
  {
    title: 'Copier dans le presse-papier',
    copiedTitle: 'Copié !',
  }
)

const isCopied = ref(false)

const copyText = () => {
  const performCopy = () => {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(props.text)
    } else {
      const textArea = document.createElement('textarea')
      textArea.value = props.text
      textArea.style.position = 'absolute'
      textArea.style.opacity = '0'
      document.body.appendChild(textArea)
      textArea.select()
      return new Promise<void>((resolve, reject) => {
        try {
          document.execCommand('copy') ? resolve() : reject()
        } catch (err) {
          reject(err)
        } finally {
          document.body.removeChild(textArea)
        }
      })
    }
  }

  performCopy()
    .then(() => {
      isCopied.value = true
      setTimeout(() => {
        isCopied.value = false
      }, 2000)
    })
    .catch((err) => {
      console.error('Erreur lors de la copie :', err)
    })
}
</script>
