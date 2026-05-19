<template>
  <div class="fr-container fr-py-6w">
    <div v-if="showLoading" class="fr-grid-row fr-grid-row--center fr-my-8w">
      <div class="fr-col-12 fr-col-md-6 text-center">
        <span
          class="fr-icon-refresh-line fr-icon--lg"
          aria-hidden="true"
          style="animation: spin 1s linear infinite"
        ></span>
        <p class="fr-mt-2w">Chargement de la page...</p>
      </div>
    </div>

    <div v-else>
      <h1 class="fr-h1 fr-mb-2w">Commencer une constatation</h1>

      <p class="fr-text--lead fr-mb-4w">
        Pour initier une procédure, vous devez matérialiser le dépôt sauvage dans un rapport de
        constatation.
      </p>

      <DsfrAlert type="info" class="fr-mb-4w">
        <p class="fr-mb-0">
          Avant de démarrer votre constatation, vous pouvez vérifier votre éligibilité à la
          procédure administrative.
          <strong>
            <a href="#" @click.prevent="openSimulator">
              Je vérifie mon éligibilité grâce au simulateur
            </a>
          </strong>
        </p>
      </DsfrAlert>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <div
            class="premium-card premium-card--small premium-card--static"
            style="align-items: flex-start; text-align: left"
          >
            <h2 class="fr-h4">De quoi avez-vous besoin pour réaliser cette constatation ?</h2>
            <ul class="fr-text--sm fr-mb-0 premium-choices-list" style="padding-left: 1.5rem">
              <li>
                Les informations concernant le dépôt sauvage : localisation, descriptions du dépôt,
                volumes, types de déchets, etc.
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
                Vous serez guidé étape par étape pour vous permettre d'initier la procédure adaptée
                à votre situation
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div v-if="userInfo?.is_authenticated" class="fr-mt-6w" style="text-align: center">
        <router-link
          to="/constatation/formulaire"
          class="fr-btn fr-btn--lg"
          title="Démarrer la constatation"
        >
          Démarrer la constatation
        </router-link>
      </div>

      <LoginInvitation
        v-else
        title="Connectez-vous pour démarrer"
        description="Pour initier une procédure et accéder au formulaire de constatation, vous devez vous connecter avec ProConnect."
        redirectTo="/constatation/formulaire"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert } from '@gouvminint/vue-dsfr'
import { onMounted, ref } from 'vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { openTallyPopup } from '../utils/tally'

const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)

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
</style>
