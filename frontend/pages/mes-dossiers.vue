<template>
  <div class="fr-container fr-py-5w">
    <h1>Mes procédures</h1>

    <DnLoading v-if="showLoading" message="Récupération de vos procédures..." />

    <div v-else>
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
                  <div class="fr-text--xs fr-mb-2w">
                    <span
                      class="fr-icon-calendar-line fr-icon--sm fr-mr-1v"
                      aria-hidden="true"
                    ></span>
                    Créé le {{ formatDate(dossier.date_creation) }}
                    <span v-if="dossier.date_modification">
                      &middot; Modifié le {{ formatDate(dossier.date_modification) }}
                    </span>
                  </div>

                  <div v-if="dossier.date_constat || dossier.localisation_depot">
                    <div class="fr-grid-row fr-grid-row--gutters">
                      <div v-if="dossier.date_constat" class="fr-col-12 fr-col-md-6">
                        <strong>Date de constatation :</strong> <br />
                        {{ formatDate(dossier.date_constat) }}
                      </div>
                      <div v-if="dossier.localisation_depot" class="fr-col-12 fr-col-md-6">
                        <strong>Adresse du dépôt :</strong> <br />
                        {{ dossier.localisation_depot }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="fr-card__footer">
                <ul class="fr-btns-group fr-btns-group--inline-lg">
                  <li>
                    <DsfrButton
                      label="Voir sur Démarche Numérique"
                      class="fr-btn--secondary"
                      :icon="{ name: 'ri-external-link-line', class: 'fr-mr-1w' }"
                      icon-right
                      @click="openExternalLink(getDnModifyUrl(String(dossier.numero_dossier)))"
                    />
                  </li>
                  <li>
                    <DsfrButton
                      label="Documents de procédure"
                      :icon="{ name: 'ri-file-list-line', class: 'fr-mr-1w' }"
                      icon-right
                      @click="router.push(getSignalementDocumentsUrl(dossier.id))"
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
  </div>
</template>

<script setup lang="ts">
import { useDossierStore } from '@/stores/dossier.ts'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import DnLoading from '../components/dn/DnLoading.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { getDnModifyUrl, getSignalementDocumentsUrl } from '../services/urls'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const dossierStore = useDossierStore()
const showLoading = ref(true)

const dossiers = computed(() => dossierStore.dossiers)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      await dossierStore.fetchDossiers()
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})

const openExternalLink = (url: string) => {
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return 'Date inconnue'
  return new Date(dateStr).toLocaleString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.shadow-card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e5e5;
}
</style>
