<template>
  <div class="fr-container--sm fr-py-5w">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12">
        <h1 class="fr-h1 fr-mb-3w">Contactez-nous</h1>
      </div>

      <div class="fr-container">
        <p class="fr-mb-4w">
          Choisissez votre mode de contact préféré pour démarrer votre démarche :
        </p>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <a
              :href="`mailto:${contactEmail}`"
              class="fr-btn fr-mb-2w"
              aria-label="Envoyer un e-mail"
            >
              Envoyer un e-mail
            </a>
            <p class="fr-text--bold">Besoin d'aide ou d'informations détaillées ?</p>
            <p>
              Envoyez-nous un e-mail en cliquant sur le bouton ci-dessus. Vous pouvez poser vos
              questions, joindre des documents et expliquer votre situation en détail. Notre équipe
              vous répondra dans les meilleurs délais.
            </p>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <a
              href="https://rdv.anct.gouv.fr/org/1769/protect-envi"
              target="_blank"
              rel="noopener noreferrer"
              class="fr-btn fr-btn--secondary fr-mb-2w"
            >
              Prendre rendez-vous
            </a>
            <p class="fr-text--bold">Pour un accompagnement personnalisé</p>
            <p>
              Réservez un créneau pour une session d'accompagnement ou un webinaire avec notre
              équipe. Vous pourrez poser vos questions et obtenir des conseils adaptés à votre
              situation.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const contactEmail = import.meta.env.VITE_CONTACT_EMAIL
</script>
