<template>
  <div class="hero-section fr-mb-4w fr-py-4w">
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
            <h1 class="fr-hero__title fr-text--center">
              {{
                auteurIdentifie
                  ? 'Télécharger les pièces de procédure pré-remplies'
                  : 'Vous pouvez les télécharger et les compléter avec les éléments manquants'
              }}
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              <template v-if="auteurIdentifie">
                Vous trouverez ci-dessous vos pièces de procédure <strong>pré-remplies</strong>, à
                compléter avec les éléments manquants, par exemple la charte graphique de la mairie,
                la date et la signature de l'autorité compétente (maire ou personne habilitée à
                réaliser des constatations).
              </template>
              <template v-else>
                Vous trouverez ci-dessous votre rapport de constatation
                <strong>pré-rempli</strong>, à compléter avec les éléments manquants, par exemple la
                charte graphique de la mairie, la date et la signature de la personne habilitée à
                réaliser des constatations.
              </template>
            </p>
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
