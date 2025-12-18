<template>
  <div class="fr-container--md fr-py-6w fr-pb-8w">
    <header class="hero-section fr-mb-6w fr-p-4w">
      <h1 class="fr-h1 fr-mb-3w">Contactez-nous</h1>
      <p class="fr-text fr-text--lead">
        Contactez-nous et posez vos questions sur Protect’Envi et les procédures dépôts sauvages
      </p>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <DsfrCard
          title="Besoin d'une réponse rapide ?"
          description="Échangez avec nos équipes par chat ou envoyez-nous un e-mail pour obtenir des réponses rapides à vos questions."
          :buttons="[
            {
              label: 'Ouvrir le chat',
              icon: chatIcon,
              onClick: openCrispChat,
            },
            {
              label: 'Envoyer un e-mail',
              icon: emailIcon,
              onClick: sendEmail,
              disabled: !contactEmail,
              secondary: true,
            },
          ]"
          size="large"
          no-arrow
          title-tag="h4"
        />
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrCard
          title="Besoin d'un accompagnement spécifique ?"
          description="Participez à un webinaire ou réservez une session d'accompagnement individuelle pour votre cas concret."
          :buttons="[
            {
              label: 'Prendre rendez-vous',
              icon: externalLinkIcon,
              onClick: openRdvPage,
              secondary: true,
            },
          ]"
          size="large"
          no-arrow
          title-tag="h4"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL

const chatIcon = { name: 'ri-chat-1-line', scale: 1.5, class: 'fr-mr-1w' }
const emailIcon = { name: 'ri-mail-line', scale: 1.5, class: 'fr-mr-1w' }
const externalLinkIcon = { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' }

const sendEmail = () => {
  window.location.href = `mailto:${contactEmail}`
}

const openRdvPage = () => {
  window.open(
    'https://rdv.anct.gouv.fr/prendre_rdv?departement=&public_link_organisation_id=1769',
    '_blank',
    'noopener,noreferrer'
  )
}

const openCrispChat = () => {
  const crisp = (window as any).$crisp
  if (crisp) {
    crisp.push(['do', 'chat:open'])
  }
}
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
