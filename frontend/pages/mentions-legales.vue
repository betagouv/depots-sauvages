<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Mentions légales</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Informations légales concernant l'éditeur et l'hébergeur du service Protect’Envi.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <h2>Éditeur du site</h2>
          <p>
            Le site Protect’Envi est édité par le <strong>Commandement pour l’environnement et la santé (CESAN)</strong> de la Gendarmerie nationale, sous l'égide du Ministère de l'Intérieur.
          </p>

          <DsfrHighlight class="fr-ml-0 fr-mb-4w">
            <strong>Adresse de l'éditeur :</strong><br />
            CESAN - Gendarmerie Nationale<br />
            6 Av. de Stalingrad<br />
            94110 Arcueil<br />
            France
            <br /><br />
            <strong>Directeur de la publication :</strong><br />
            Le Général de division, commandant le CESAN.
          </DsfrHighlight>

          <hr class="fr-my-4w" />

          <h2>Hébergement du site</h2>
          <p>
            Ce site est hébergé en France par la société <strong>Scalingo SAS</strong>, une entreprise française spécialisée dans l'hébergement cloud souverain et conforme aux standards de sécurité.
          </p>

          <DsfrHighlight class="fr-ml-0 fr-mb-4w">
            <strong>Adresse de l'hébergeur :</strong><br />
            Scalingo SAS<br />
            3 rue de la Chocolaterie<br />
            41000 Blois<br />
            France
          </DsfrHighlight>

          <hr class="fr-my-4w" />

          <h2>Accessibilité</h2>
          <p>
            La conformité aux normes d'accessibilité numérique est un droit pour tous. Protect’Envi est engagé dans une démarche d'amélioration continue pour rendre ce site accessible à chacun. Vous pouvez consulter notre <router-link to="/a11y">déclaration d'accessibilité</router-link> pour plus de détails.
          </p>

          <hr class="fr-my-4w" />

          <h2>Propriété intellectuelle</h2>
          <p>
            Sauf mention contraire, tous les contenus de ce site (textes, images, graphismes, logos, icônes) sont sous <a href="https://github.com/etalab/licence-ouverte/blob/master/LO.md" target="_blank" rel="noopener">licence etalab-2.0</a>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrHighlight } from '@gouvminint/vue-dsfr'
</script>
