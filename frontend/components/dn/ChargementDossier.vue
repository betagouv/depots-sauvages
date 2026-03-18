<template>
  <div class="fr-container fr-pb-4w fr-mt-4w">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
        <div class="loading-section fr-p-4w fr-text--center" role="status" aria-live="polite">
          <VIcon
            name="ri-loader-4-line"
            :scale="3"
            animation="spin"
            class="fr-mb-2w"
            aria-hidden="true"
          />
          <p class="fr-text--lg fr-mb-0">{{ message }}</p>
          <p class="fr-text--sm fr-text-mention--grey">Veuillez patienter quelques instants.</p>
        </div>
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
    message: 'Récupération des informations du dossier...',
  }
)
</script>

<style scoped>
.loading-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
}
</style>
