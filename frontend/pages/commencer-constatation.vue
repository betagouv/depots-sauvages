<template>
  <div>
    <div v-if="showLoading" class="fr-container fr-py-6w">
      <div class="fr-grid-row fr-grid-row--center fr-my-8w">
        <div class="fr-col-12 fr-col-md-6 text-center">
          <span
            class="fr-icon-refresh-line fr-icon--lg"
            aria-hidden="true"
            style="animation: spin 1s linear infinite"
          ></span>
          <p class="fr-mt-2w">Chargement de la page...</p>
        </div>
      </div>
    </div>

    <div v-else>
      <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
        <div class="fr-container">
          <h1 class="fr-h1 fr-mb-3w">Lancer une procédure</h1>
          <p class="fr-text fr-text--lead fr-mb-0">
            Pour initier une procédure, vous devez commencer par établir le constat du dépôt
            sauvage.
          </p>
        </div>
      </div>

      <div class="fr-container fr-pb-8w">
        <PremiumCallout
          v-if="dossiersCount > 0"
          type="banner"
          title="Vous avez déjà des procédures en cours"
          :description="`Vous avez actuellement <strong>${dossiersCount} procédure${dossiersCount > 1 ? 's' : ''} en cours</strong>.`"
          iconClass="fr-icon-folder-2-line"
          buttonText="Voir mes procédures en cours"
          buttonTo="/mes-procedures"
        >
          <template #button-icon>
            <span class="fr-icon-eye-line fr-mr-1w" aria-hidden="true"></span>
          </template>
        </PremiumCallout>

        <PremiumCallout
          description="Avant de démarrer votre constatation, vous pouvez vérifier votre éligibilité à la procédure administrative."
          iconClass="fr-icon-question-line"
          buttonText="Je vérifie mon éligibilité grâce au simulateur"
          @click="openSimulator"
        />

        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <div
              class="premium-card premium-card--small premium-card--static"
              style="align-items: flex-start; text-align: left"
            >
              <h2 class="fr-h4">De quoi avez-vous besoin pour réaliser cette constatation ?</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list" style="padding-left: 1.5rem">
                <li>
                  Les informations concernant le dépôt sauvage : localisation, descriptions du
                  dépôt, volumes, types de déchets, etc.
                </li>
                <li>L'identité de la personne habilitée qui a constaté les dépôts sauvages</li>
                <li>Les informations éventuelles sur le responsable présumé</li>
                <li>Cette démarche nécessite une authentification via ProConnect.</li>
              </ul>
            </div>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <div
              class="premium-card premium-card--small premium-card--static"
              style="align-items: flex-start; text-align: left"
            >
              <h2 class="fr-h4">À l'issue de la constatation :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list" style="padding-left: 1.5rem">
                <li>
                  Vous pourrez récupérer les documents personnalisés utiles pour votre procédure
                </li>
                <li>
                  Vous serez guidé étape par étape pour vous permettre d'initier la procédure
                  adaptée à votre situation
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div v-if="userInfo?.is_authenticated" class="fr-mt-6w" style="text-align: center">
          <router-link
            to="/constatation"
            class="fr-btn fr-btn--lg"
            title="Démarrer la constatation"
          >
            Démarrer la constatation
          </router-link>
        </div>

        <LoginInvitation
          v-else
          title="Connectez-vous pour démarrer"
          description="Pour initier une procédure et accéder au formulaire de constatation de dépôt sauvage, vous devez vous connecter avec ProConnect."
          redirectTo="/constatation"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import PremiumCallout from '../components/shared/PremiumCallout.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { openTallyPopup } from '../utils/tally'

const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)

const dossiersCount = computed(() => userInfo.value?.procedures_count || 0)

const openSimulator = () => {
  openTallyPopup('A7xA8z', { layout: 'modal', width: 900 })
}

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
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.text-center {
  text-align: center;
}
.text-blue {
  color: var(--text-active-blue-france);
}

.font-premium {
  font-weight: 700;
  color: var(--text-title-blue-france);
}

.text-muted {
  color: var(--text-mention-grey);
}

@media (min-width: 768px) {
  .text-md-right {
    text-align: right;
  }
}
</style>
