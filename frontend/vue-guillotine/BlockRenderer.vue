<template>
  <div class="vue-guillotine-renderer" @click="onLinkClick">
    <template v-for="(block, index) in blocks" :key="index">
      <div
        v-if="block.type === 'rich_text'"
        class="content-styled"
        v-html="processLinks(block.value)"
      ></div>
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
import { useRouter } from 'vue-router'
import { classifyLink, processLinks } from './utils/links.js'

interface Block {
  type: string
  value: any
  [key: string]: any
}

defineProps<{
  blocks: Block[]
}>()

const router = useRouter()

// Liens vers une page du site : navigation interne, sans recharger la page.
// Ctrl/Cmd/Maj + clic et clic molette gardent le comportement du navigateur.
const onLinkClick = (event: MouseEvent) => {
  if (!router || event.defaultPrevented || event.button !== 0) return
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return

  const link = (event.target as HTMLElement | null)?.closest('a')
  const href = link?.getAttribute('href')
  if (!href || link?.getAttribute('target') === '_blank') return
  if (classifyLink(href) !== 'internal') return

  event.preventDefault()
  router.push(href)
}
</script>
