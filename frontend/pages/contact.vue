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
          <div class="fr-card fr-card--no-arrow">
            <div class="fr-card__body">
              <div class="fr-card__content">
                <h4 class="fr-card__title">Besoin d'une réponse rapide ?</h4>
                <p class="fr-card__desc">
                  Échangez avec nos équipes par chat ou envoyez-nous un e-mail pour obtenir des
                  réponses rapides à vos questions.
                </p>
              </div>
              <div class="fr-card__footer">
                <ul class="fr-btns-group fr-btns-group--inline">
                  <li>
                    <DsfrButton @click="openCrispChat">
                      <span class="fr-icon-chat-2-line fr-mr-1w" aria-hidden="true"></span>
                      Ouvrir le chat
                    </DsfrButton>
                  </li>
                  <li>
                    <DsfrButton secondary :disabled="!contactEmail" @click="sendEmail">
                      <span class="fr-icon-mail-line fr-mr-1w" aria-hidden="true"></span>
                      Envoyer un e-mail
                    </DsfrButton>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <div class="fr-card fr-card--no-arrow">
            <div class="fr-card__body">
              <div class="fr-card__content">
                <h4 class="fr-card__title">Besoin d'un accompagnement ?</h4>
                <p class="fr-card__desc">
                  Participez à un webinaire collectif ou réservez une session d'accompagnement
                  individuelle pour votre cas concret.
                </p>
              </div>
              <div class="fr-card__footer">
                <ul class="fr-btns-group">
                  <li>
                    <DsfrButton secondary @click="() => router.push({ name: 'RDV' })">
                      <span class="fr-icon-calendar-line fr-mr-1w" aria-hidden="true"></span>
                      Prendre rendez-vous
                    </DsfrButton>
                  </li>
                </ul>
              </div>
            </div>
          </div>
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
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { useRouter } from 'vue-router'

const router = useRouter()
const contactEmail = import.meta.env.VITE_CONTACT_EMAIL

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
