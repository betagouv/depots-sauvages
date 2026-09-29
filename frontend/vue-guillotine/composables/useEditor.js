import Link from '@tiptap/extension-link'
import StarterKit from '@tiptap/starter-kit'
import { useEditor as useTiptapEditor } from '@tiptap/vue-3'
import { watch } from 'vue'

export function useEditor(props, emit) {
  const editor = useTiptapEditor({
    content: props.modelValue,
    extensions: [
      StarterKit.configure({
        link: false,
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
      // Pas de target/rel enregistrés : c'est BlockRenderer qui décide à l'affichage
      // (même onglet pour les pages du site, nouvel onglet pour les autres sites).
      Link.extend({
        addAttributes() {
          return {
            ...this.parent?.(),
            target: { default: null, parseHTML: () => null },
            rel: { default: null, parseHTML: () => null },
          }
        },
      }).configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'fr-link',
          target: null,
          rel: null,
        },
      }),
    ],
    editorProps: {
      attributes: {
        class: 'tiptap',
      },
    },
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
