<template>
  <div class="step-locked-notice fr-p-2w fr-mb-3w" role="note" aria-live="polite">
    <div class="fr-grid-row fr-grid-row--middle fr-no-wrap">
      <div class="fr-col-auto fr-mr-2w">
        <div class="locked-icon-badge">
          <span class="fr-icon-lock-line fr-icon--sm" aria-hidden="true"></span>
        </div>
      </div>
      <div class="fr-col">
        <p class="fr-text--sm fr-text--bold fr-mb-0 locked-title">
          Étape en consultation
        </p>
        <p class="fr-text--xs fr-mb-0 locked-description">
          {{ message }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    message?: string
  }>(),
  {
    message:
      'Les actions seront modifiables dès validation des étapes précédentes.',
  }
)
</script>

<style scoped>
.step-locked-notice {
  background: linear-gradient(135deg, rgba(246, 246, 246, 0.95) 0%, rgba(238, 240, 248, 0.7) 100%);
  border: 1px solid var(--border-default-grey);
  border-left: 3px solid var(--border-action-high-blue-france);
  border-radius: 8px;
  backdrop-filter: blur(4px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.locked-icon-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: var(--background-action-low-blue-france);
  color: var(--text-action-high-blue-france);
}

.locked-title {
  color: var(--text-title-grey);
  line-height: 1.25rem;
}

.locked-description {
  color: var(--text-mention-grey);
}
</style>
