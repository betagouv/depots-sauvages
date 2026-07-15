<template>
  <div>
    <div v-if="showLoading" class="fr-container fr-py-6w">
      <PageLoader />
    </div>

    <div v-else>
      <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
        <div class="fr-container">
          <h1 class="fr-h1 fr-mb-3w">Démarrer une procédure dépôt sauvage</h1>
          <p class="fr-text fr-text--lead fr-mb-0">
            Nous allons vous guider étape par étape. Pour engager une procédure, la première étape
            consiste à établir le constat du dépôt sauvage.
          </p>
        </div>
      </div>

      <div class="fr-container fr-pb-8w">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <div class="premium-card premium-card--small premium-card--static premium-card--align-left">
              <h2 class="fr-h4">Ce dont vous avez besoin pour commencer la constatation :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list">
                <li>
                  <span class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w" aria-hidden="true"></span>
                  <span>Informations concernant le dépôt sauvage : localisation, volume estimé, types de déchets, etc.</span>
                </li>
                <li>
                  <span class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w" aria-hidden="true"></span>
                  <span>Identité de la personne habilitée qui a constaté les dépôts sauvages</span>
                </li>
                <li>
                  <span class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w" aria-hidden="true"></span>
                  <span>Informations sur l'auteur présumé (si connues)</span>
                </li>
                <li>
                  <span class="fr-icon-time-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
                  <span>Temps estimé : 7 minutes</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <div class="premium-card premium-card--small premium-card--static premium-card--align-left">
              <h2 class="fr-h4">À l'issue de cette étape :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list">
                <li>
                  <span class="fr-icon-file-text-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
                  <span>Rapport de constatation généré automatiquement</span>
                </li>
                <li>
                  <span class="fr-icon-file-text-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
                  <span>Lettre d'information prête à être envoyée (si l'auteur présumé est identifié)</span>
                </li>
                <li>
                  <span class="fr-icon-arrow-right-line fr-text-default--info fr-mr-1w" aria-hidden="true"></span>
                  <span>Vous serez guidé étape par étape pour faire avancer la procédure adaptée à votre situation</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="constatation-actions">
          <template v-if="userInfo?.is_authenticated">
            <div class="premium-text-center">
              <router-link
                to="/constatation"
                class="fr-btn fr-btn--lg"
                title="Démarrer la constatation"
              >
                Démarrer la constatation
              </router-link>
            </div>

            <PremiumCallout
              type="banner"
              title="Vous avez un doute ?"
              description="Vous ne savez pas si votre situation permet d'engager une procédure ?"
              iconClass="fr-icon-question-line"
              buttonText="Vérifier ma situation en 2 min"
              buttonTo="/demarrer-constatation/simulateur"
            />
          </template>

          <template v-else>
            <PremiumCallout
              type="banner"
              title="Vous avez un doute ?"
              description="Vous ne savez pas si votre situation permet d'engager une procédure ?"
              iconClass="fr-icon-question-line"
              buttonText="Vérifier ma situation en 2 min"
              buttonTo="/demarrer-constatation/simulateur"
            />

            <LoginInvitation
              title="Connectez-vous pour démarrer la constatation"
              description="Pour initier une procédure et accéder au formulaire de constatation de dépôt sauvage, vous devez vous connecter avec ProConnect."
              redirectTo="/constatation"
            />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import PageLoader from '../components/shared/PageLoader.vue'
import PremiumCallout from '../components/shared/PremiumCallout.vue'
import { useTallyRoutes } from '../composables/useTally'
import { getUserInfo, type UserInfo } from '../services/api'

const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)

useTallyRoutes({
  '/demarrer-constatation/simulateur': {
    formId: 'A7xA8z',
    options: { layout: 'modal', width: 900 },
    returnPath: '/demarrer-constatation',
  },
})

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.premium-card--align-left {
  align-items: flex-start;
  text-align: left;
}

.premium-choices-list {
  padding-left: 0;
  list-style-type: none;
}

.premium-choices-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.premium-choices-list li:last-child {
  margin-bottom: 0;
}

.premium-choices-list li span:first-child {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.constatation-actions {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  margin-top: 3rem;
}

.constatation-actions :deep(.premium-alert-banner) {
  margin: 0 !important;
}

.constatation-actions :deep(.premium-block-container) {
  padding-top: 0 !important;
}
</style>
