<template>
  <div class="admin-inline-controls">
    <button
      class="admin-btn fr-icon-arrow-up-line"
      :aria-label="upLabel"
      :title="upLabel"
      :disabled="upDisabled"
      @click.stop="$emit('up')"
    ></button>
    <button
      class="admin-btn fr-icon-arrow-down-line"
      :aria-label="downLabel"
      :title="downLabel"
      :disabled="downDisabled"
      @click.stop="$emit('down')"
    ></button>
    <button
      class="admin-btn fr-icon-edit-line"
      :aria-label="editLabel"
      :title="editLabel"
      @click.stop="$emit('edit')"
    ></button>
    <button
      class="admin-btn admin-btn-delete fr-icon-delete-line"
      :aria-label="deleteLabel"
      :title="deleteLabel"
      @click.stop="$emit('delete')"
    ></button>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    upDisabled?: boolean
    downDisabled?: boolean
    upLabel?: string
    downLabel?: string
    editLabel?: string
    deleteLabel?: string
  }>(),
  {
    upDisabled: false,
    downDisabled: false,
    upLabel: 'Monter',
    downLabel: 'Descendre',
    editLabel: 'Modifier',
    deleteLabel: 'Supprimer',
  }
)

defineEmits<{
  (e: 'up'): void
  (e: 'down'): void
  (e: 'edit'): void
  (e: 'delete'): void
}>()
</script>

<style scoped>
.admin-inline-controls {
  z-index: 10;
  display: flex;
  gap: 0.35rem;
  align-items: center;
}
.admin-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-default-grey) !important;
  color: var(--text-action-high-blue-france) !important;
  padding: 0 !important;
  min-height: auto !important;
  transition: all 0.15s ease-in-out;
  cursor: pointer;
}
.admin-btn::before {
  margin: 0 !important;
}
.admin-btn:hover:not(:disabled) {
  background-color: var(--background-alt-blue-france) !important;
  border-color: var(--border-default-blue-france) !important;
  color: var(--text-active-blue-france) !important;
}
.admin-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  background-color: var(--background-alt-grey) !important;
  border-color: var(--border-default-grey) !important;
  color: var(--text-disabled-grey) !important;
}
.admin-btn-delete {
  color: var(--text-default-error) !important;
}
.admin-btn-delete:hover:not(:disabled) {
  background-color: #fee9e9 !important;
  border-color: var(--border-plain-error) !important;
  color: var(--text-default-error) !important;
}
</style>
