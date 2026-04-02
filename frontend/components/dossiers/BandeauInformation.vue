<template>
  <div class="hero-section fr-mb-2w fr-pt-2w">
    <div class="fr-grid-row">
      <div class="fr-col-12">
        <template v-if="!hasProcedure">
          <p class="fr-text--lg">Le dossier n'est pas associé à une procédure de dépôt sauvage.</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hasProcedure: boolean
  auteurIdentifie: boolean
}>()
</script>
