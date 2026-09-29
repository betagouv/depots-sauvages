<template>
  <div class="vue-guillotine-renderer" @click="onLinkClick">
    <template v-for="(block, index) in blocks" :key="index">
      <div
        v-if="block.type === 'rich_text'"
        class="content-styled"
        v-html="processLinks(block.value, siteHosts)"
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
import { processLinks } from './utils/links.js'

interface Block {
  type: string
  value: any
  [key: string]: any
}

withDefaults(
  defineProps<{
    blocks: Block[]
    siteHosts?: string[]
  }>(),
  { siteHosts: () => [] }
)

const router = useRouter()

const onLinkClick = (event: MouseEvent) => {
  if (!router || event.defaultPrevented || event.button !== 0) return
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
  const link = (event.target as HTMLElement | null)?.closest('a')
  const href = link?.getAttribute('href')
  if (!href?.startsWith('/') || link?.target) return
  event.preventDefault()
  router.push(href)
}
</script>
