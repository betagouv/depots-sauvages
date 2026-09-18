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
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'fr-link',
          // L'extension pose sinon target="_blank" et rel="nofollow" sur TOUS
          // les liens, y compris internes : le lecteur perd son onglet et les
          // moteurs cessent de suivre notre propre maillage. Le comportement
          // est décidé à l'affichage, selon la destination du lien
          // (voir vue-guillotine/utils/links.ts).
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
