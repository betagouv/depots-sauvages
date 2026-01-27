<template>
  <div class="hero-section fr-mb-2w fr-pt-2w">
    <div class="fr-container">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
          <template v-if="!hasProcedure">
            <h1 class="fr-hero__title fr-text--center">Dossier sans procédure</h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Le dossier n'est pas associé à une procédure de dépôt sauvage.
            </p>
          </template>

          <template v-else>
            <h1 class="fr-h2 fr-text--center">
              {{
                auteurIdentifie
                  ? 'Télécharger les pièces de procédure pré-remplies'
                  : 'Télécharger le rapport de constatation pré-rempli'
              }}
            </h1>
          </template>
        </div>
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

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
