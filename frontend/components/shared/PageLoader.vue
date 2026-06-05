<template>
  <div class="fr-grid-row fr-grid-row--center fr-my-8w">
    <div class="fr-col-12 fr-col-md-6 text-center">
      <span
        class="fr-icon-refresh-line fr-icon--lg"
        aria-hidden="true"
        style="animation: spin 1s linear infinite"
      ></span>
      <p class="fr-mt-2w">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    message?: string
  }>(),
  {
    message: 'Chargement de la page...',
  }
)
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.text-center {
  text-align: center;
}
</style>
