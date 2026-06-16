<template>
  <button
    type="button"
    class="toolbar-btn"
    :class="{ 'is-active': active }"
    :title="title"
    :aria-label="ariaLabel || title"
  >
    <span :class="icon" aria-hidden="true"></span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  ariaLabel?: string
  active?: boolean
}>()
</script>

<style scoped>
.toolbar-btn {
  width: 2rem;
  height: 2rem;
  padding: 0 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none !important;
  border-radius: 4px;
  background-color: transparent !important;
  color: var(--text-action-high-blue-france) !important;
  min-height: auto !important;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.toolbar-btn:hover {
  background-color: rgba(0, 0, 145, 0.05) !important;
}

.toolbar-btn.is-active {
  background-color: var(--background-active-blue-france) !important;
  color: white !important;
}
</style>
