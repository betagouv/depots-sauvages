<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Gestion des cookies</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Politique relative aux traceurs et cookies utilisés sur Protect’Envi.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <p>
            Un cookie ou traceur est un petit fichier texte déposé sur votre terminal (ordinateur, tablette, smartphone) lors de la visite d'un site internet.
          </p>

          <h2>Cookies de mesure d'audience (Matomo)</h2>
          <p>
            Protect’Envi utilise l'outil de mesure d'audience anonyme <strong>Matomo</strong> (recommandé par la CNIL et hébergé en France) afin d'analyser l'utilisation du site, d'évaluer les performances et d'améliorer continuellement l'ergonomie générale du service.
          </p>

          <DsfrHighlight class="fr-ml-0 fr-mb-4w">
            Les données générées sont strictement anonymisées (les adresses IP sont tronquées avant enregistrement) et ne sont pas croisées avec d'autres traitements ni transmises à des tiers. Par conséquent, l'utilisation de ce traceur est exemptée de consentement préalable selon les recommandations de la CNIL.
          </DsfrHighlight>

          <h2>Cookies strictement nécessaires au fonctionnement</h2>
          <p>
            Ces cookies sont requis pour assurer la sécurité et le bon fonctionnement technique de l'application (comme le maintien de votre session de connexion ou la mémorisation de l'état d'avancement d'une procédure en cours d'édition). Ils ne requièrent pas de consentement préalable de votre part selon les directives de la CNIL car ils sont indispensables à la fourniture du service demandé.
          </p>

          <hr class="fr-my-4w" />

          <h2>Comment désactiver les traceurs ?</h2>
          <p>
            Vous pouvez configurer votre navigateur internet pour rejeter systématiquement tous les cookies ou pour vous alerter lorsqu'un cookie est enregistré.
          </p>
          
          <DsfrCallout title="Paramétrage du navigateur" class="fr-mb-4w">
            <ul class="fr-pl-2w fr-mb-0">
              <li class="fr-mb-1w">
                <a
                  class="fr-link fr-icon-external-link-line fr-link--icon-right"
                  href="https://support.google.com/chrome/answer/95647?hl=fr"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Paramétrer les cookies sur Google Chrome
                </a>
              </li>
              <li class="fr-mb-1w">
                <a
                  class="fr-link fr-icon-external-link-line fr-link--icon-right"
                  href="https://www.firefox.com/fr/features/total-cookie-protection/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Paramétrer les cookies sur Mozilla Firefox
                </a>
              </li>
              <li class="fr-mb-1w">
                <a
                  class="fr-link fr-icon-external-link-line fr-link--icon-right"
                  href="https://support.apple.com/fr-fr/guide/safari/sfri11471/mac"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Paramétrer les cookies sur Apple Safari
                </a>
              </li>
              <li class="fr-mb-1w">
                <a
                  class="fr-link fr-icon-external-link-line fr-link--icon-right"
                  href="https://support.microsoft.com/fr-fr/edge/manage-cookies-in-microsoft-edge-view-allow-block-delete-and-use"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Paramétrer les cookies sur Microsoft Edge
                </a>
              </li>
            </ul>
          </DsfrCallout>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCallout, DsfrHighlight } from '@gouvminint/vue-dsfr'
</script>
