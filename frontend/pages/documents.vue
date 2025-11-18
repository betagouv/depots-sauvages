<template>
  <div>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">Télécharger vos documents</h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Téléchargez en un clic votre rapport de constatation et la lettre d'information
              associée à votre dossier.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="fr-container fr-pb-4w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Lettre d'information"
            description="Courrier type rappelant les faits constatés, les obligations du détenteur des déchets et le délai de réponse prévu par la procédure."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => {},
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Rapport de constatation"
            description="Pièce officielle résumant les observations de terrain et les préjudices causés par le dépôt sauvage."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => {},
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
