<template>
  <div class="fr-container--md fr-py-6w fr-pb-8w">
    <header class="hero-section fr-mb-6w fr-p-4w">
      <h1 class="fr-h1 fr-mb-3w">Contactez-nous</h1>
      <p class="fr-text fr-text--lead">
        Échangez avec nos équipes pour répondre à toutes vos questions sur Protect'Envi et les
        procédures dépôts sauvages.
      </p>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-mb-4w">
          <h4 class="fr-h4 fr-mb-4w">Besoin d'une réponse rapide ?</h4>

          <div class="fr-mb-4w">
            <DsfrCard
              title="Discutez avec nos équipes en direct"
              description="Échangez en temps réel avec nos équipes pour obtenir des réponses rapides à vos questions."
              :buttons="[
                {
                  label: 'Ouvrir le chat',
                  icon: chatIcon,
                  onClick: openCrispChat,
                },
              ]"
              size="large"
              no-arrow
              title-tag="h5"
            />
          </div>

          <div>
            <DsfrCard
              title="Envoyer un mail à l'équipe"
              description="Envoyez-nous un e-mail pour poser vos questions, joindre des documents et expliquer votre situation en détail."
              :buttons="[
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
              title-tag="h5"
            />
          </div>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-mb-4w">
          <h4 class="fr-h4 fr-mb-4w">Besoin d'un accompagnement spécifique ?</h4>
          <div class="fr-mb-4w">
            <DsfrCard
              title="En savoir plus sur le dispositif Protect'Envi"
              description="Participez à notre webinaire de présentation hebdomadaire : 30 min de présentation + 15 min de questions/réponses."
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
              title-tag="h5"
            />
          </div>

          <div class="fr-mb-4w">
            <DsfrCard
              title="Vous avez un cas concret de procédure"
              description="Participez à une session d'accompagnement individuelle de 15min pour en discuter en détail."
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
              title-tag="h5"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL

const chatIcon = { name: 'ri-message-3-line', scale: 1.5, class: 'fr-mr-1w' }
const emailIcon = { name: 'ri-mail-line', scale: 1.5, class: 'fr-mr-1w' }
const externalLinkIcon = { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' }

const sendEmail = () => {
  window.location.href = `mailto:${contactEmail}`
}

const openRdvPage = () => {
  window.open('https://rdv.anct.gouv.fr/org/1769/protect-envi', '_blank', 'noopener,noreferrer')
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
