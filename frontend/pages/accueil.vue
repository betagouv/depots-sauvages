<template>
  <div>
    <div class="fr-container fr-py-5w">
      <div class="fr-grid-row">
        <div class="fr-col-12">
          <h1 class="fr-h1 fr-mt-0 fr-mb-2w">
            Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.
          </h1>
        </div>
      </div>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6 premium-hero-text">
          <p class="fr-text fr-mb-1w fr-text--bold">
            Protect'Envi accompagne les collectivités à la mise en œuvre de la procédure
            administrative qui permet de sanctionner efficacement l'auteur d'un dépôt sauvage.
          </p>
          <ul class="fr-p-0 fr-mt-2w fr-mb-3w" style="list-style: none">
            <li class="fr-mb-1w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span>Formulaire de procédure <strong>prêt à l'emploi</strong></span>
            </li>
            <li class="fr-mb-1w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span>Amende jusqu'à <strong>15 000 €</strong> recouvrée au profit de la collectivité</span>
            </li>
            <li class="fr-mb-1w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span>Service numérique <strong>gratuit</strong></span>
            </li>
          </ul>
          <div>
            <router-link
              to="/demarrer-constatation"
              class="fr-btn fr-btn--lg"
              title="Lancer une procédure"
            >
              Lancer une procédure
            </router-link>
            <p class="fr-text--sm fr-mt-2w fr-mb-0 fr-hint-text">
              Connexion ProConnect requise.
              <a
                href="https://proconnect.crisp.help/fr/article/utiliser-proconnect-au-sein-dune-collectivite-ou-dune-mairie-1mobnb6"
                target="_blank"
                rel="noopener noreferrer"
                title="En savoir plus sur ProConnect - nouvelle fenêtre"
                >En savoir plus</a
              >
            </p>
          </div>
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrPicture
            class="premium-rounded-image"
            legend="Dépôt sauvage"
            ratio="16x9"
            size="medium"
            src="/static/depot-de-dechet-sauvage-image-accueil.webp"
            title="Dépôt sauvage"
          />
        </div>
      </div>
    </div>

    <div class="fr-background-alt--blue-france fr-pb-8w fr-pt-4w">
      <div class="fr-container">
        <h2 class="fr-h2 fr-mb-6w premium-text-center">Vous êtes témoin d'un dépôt sauvage ?</h2>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <img
                src="/static/artwork/pictograms/document-search.svg"
                alt=""
                class="fr-artwork"
                aria-hidden="true"
              />
              <h3 class="fr-h4">Simulateur d'éligibilité</h3>
              <p class="fr-text--sm fr-mb-3w">
                Découvrez en 2 minutes si le dépôt est éligible à la procédure administrative
              </p>
              <TallyPopupButton
                form-id="A7xA8z"
                label="Lancer le simulateur"
                variant="secondary"
                class="fr-mt-auto"
                to="/simulateur"
              />
            </div>
          </div>
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <img
                src="/static/artwork/pictograms/money.svg"
                alt=""
                class="fr-artwork"
                aria-hidden="true"
              />
              <h3 class="fr-h4">Calculateur d'amende</h3>
              <p class="fr-text--sm fr-mb-3w">
                Evaluez le montant de l'amende qui peut être prononcée pour ce dépôt
              </p>
              <TallyPopupButton
                form-id="9qElYG"
                label="Lancer le calculateur"
                variant="secondary"
                class="fr-mt-auto"
                to="/calculateur"
              />
            </div>
          </div>
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <img
                src="/static/artwork/pictograms/human-cooperation.svg"
                alt=""
                class="fr-artwork"
                aria-hidden="true"
              />
              <h3 class="fr-h4">Besoin d'aide ?</h3>
              <p class="fr-text--sm fr-mb-3w">
                Nos experts vous accompagnent pas à pas dans vos démarches administratives.
              </p>
              <router-link to="/contact" class="fr-btn fr-btn--secondary fr-mt-auto">
                Demander une démo
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fr-container fr-py-8w">
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-12 fr-col-md-5">
          <h2 class="fr-h2 fr-mb-3w">Vos leviers d'action</h2>

          <p class="fr-text fr-my-4w">
            Lorsqu'une commune constate un dépôt sauvage, elle dispose de deux leviers d'action.
            <br />Protect’Envi vous accompagne dans ces procédures en vous guidant pas à pas
          </p>
        </div>
        <div class="fr-col-12 fr-col-md-7">
          <div class="fr-grid-row fr-grid-row--gutters">
            <div class="fr-col-12 fr-col-sm-6">
              <div class="premium-card premium-card--small premium-card--static">
                <img
                  src="/static/artwork/pictograms/contract.svg"
                  alt=""
                  class="fr-artwork"
                  aria-hidden="true"
                />
                <h3 class="fr-h5">Procédure administrative</h3>
                <p class="fr-text--sm fr-mb-0">
                  Efficace et rapide, quand l'auteur est identifié. Elle permet d'émettre une amende
                  pouvant aller jusqu'à 15 000 €, recouvrée au profit de la mairie.
                </p>
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6">
              <div class="premium-card premium-card--small premium-card--static">
                <img
                  src="/static/artwork/pictograms/justice.svg"
                  alt=""
                  class="fr-artwork"
                  aria-hidden="true"
                />
                <h3 class="fr-h5">Procédure judiciaire</h3>
                <p class="fr-text--sm fr-mb-0">
                  Déposer plainte auprès de la police ou de la gendarmerie.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import TallyPopupButton from '@/components/shared/TallyPopupButton.vue'
import { useTallyRoutes } from '@/composables/useTally'
import { DsfrPicture } from '@gouvminint/vue-dsfr'

useTallyRoutes({
  '/simulateur': { formId: 'A7xA8z', options: { layout: 'modal', width: 900 } },
  '/calculateur': { formId: '9qElYG', options: { layout: 'modal', width: 900 } },
})
</script>
