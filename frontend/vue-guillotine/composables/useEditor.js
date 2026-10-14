import { mergeAttributes } from '@tiptap/core'
import Link from '@tiptap/extension-link'
import StarterKit from '@tiptap/starter-kit'
import { useEditor as useTiptapEditor } from '@tiptap/vue-3'
import { watch } from 'vue'
import { isInternalUrl, normalizeLinkHref } from '../utils/linkUtils.js'

const CustomLink = Link.extend({
  renderHTML({ HTMLAttributes }) {
    const rawHref = HTMLAttributes.href || ''
    const isInternal = isInternalUrl(rawHref)
    const normalizedHref = isInternal ? normalizeLinkHref(rawHref) : rawHref
    const attrs = mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, {
      href: normalizedHref,
    })
    if (isInternal) {
      delete attrs.target
      delete attrs.rel
    } else {
      attrs.target = '_blank'
      attrs.rel = 'noopener noreferrer'
    }
    return ['a', attrs, 0]
  },
})

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
      CustomLink.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'fr-link',
          // Prevent extension from enforcing target="_blank" and rel="nofollow" on internal links.
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
