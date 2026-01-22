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
          title="Besoin d'un accompagnement ?"
          description="Participez à un webinaire collectif ou réservez une session d'accompagnement individuelle pour votre cas concret."
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

    <section class="fr-mt-6w">
      <h2 class="fr-h3 fr-mb-3w">Ressources utiles</h2>

      <DsfrCallout class="fr-mb-3w" title="Guide ACDéchets" content="">
        <p class="fr-text fr-mb-0">
          Pour un accompagnement pas à pas, consultez le
          <a
            href="https://acdechets.smartidf.services/aide-verbalisation"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
            rel="noopener"
          >
            guide ACDéchets de la Région Île-de-France
          </a>
        </p>
      </DsfrCallout>

      <DsfrCallout title="Application Gend'élus" content="">
        <p class="fr-text fr-mb-2w">
          Retrouvez des conseils pratiques sur l'application à destination des élus, Gend'élus,
          accessible à tout le monde :
        </p>
        <ul class="fr-pl-2w fr-mb-0">
          <li>
            <a
              href="https://play.google.com/store/apps/details?id=com.gendelus&hl=fr&pli=1"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noreferrer noopener"
            >
              Télécharger sur le Play Store
            </a>
          </li>
          <li>
            <a
              href="https://apps.apple.com/fr/app/gend%C3%A9lus/id6444316373"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noreferrer noopener"
            >
              Télécharger sur l'App Store
            </a>
          </li>
        </ul>
      </DsfrCallout>
    </section>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL
const rdvPageUrl = import.meta.env.VITE_RDV_PAGE_URL || 'https://rdv.anct.gouv.fr/prendre_rdv'

const chatIcon = { name: 'ri-chat-1-line', scale: 1.5, class: 'fr-mr-1w' }
const emailIcon = { name: 'ri-mail-line', scale: 1.5, class: 'fr-mr-1w' }
const externalLinkIcon = { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' }

const sendEmail = () => {
  window.location.href = `mailto:${contactEmail}`
}

const openRdvPage = () => {
  window.open(rdvPageUrl, '_blank', 'noopener,noreferrer')
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
