<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
      </div>
      <div v-if="userInfo?.is_authenticated" class="fr-col-auto">
        <DsfrButton
          label="Synchroniser avec Démarche Numérique"
          secondary
          icon="fr-icon-refresh-line"
          :disabled="dossierStore.syncing"
          @click="handleManualSync"
        />
      </div>
    </div>

    <ChargementDossier
      v-if="showLoading || dossierStore.syncing"
      :message="
        dossierStore.syncing
          ? 'Synchronisation avec Démarche Numérique...'
          : 'Récupération de vos procédures...'
      "
    />

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
          <div class="fr-card fr-card--no-arrow">
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
                    <DsfrButton
                      label="Voir sur Démarche Numérique"
                      secondary
                      icon="fr-icon-external-link-line"
                      icon-right
                      @click="openExternalLink(getDnModifyUrl(String(dossier.numero_dossier)))"
                    />
                  </li>
                  <li>
                    <DsfrButton
                      label="Suivre la procédure"
                      icon="fr-icon-file-line"
                      icon-right
                      @click="router.push(getSuiviProcedureUrl(dossier.numero_dossier))"
                    />
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="dossiers.length === 0 && userInfo?.is_authenticated" class="fr-mt-5w">
        <DsfrAlert
          title="Aucune procédure trouvée"
          description="Aucune procédure trouvée sur Démarche Numérique."
          type="info"
        />
      </div>
    </div>
    <LoginInvitation v-else />
  </div>
</template>

<script setup lang="ts">
import { useDossierStore } from '@/stores/dossier'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import DossierMetadata from '../components/dossiers/DossierMetadata.vue'
import ChargementDossier from '../components/dossiers/ChargementDossier.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { getDnModifyUrl, getSuiviProcedureUrl } from '../services/urls'
import { openExternalLink } from '../utils/browser'

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




const handleManualSync = async () => {
  try {
    await dossierStore.syncDossiers(true)
  } catch (error) {
    console.error('Manual sync failed:', error)
  }
}
</script>

<style scoped>
.shadow-card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e5e5;
}
</style>
