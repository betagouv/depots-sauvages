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
                  ✅ informations concernant le dépôt sauvage : localisation, volume estimé, types
                  de déchets, etc.
                </li>
                <li>✅ identité de la personne habilitée qui a constaté les dépôts sauvages</li>
                <li>✅ Informations sur l'auteur présumé (si connues)</li>
                <li>⏱️ Temps estimé 7 minutes</li>
              </ul>
            </div>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <div class="premium-card premium-card--small premium-card--static premium-card--align-left">
              <h2 class="fr-h4">À l'issue de cette étape :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list">
                <li>📄 Rapport de constatation généré automatiquement</li>
                <li>
                  📄 Lettre d'information prête à être envoyée (si l'auteur présumé est identifié)
                </li>
                <li>
                  ➡️ Vous serez guidé étape par étape pour faire avancer la procédure adaptée à
                  votre situation
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="constatation-actions">
          <template v-if="userInfo?.is_authenticated">
            <div style="text-align: center">
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
  padding-left: 1.5rem;
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
