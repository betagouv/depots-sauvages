<template>
  <div class="link-bar">
    <input
      ref="inputRef"
      v-model="linkUrl"
      type="url"
      class="fr-input fr-input--sm link-input"
      placeholder="URL du lien (ex: https://...)"
      @keydown.enter.prevent="applyLink"
      @keydown.esc.prevent="$emit('close')"
    />
    <button type="button" class="fr-btn fr-btn--sm" @click="applyLink">Valider</button>
    <button
      v-if="showRemove"
      type="button"
      class="fr-btn fr-btn--sm fr-btn--secondary btn-remove-link"
      @click="removeLink"
    >
      Supprimer
    </button>
    <button
      type="button"
      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline"
      @click="$emit('close')"
    >
      Annuler
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

const props = defineProps<{
  editor: any
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const linkUrl = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

const showRemove = computed(() => props.editor?.isActive('link'))

onMounted(() => {
  if (props.editor) {
    linkUrl.value = props.editor.getAttributes('link').href || 'https://'
  }
  if (inputRef.value) {
    inputRef.value.focus()
    inputRef.value.select()
  }
})

const applyLink = () => {
  if (!props.editor) return
  const url = linkUrl.value.trim()
  if (url === '' || url === 'https://') {
    props.editor.chain().focus().extendMarkRange('link').unsetLink().run()
  } else {
    props.editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
  }
  emit('close')
}

const removeLink = () => {
  if (!props.editor) return
  props.editor.chain().focus().extendMarkRange('link').unsetLink().run()
  emit('close')
}
</script>

<style scoped>
.link-bar {
  position: absolute;
  top: 3rem;
  left: 0.5rem;
  right: 0.5rem;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-active-blue-france);
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 145, 0.15);
  animation: slide-down 0.15s ease-out;
}

@keyframes slide-down {
  from {
    transform: translateY(-5px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.link-input {
  flex: 1;
  min-width: 150px;
  background-color: white !important;
}

.btn-remove-link {
  color: var(--text-default-error) !important;
  background-color: transparent !important;
  box-shadow: inset 0 0 0 1px var(--border-plain-error) !important;
}

.btn-remove-link:hover {
  background-color: #fee9e9 !important;
}
</style>
