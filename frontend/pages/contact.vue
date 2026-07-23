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
                <h4 class="fr-card__title">Participez à notre webinaire gratuit</h4>
                <p class="fr-card__desc">
                  Chaque semaine notre équipe vous présente comment agir contre les dépôts
                  sauvages en moins de 60 minutes.
                </p>
              </div>
              <div class="fr-card__footer">
                <ul class="fr-btns-group">
                  <li>
                    <DsfrButton secondary @click="() => router.push({ name: 'RDV' })">
                      <span class="fr-icon-calendar-line fr-mr-1w" aria-hidden="true"></span>
                      Découvrir notre webinaire
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

        <DsfrCallout class="fr-mb-3w" title="ACDéchets" content="">
          <p class="fr-text fr-mb-2w">
            Un guide pédagogique pas à pas proposé par la Région Île-de-France pour aider les
            collectivités.
          </p>
          <p class="fr-text fr-mb-0">
            <a
              href="https://acdechets.smartidf.services/aide-verbalisation"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noopener"
            >
              Découvrez le guide ACDéchets
            </a>
          </p>
        </DsfrCallout>

        <DsfrCallout title="Gend'Élus" content="">
          <p class="fr-text fr-mb-2w">
            Un site web pour accompagner les élus sur toutes les problématiques sécuritaires
            auxquelles ils peuvent être confrontés :
          </p>
          <ul class="fr-text--md fr-pl-2w fr-mb-2w">
            <li>
              fiches conseils et modules de sensibilisation aux risques cyber et enjeux
              environnementaux ;
            </li>
            <li>tchat avec un gendarme 24h/24 7j/7 ;</li>
            <li>partage de bonnes pratiques et de ressources utiles ;</li>
          </ul>
          <p class="fr-text fr-mb-0">
            <a
              href="https://www.gendarmerie.interieur.gouv.fr/gendelus"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noopener"
            >
              Découvrir Gend'Élus
            </a>
          </p>
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
