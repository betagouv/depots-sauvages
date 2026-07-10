<template>
  <ToolbarButton
    icon="fr-icon-bold"
    title="Gras"
    aria-label="Formater en gras"
    :active="editor.isActive('bold')"
    @click="editor.chain().focus().toggleBold().run()"
  />

  <ToolbarButton
    icon="fr-icon-italic"
    title="Italique"
    aria-label="Formater en italique"
    :active="editor.isActive('italic')"
    @click="editor.chain().focus().toggleItalic().run()"
  />

  <ToolbarButton
    icon="fr-icon-link"
    title="Lien"
    aria-label="Ajouter un lien"
    :active="editor.isActive('link') || modelValue"
    @click="$emit('update:modelValue', !modelValue)"
  />

  <div class="toolbar-divider"></div>

  <ToolbarButton
    icon="fr-icon-list-unordered"
    title="Liste à puces"
    aria-label="Insérer une liste à puces"
    :active="editor.isActive('bulletList')"
    @click="editor.chain().focus().toggleBulletList().run()"
  />

  <ToolbarButton
    icon="fr-icon-list-ordered"
    title="Liste ordonnée"
    aria-label="Insérer une liste numérotée"
    :active="editor.isActive('orderedList')"
    @click="editor.chain().focus().toggleOrderedList().run()"
  />
</template>

<script setup lang="ts">
import ToolbarButton from './ToolbarButton.vue'

defineProps<{
  editor: any
  modelValue?: boolean
}>()

defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()
</script>

<style scoped>
.toolbar-divider {
  width: 1px;
  height: 1.25rem;
  background-color: var(--border-default-grey);
  margin: 0 0.25rem;
}
</style>
