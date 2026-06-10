<template>
  <div v-if="editor" class="tiptap-editor-container">
    <!-- Toolbar -->
    <div class="tiptap-toolbar">
      <button
        type="button"
        class="toolbar-btn fr-btn--secondary"
        :class="{ 'is-active': editor.isActive('bold') }"
        @click="editor.chain().focus().toggleBold().run()"
        title="Gras"
        aria-label="Formater en gras"
      >
        <span class="fr-icon-bold" aria-hidden="true"></span>
      </button>

      <button
        type="button"
        class="toolbar-btn fr-btn--secondary"
        :class="{ 'is-active': editor.isActive('italic') }"
        @click="editor.chain().focus().toggleItalic().run()"
        title="Italique"
        aria-label="Formater en italique"
      >
        <span class="fr-icon-italic" aria-hidden="true"></span>
      </button>

      <button
        type="button"
        class="toolbar-btn fr-btn--secondary"
        :class="{ 'is-active': editor.isActive('link') || showLinkInput }"
        @click="toggleLinkInput"
        title="Lien"
        aria-label="Ajouter un lien"
      >
        <span class="fr-icon-link" aria-hidden="true"></span>
      </button>

      <div class="toolbar-divider"></div>

      <button
        type="button"
        class="toolbar-btn fr-btn--secondary"
        :class="{ 'is-active': editor.isActive('bulletList') }"
        @click="editor.chain().focus().toggleBulletList().run()"
        title="Liste à puces"
        aria-label="Insérer une liste à puces"
      >
        <span class="fr-icon-list-unordered" aria-hidden="true"></span>
      </button>

      <button
        type="button"
        class="toolbar-btn fr-btn--secondary"
        :class="{ 'is-active': editor.isActive('orderedList') }"
        @click="editor.chain().focus().toggleOrderedList().run()"
        title="Liste ordonnée"
        aria-label="Insérer une liste numérotée"
      >
        <span class="fr-icon-list-ordered" aria-hidden="true"></span>
      </button>
    </div>

    <!-- Inline Link Bar -->
    <div v-if="showLinkInput" class="tiptap-link-bar">
      <input
        ref="linkInputRef"
        v-model="linkUrl"
        type="url"
        class="fr-input fr-input--sm link-input"
        placeholder="URL du lien (ex: https://...)"
        @keydown.enter.prevent="applyLink"
        @keydown.esc.prevent="showLinkInput = false"
      />
      <button type="button" class="fr-btn fr-btn--sm" @click="applyLink">Valider</button>
      <button
        v-if="editor.isActive('link')"
        type="button"
        class="fr-btn fr-btn--sm fr-btn--secondary btn-remove-link"
        @click="removeLink"
      >
        Supprimer
      </button>
      <button
        type="button"
        class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline"
        @click="showLinkInput = false"
      >
        Annuler
      </button>
    </div>

    <!-- Editor Text Area -->
    <div class="tiptap-content-wrapper">
      <editor-content :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Link from '@tiptap/extension-link'
import StarterKit from '@tiptap/starter-kit'
import { EditorContent, useEditor } from '@tiptap/vue-3'
import { nextTick, ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      bulletList: {
        HTMLAttributes: {
          class: 'tiptap-ul',
        },
      },
      orderedList: {
        HTMLAttributes: {
          class: 'tiptap-ol',
        },
      },
    }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: 'fr-link',
      },
    }),
  ],
  onUpdate: () => {
    emit('update:modelValue', editor.value?.getHTML() || '')
  },
})

watch(
  () => props.modelValue,
  (value) => {
    if (editor.value) {
      const isSame = editor.value.getHTML() === value
      if (!isSame) {
        editor.value.commands.setContent(value, false)
      }
    }
  }
)

const showLinkInput = ref(false)
const linkUrl = ref('')
const linkInputRef = ref<HTMLInputElement | null>(null)

const toggleLinkInput = () => {
  if (!editor.value) return

  if (showLinkInput.value) {
    showLinkInput.value = false
    return
  }

  const previousUrl = editor.value.getAttributes('link').href || ''
  linkUrl.value = previousUrl || 'https://'
  showLinkInput.value = true

  nextTick(() => {
    if (linkInputRef.value) {
      linkInputRef.value.focus()
      linkInputRef.value.select()
    }
  })
}

const applyLink = () => {
  if (!editor.value) return

  const url = linkUrl.value.trim()

  if (url === '' || url === 'https://') {
    editor.value.chain().focus().extendMarkRange('link').unsetLink().run()
  } else {
    editor.value.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
  }
  showLinkInput.value = false
}

const removeLink = () => {
  if (!editor.value) return
  editor.value.chain().focus().extendMarkRange('link').unsetLink().run()
  showLinkInput.value = false
}
</script>

<style scoped>
.tiptap-editor-container {
  position: relative;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
  border-radius: 6px;
  background-color: var(--background-default-grey);
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.tiptap-editor-container:focus-within {
  border-color: var(--border-active-blue-france);
  box-shadow: 0 0 0 1px var(--border-active-blue-france);
}

.tiptap-toolbar {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  background-color: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
  flex-wrap: wrap;
}

.tiptap-link-bar {
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

.toolbar-btn {
  width: 2rem;
  height: 2rem;
  padding: 0 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none !important;
  border-radius: 4px;
  background-color: transparent !important;
  color: var(--text-action-high-blue-france) !important;
  min-height: auto !important;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.toolbar-btn:hover {
  background-color: rgba(0, 0, 145, 0.05) !important;
}

.toolbar-btn.is-active {
  background-color: var(--background-active-blue-france) !important;
  color: white !important;
}

.toolbar-divider {
  width: 1px;
  height: 1.25rem;
  background-color: var(--border-default-grey);
  margin: 0 0.25rem;
}

.tiptap-content-wrapper {
  height: 200px;
  overflow-y: auto;
  padding: 0.75rem;
}

.tiptap-content-wrapper :deep(.tiptap) {
  min-height: 100%;
  outline: none;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
}

.tiptap-content-wrapper :deep(.tiptap p) {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.tiptap-content-wrapper :deep(.tiptap p:last-child) {
  margin-bottom: 0;
}
</style>
