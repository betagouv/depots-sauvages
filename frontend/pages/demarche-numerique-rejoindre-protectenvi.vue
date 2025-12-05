<template>
  <main>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              Rejoignez les 100 collectivités pilotes pour mieux lutter contre les dépôts sauvages.
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Vous êtes une collectivité touchée par les dépôts sauvages et vous souhaitez agir ? La
              Gendarmerie nationale peut vous aider. Pour bénéficier d'un accompagnement
              personnalisé complétez la démarche numérique en deux minutes en cliquant sur le bouton
              ci-dessous
            </p>
            <div class="fr-hero__actions fr-text--center">
              <a
                class="fr-btn fr-btn--lg"
                :href="demarcheUrl"
                target="_blank"
                rel="noreferrer noopener"
                aria-label="Je candidate pour ma collectivité (nouvel onglet)"
              >
                Je candidate pour ma collectivité</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { DN_BASE_URL } from '../services/api'

const demarcheUrl = `${DN_BASE_URL}/commencer/rejoindre-protect-envi-pour-mieux-lutter-contre-les-depots-sauvages`
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
