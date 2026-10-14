<template>
  <div class="vue-guillotine-renderer" @click="handleClick">
    <template v-for="(block, index) in blocks" :key="index">
      <div
        v-if="block.type === 'rich_text'"
        class="content-styled"
        v-html="cleanHtmlLinks(block.value)"
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
import { cleanHtmlLinks, isInternalUrl, normalizeLinkHref } from './utils/linkUtils.js'

interface Block {
  type: string
  value: any
  [key: string]: any
}

defineProps<{
  blocks: Block[]
}>()

const router = useRouter()

// Intercepte les clics sur les liens internes pour naviguer via le routeur SPA sans rechargement.
const handleClick = (event: MouseEvent) => {
  if (event.defaultPrevented || event.button !== 0) {
    return
  }
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
    return
  }
  const link = (event.target as HTMLElement)?.closest?.('a[href]')
  if (!link) {
    return
  }
  const href = link.getAttribute('href')
  if (!href || !router) {
    return
  }

  if (
    isInternalUrl(href) &&
    !href.startsWith('#') &&
    !href.startsWith('mailto:') &&
    !href.startsWith('tel:')
  ) {
    event.preventDefault()
    router.push(normalizeLinkHref(href))
  }
}
</script>
