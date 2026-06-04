<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Plan du site</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Arborescence complète des pages disponibles sur Protect’Envi.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <nav role="navigation" aria-label="Plan du site">
            <h2 class="fr-h4 fr-mb-2w">Pages principales</h2>
            <ul class="fr-pl-3w fr-mb-4w">
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/">Accueil</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/comprendre-la-procedure">Comprendre la procédure</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/demarche-numerique-rejoindre-protectenvi">Rejoindre le dispositif</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/mes-procedures">Mes procédures (espace connecté)</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/contact">Contactez-nous</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/rdv">Prendre rendez-vous</router-link>
              </li>
            </ul>

            <h2 class="fr-h4 fr-mb-2w">Informations réglementaires</h2>
            <ul class="fr-pl-3w">
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/a11y">Accessibilité : non conforme</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/mentions-legales">Mentions légales</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/donnees-personnelles">Données personnelles et confidentialité</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/cookies">Gestion des cookies</router-link>
              </li>
              <li class="fr-mb-1w">
                <router-link class="fr-link" to="/plan-du-site" aria-current="page">Plan du site</router-link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Sitemap page
</script>
