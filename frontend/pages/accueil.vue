<template>
  <main class="fr-container--sm fr-py-5w">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <h1 class="fr-h1 fr-mb-3w">Agir ensemble contre les dépôts sauvages</h1>
        <p class="fr-text fr-mb-2w">Simplifier le signalement des dépôts sauvages</p>
        <p>Notre outil vous accompagne et vous aide à produire des rapports pour faciliter la procédure administrative et judiciaire.</p>
        <p>Notre objectif : améliorer l’efficacité des services publics, faciliter les procédures et contribuer à la réduction durable des dépôts sauvages sur le territoire.</p>
        <RouterLink to="/debuter-procedure" class="fr-btn fr-mt-3w">Débuter une procédure</RouterLink>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrPicture
          legend="Déchèterie sauvage à Carrières-sous-Poissy - Yvelines"
          ratio="16x9"
          size="medium"
          src="frontend/assets/images/image-decheterie-carrieres-sous-poissy.jpg"
          title="Déchèterie sauvage à Carrières-sous-Poissy - Yvelines"
        />
      </div>
    </div>
  </main>
</template>
<script setup lang="ts">
import { DsfrPicture } from '@gouvminint/vue-dsfr'
</script>