<template>
  <div class="vue-guillotine-renderer" @click="handleClick">
    <template v-for="(block, index) in renderedBlocks" :key="index">
      <div v-if="block.type === 'rich_text'" class="content-styled" v-html="block.html"></div>
      <h2 v-else-if="block.type === 'heading'" class="fr-h4">
        {{ block.value }}
      </h2>
      <div v-else class="unhandled-block">
        <slot :name="block.type" :block="block">
          {{ block.value }}
        </slot>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { INTERNAL_LINK_ATTRIBUTE, normalizeRichTextLinks } from './utils/links'

interface Block {
  type: string
  value: any
  [key: string]: any
}

const props = defineProps<{
  blocks: Block[]
}>()

const router = useRouter()

const renderedBlocks = computed(() =>
  (props.blocks || []).map((block) =>
    block.type === 'rich_text'
      ? { ...block, html: normalizeRichTextLinks(block.value) }
      : { ...block, html: block.value }
  )
)

/**
 * Les liens vers le site restent dans l'application : le lecteur garde sa page
 * et son bouton « retour », et la visite n'est pas découpée en deux.
 * Les raccourcis habituels (Ctrl, Cmd, clic du milieu) continuent d'ouvrir un
 * nouvel onglet, comme sur n'importe quel lien.
 */
const handleClick = (event: MouseEvent) => {
  if (event.defaultPrevented || event.button !== 0) {
    return
  }
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
    return
  }
  const link = (event.target as HTMLElement)?.closest?.(`a[${INTERNAL_LINK_ATTRIBUTE}]`)
  if (!link) {
    return
  }
  const href = link.getAttribute('href')
  if (!href || !router) {
    return
  }
  event.preventDefault()
  router.push(href)
}
</script>
