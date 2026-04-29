<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div
        class="fr-col-12 fr-col-md-6"
        style="display: flex; flex-direction: column; justify-content: center"
      >
        <h1 class="fr-h1 fr-mt-0 fr-mb-3w">
          Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.
        </h1>
        <p class="fr-text fr-mb-4w">
          La procédure administrative permet aux collectivités locales de sanctionner rapidement
          l’auteur d’un dépôt sauvage par une amende pouvant aller jusqu’à 15 000 €, recouvrée au
          profit de la collectivité.
        </p>
        <div>
          <a
            :href="demarcheNumeriqueUrl"
            class="fr-btn fr-btn--lg"
            target="_blank"
            rel="noopener noreferrer"
          >
            Débuter une procédure administrative
          </a>
          <p class="fr-text--sm fr-mt-2w fr-mb-0" style="color: var(--text-mention-grey)">
            Connexion ProConnect requise.
            <a
              href="https://proconnect.crisp.help/fr/article/utiliser-proconnect-au-sein-dune-collectivite-ou-dune-mairie-1mobnb6"
              target="_blank"
              rel="noopener noreferrer"
              >En savoir plus</a
            >
          </p>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrPicture
          legend="Dépôt sauvage"
          ratio="16x9"
          size="medium"
          src="/static/depot-de-dechet-sauvage-image-accueil.webp"
          title="Dépôt sauvage"
        />
      </div>

      <div class="fr-col-12 fr-mt-4w fr-mb-4w">
        <h2 class="fr-h2 fr-mb-4w" style="text-align: center">Vous avez un dépôt sauvage ?</h2>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <span class="fr-icon-search-line fr-icon--lg" aria-hidden="true"></span>
              <h3 class="fr-h4">Simulateur d'éligibilité</h3>
              <p class="fr-text--sm fr-mb-3w">
                Vérifier si la procédure administrative est adaptée
              </p>
              <TallyPopupButton
                form-id="A7xA8z"
                label="Lancer le simulateur"
                variant="secondary"
                style="margin-top: auto"
              />
            </div>
          </div>
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <span class="fr-icon-calculator-line fr-icon--lg" aria-hidden="true"></span>
              <h3 class="fr-h4">Calculateur d'amende</h3>
              <p class="fr-text--sm fr-mb-3w">Calculer le montant de l’amende pour ce dépôt</p>
              <TallyPopupButton
                form-id="9qElYG"
                label="Lancer le calculateur"
                variant="secondary"
                style="margin-top: auto"
              />
            </div>
          </div>
          <div class="fr-col-12 fr-col-md-4">
            <div class="premium-card">
              <span class="fr-icon-discuss-line fr-icon--lg" aria-hidden="true"></span>
              <h3 class="fr-h4">Besoin d'aide ?</h3>
              <p class="fr-text--sm fr-mb-3w">
                Nos experts vous accompagnent pas à pas dans vos démarches administratives.
              </p>
              <router-link to="/contact" class="fr-btn fr-btn--secondary" style="margin-top: auto">
                Se faire accompagner
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <DsfrCallout
        title="Vos deux leviers d'action"
        content=""
        class="fr-callout--blue-ecume fr-mt-2w"
      >
        <p class="fr-text">Lorsqu'une commune constate un dépôt sauvage, elle peut :</p>
        <ul class="fr-text fr-mb-0">
          <li>
            Mettre en œuvre une <strong>procédure administrative</strong>, plus efficace et plus
            rapide, quand l'auteur est identifié. Cette procédure permet d'émettre une amende
            pouvant aller jusqu'à 15 000 €, recouvrée au profit de la mairie.
          </li>
          <li class="fr-mt-1w">
            Déposer plainte <strong>pour initier une procédure judiciaire ;</strong>
          </li>
        </ul>
        <p class="fr-text fr-mt-2w">
          Protect’Envi vous accompagne dans ces procédures en vous guidant pas à pas et en vous
          fournissant des documents conformes pré-remplis.
        </p>
      </DsfrCallout>
    </div>
  </div>
</template>

<script setup lang="ts">
import TallyPopupButton from '@/components/shared/TallyPopupButton.vue'
import { DsfrCallout, DsfrPicture } from '@gouvminint/vue-dsfr'

const demarcheNumeriqueUrl = import.meta.env.VITE_DN_URL
</script>
