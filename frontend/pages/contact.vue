<template>
  <div class="fr-container--md fr-py-6w fr-pb-8w">
    <header class="hero-section fr-mb-6w fr-p-4w">
      <h1 class="fr-h1 fr-mb-3w">Contactez-nous</h1>
      <p class="fr-text fr-text--lead">
        Choisissez votre mode de contact préféré pour démarrer votre démarche.
      </p>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <DsfrCard
          title="Envoyer un e-mail"
          description="Envoyez-nous un e-mail pour poser vos questions, joindre des documents et expliquer votre situation en détail. Notre équipe vous répondra dans les meilleurs délais."
          :buttons="[
            {
              label: 'Envoyer un e-mail',
              icon: { name: 'ri-mail-line', scale: 1.5, class: 'fr-mr-1w' },
              onClick: sendEmail,
              disabled: !contactEmail,
            },
          ]"
          size="large"
          no-arrow
          title-tag="h2"
          detail="Besoin d'aide ou d'informations détaillées ?"
          detail-icon="ri-question-line"
        />
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrCard
          title="Prendre rendez-vous"
          description="Réservez un créneau via RDV Service Public, pour une session d'accompagnement ou un webinaire avec notre équipe. Vous pourrez poser vos questions et obtenir des conseils adaptés à votre situation."
          :buttons="[
            {
              label: 'Prendre rendez-vous',
              icon: { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' },
              secondary: true,
              onClick: openRdvPage,
            },
          ]"
          size="large"
          no-arrow
          title-tag="h2"
          detail="Besoin d'un accompagnement personnalisé ?"
          detail-icon="ri-user-line"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL

const sendEmail = () => {
  window.location.href = `mailto:${contactEmail}`
}

const openRdvPage = () => {
  window.open('https://rdv.anct.gouv.fr/org/1769/protect-envi', '_blank', 'noopener,noreferrer')
}
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
