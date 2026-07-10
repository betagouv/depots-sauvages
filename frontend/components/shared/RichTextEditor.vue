<template>
  <EditorContent v-if="editor" :editor="editor">
    <template #toolbar>
      <Toolbar>
        <SimpleToolbarButtons :editor="editor" v-model="showLinkInput" />
      </Toolbar>
      <LinkInput v-if="showLinkInput" :editor="editor" @close="showLinkInput = false" />
    </template>
  </EditorContent>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  EditorContent,
  LinkInput,
  SimpleToolbarButtons,
  Toolbar,
  useEditor,
} from '../../vue-guillotine'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const editor = useEditor(props, emit)
const showLinkInput = ref(false)
</script>
