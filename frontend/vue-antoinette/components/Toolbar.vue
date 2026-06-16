<template>
  <div class="toolbar">
    <slot></slot>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  background-color: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
  flex-wrap: wrap;
}
</style>
