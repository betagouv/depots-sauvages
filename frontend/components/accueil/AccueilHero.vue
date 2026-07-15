<template>
  <div class="fr-container fr-py-6w">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-6 premium-hero-text">
        <h1 class="fr-h1 fr-mt-0 fr-mb-2w text-balance">
          Agir contre les dépôts sauvages dans votre collectivité
        </h1>
        <p class="fr-text fr-text--lead fr-mb-3w">
          Comprendre comment agir, sécuriser vos procédures et sanctionner les auteurs de dépôts
          sauvages.
        </p>
        <ul class="fr-p-0 fr-mt-2w fr-mb-0 unstyled-list">
          <li class="fr-mb-2v fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span
              ><strong>Accompagnement pas à pas</strong>, accessible sans expertise
              juridique</span
            >
          </li>
          <li class="fr-mb-2v fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span
              ><strong>Procédure juridiquement sécurisée</strong>, conforme au Code de
              l'environnement</span
            >
          </li>
          <li class="fr-mb-2v fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span><strong>Dispositif gratuit</strong> proposé par la Gendarmerie nationale</span>
          </li>
        </ul>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrPicture
          class="premium-rounded-image"
          legend="Constatation d'un dépôt sauvage par la police municipale"
          ratio="16x9"
          size="medium"
          src="/static/depot-de-dechet-sauvage-image-accueil.webp"
          title="Constatation d'un dépôt sauvage par la police municipale"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrPicture } from '@gouvminint/vue-dsfr'
</script>

<style scoped>
.text-balance {
  text-wrap: balance;
}

.unstyled-list {
  list-style: none;
}
</style>
