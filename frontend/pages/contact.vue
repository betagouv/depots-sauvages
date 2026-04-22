<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Contactez-nous</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Contactez-nous et posez vos questions sur Protect’Envi et les procédures dépôts sauvages
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
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
                onClick: () => router.push({ name: 'RDV' }),
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
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'
import { useRouter } from 'vue-router'

const router = useRouter()
const contactEmail = import.meta.env.VITE_CONTACT_EMAIL

const chatIcon = { name: 'ri-chat-1-line', scale: 1.5, class: 'fr-mr-1w' }
const emailIcon = { name: 'ri-mail-line', scale: 1.5, class: 'fr-mr-1w' }

const sendEmail = () => {
  window.location.href = `mailto:${contactEmail}`
}

const openCrispChat = () => {
  const crisp = (window as any).$crisp
  if (crisp) {
    crisp.push(['do', 'chat:open'])
  }
}
</script>
