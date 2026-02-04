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
          <DsfrCard
            :title="dossier.title"
            :description="getDossierDescription(dossier)"
            :buttons="[
              {
                label: 'Voir sur Démarche Numérique',
                onClick: () => openExternalLink(getDnModifyUrl(String(dossier.numero_dossier))),
                icon: { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' },
                class: 'fr-btn--secondary',
              },
              {
                label: 'Documents de procédure',
                onClick: () => router.push(getSignalementDocumentsUrl(dossier.id)),
                icon: { name: 'ri-file-list-line', scale: 1.5, class: 'fr-mr-1w' },
              },
            ]"
          />
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
import { useDossierStore } from '@/stores/dossier'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import DnLoading from '../components/dn/DnLoading.vue'
import { getUserInfo, type UserDossier, type UserInfo } from '../services/api'
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

const getDossierDescription = (dossier: UserDossier) => {
  let desc = `Créé le ${formatDate(dossier.date_creation)}`
  if (dossier.date_modification) {
    desc += ` · Modifié le ${formatDate(dossier.date_modification)}`
  }
  return desc
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
