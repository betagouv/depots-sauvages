<template>
  <div class="tiptap-editor-container">
    <slot name="toolbar"></slot>
    <div class="tiptap-content-wrapper">
      <TiptapEditorContent :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { EditorContent as TiptapEditorContent } from '@tiptap/vue-3'

defineProps<{
  editor: any
}>()
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

.tiptap-content-wrapper {
  height: 200px;
  overflow-y: auto;
  padding: 0.75rem;
}

:deep(.tiptap) {
  min-height: 100%;
  outline: none;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
}

:deep(.tiptap p) {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

:deep(.tiptap p:last-child) {
  margin-bottom: 0;
}

:deep(.tiptap ul) {
  list-style-type: disc !important;
  padding-left: 1.5rem !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0.5rem !important;
}

:deep(.tiptap ol) {
  list-style-type: decimal !important;
  padding-left: 1.5rem !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0.5rem !important;
}

:deep(.tiptap li) {
  display: list-item !important;
  list-style: inherit !important;
  padding-left: 0 !important;
  margin-bottom: 0.5rem !important;
  line-height: 1.6 !important;
}

:deep(.tiptap li::before) {
  content: none !important;
  display: none !important;
}
</style>
