<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
      </div>
      <div v-if="userInfo?.is_authenticated" class="fr-col-auto">
        <router-link to="/demarrer-constatation" class="fr-btn">
          <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
          Démarrer une nouvelle constatation
        </router-link>
      </div>
    </div>

    <ChargementDossier v-if="showLoading" message="Récupération de vos procédures..." />

    <div v-else-if="userInfo?.is_authenticated">
      <div v-if="userInfo && userInfo.is_authenticated" class="fr-mb-4w">
        <p v-if="userInfo.first_name && userInfo.last_name" class="fr-text--lead">
          Utilisateur connecté :
          <strong>{{ userInfo.first_name }} {{ userInfo.last_name }}</strong>
          <span v-if="userInfo.email"> - {{ userInfo.email }}</span>
        </p>
      </div>

      <div v-if="dossiers.length > 0" class="fr-mb-2w">
        <p class="fr-text--bold">
          {{ dossiers.length }} procédure{{ dossiers.length > 1 ? 's' : '' }}
        </p>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-for="dossier in dossiers" :key="dossier.id" class="fr-col-12">
          <div class="fr-card fr-card--no-arrow shadow-card">
            <div class="fr-card__body">
              <div class="fr-card__content">
                <h3 class="fr-card__title">
                  {{ dossier.title }}
                </h3>
                <div class="fr-card__desc">
                  <DossierMetadata :dossier="dossier" />
                </div>
              </div>

              <div class="fr-card__footer">
                <ul class="fr-btns-group fr-btns-group--inline-lg">
                  <li>
                    <DsfrButton @click="router.push(getSuiviProcedureUrl(dossier.numero_dossier))">
                      <span class="fr-icon-file-line fr-mr-1w" aria-hidden="true"></span>
                      Suivre la procédure
                    </DsfrButton>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="dossiers.length === 0 && userInfo?.is_authenticated" class="fr-mt-5w">
        <DsfrAlert
          title="Aucune procédure en cours"
          description="Vous n'avez pas encore créé de constatation pour initier une procédure administrative."
          type="info"
        />
        <div class="fr-mt-4w" style="text-align: center">
          <router-link to="/demarrer-constatation" class="fr-btn fr-btn--lg">
            Débuter une procédure administrative
          </router-link>
        </div>
      </div>
    </div>
    <LoginInvitation v-else />
  </div>
</template>

<script setup lang="ts">
import { useDossierStore } from '@/stores/dossier'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import ChargementDossier from '../components/dossiers/ChargementDossier.vue'
import DossierMetadata from '../components/dossiers/DossierMetadata.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { getSuiviProcedureUrl } from '../services/urls'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const dossierStore = useDossierStore()
const showLoading = ref(true)

const dossiers = computed(() => dossierStore.dossiers)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      // Wait for global fetch to complete to ensure data is ready before hiding spinner
      await dossierStore.fetchDossiers()
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.shadow-card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e5e5;
}
</style>
