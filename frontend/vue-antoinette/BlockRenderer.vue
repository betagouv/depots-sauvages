<template>
  <div class="vue-antoinette-renderer">
    <template v-for="(block, index) in blocks" :key="index">
      <div v-if="block.type === 'rich_text'" class="content-styled" v-html="block.value"></div>
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
interface Block {
  type: string
  value: any
  [key: string]: any
}

defineProps<{
  blocks: Block[]
}>()
</script>
