import Link from '@tiptap/extension-link'
import StarterKit from '@tiptap/starter-kit'
import { useEditor as useTiptapEditor } from '@tiptap/vue-3'
import { watch } from 'vue'

export function useEditor(props, emit) {
  const editor = useTiptapEditor({
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

  return editor
}
