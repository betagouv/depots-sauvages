<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Participez à notre prochain webinaire</h1>
        <p class="fr-text fr-text--lead fr-mb-3w">
          En moins de 60 minutes, découvrez comment les collectivités peuvent agir concrètement
          contre les dépôts sauvages grâce à la procédure administrative.
        </p>
        <a
          :href="anctLink"
          target="_blank"
          rel="noopener noreferrer"
          class="fr-btn fr-btn--lg fr-icon-video-chat-line fr-btn--icon-left"
        >
          Je m'inscris au webinaire via RDV service public
        </a>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <section class="fr-mb-4w">
        <h2 class="fr-h4 fr-mb-3w">Pendant ce webinaire, vous découvrirez :</h2>
        <ul class="fr-raw-list fr-mb-0">
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>quand utiliser la procédure administrative</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>comment traiter votre premier dépôt sauvage</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>les bonnes pratiques à appliquer et les erreurs à éviter</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>comment répondre aux situations les plus fréquentes</span>
          </li>
        </ul>
      </section>

      <hr class="fr-my-4w" />

      <section class="fr-mb-4w">
        <h2 class="fr-h4 fr-mb-3w">À qui s'adresse ce webinaire</h2>
        <ul class="fr-raw-list fr-mb-0">
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-user-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Maires, présidents d'intercommunalité et élus en charge du sujet</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-government-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Directions générales des services (DGS) et agents administratifs</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-shield-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Polices municipales et gardes champêtres</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-settings-5-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Services techniques et environnement</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-shield-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Gendarmes ou policiers accompagnant les collectivités</span>
          </li>
          <li class="fr-mb-0 fr-display-flex">
            <span class="fr-icon-community-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
            <span>Toute personne impliquée dans la gestion des dépôts sauvages au sein d'une collectivité</span>
          </li>
        </ul>
      </section>

      <hr class="fr-my-4w" />

      <section class="fr-mb-4w">
        <h2 class="fr-h4 fr-mb-3w">Informations pratiques</h2>
        <ul class="fr-raw-list fr-mb-0">
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-calendar-line fr-mr-1w" aria-hidden="true"></span>
            <span>Toutes les semaines</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-time-line fr-mr-1w" aria-hidden="true"></span>
            <span>Durée : 45 à 60 minutes</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-money-euro-circle-line fr-mr-1w" aria-hidden="true"></span>
            <span>Gratuit</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span class="fr-icon-computer-line fr-mr-1w" aria-hidden="true"></span>
            <span>En visioconférence</span>
          </li>
        </ul>
      </section>

      <div class="fr-mb-4w">
        <a
          :href="anctLink"
          target="_blank"
          rel="noopener noreferrer"
          class="fr-btn fr-btn--lg fr-icon-video-chat-line fr-btn--icon-left"
        >
          Je m'inscris au webinaire via RDV service public
        </a>
      </div>

      <hr class="fr-my-4w" />

      <section>
        <h2 class="fr-h4 fr-mb-2w">Et si vous n'êtes pas disponible ?</h2>
        <p class="fr-text fr-mb-1w">Laissez-nous votre adresse e-mail.</p>
        <p class="fr-text fr-mb-1w">Nous vous informerons :</p>
        <ul class="fr-pl-3w fr-mb-3w">
          <li class="fr-mb-1w">des prochaines dates des webinaires ;</li>
          <li class="fr-mb-0">des nouveautés de Protect'Envi.</li>
        </ul>
        <TallyPopupButton
          form-id="Pdyay0"
          label="Je souhaite être informé"
          variant="primary"
          to="/rdv/etre-informe"
          icon="fr-icon-mail-line"
        />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import TallyPopupButton from '@/components/shared/TallyPopupButton.vue'
import { useTallyRoutes } from '@/composables/useTally'

const anctLink = import.meta.env.VITE_RDV_PAGE_URL || ''

useTallyRoutes({
  '/rdv/etre-informe': {
    formId: 'Pdyay0',
    options: { layout: 'modal', width: 900 },
    returnPath: '/rdv',
  },
})
</script>
