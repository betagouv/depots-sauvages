<template>
  <div class="fr-container fr-py-5w">
    <h1>Mes dossiers</h1>

    <div v-if="userInfo && userInfo.is_authenticated" class="fr-mb-4w">
      <p v-if="userInfo.first_name && userInfo.last_name" class="fr-text--lead">
        Utilisateur connecté :
        <strong>{{ userInfo.first_name }} {{ userInfo.last_name }}</strong>
        <span v-if="userInfo.email"> - {{ userInfo.email }}</span>
      </p>
    </div>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="dossier in dossiers" :key="dossier.id" class="fr-col-12 fr-col-md-6">
        <DsfrCard
          :title="formatTitle(dossier)"
          no-arrow
          :buttons="[
            {
              label: 'Voir sur Démarche Numérique',
              secondary: true,
              icon: { name: 'ri-external-link-line', scale: 1, class: 'fr-mr-1w' },
              onClick: () => openDn(dossier),
            },
            {
              label: 'Documents de procédure',
              onClick: () => openLocal(dossier.id),
            },
          ]"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getUserDossiers, getUserInfo, type UserDossier, type UserInfo } from '../services/api'
import { getDnModifyUrl } from '../services/urls'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const dossiers = ref<UserDossier[]>([])

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      dossiers.value = await getUserDossiers()
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  }
})

const openDn = (dossier: UserDossier) => {
  const url = getDnModifyUrl(String(dossier.numero_dossier))
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

const openLocal = (id: number) => {
  router.push(`/signalements-dn/${id}`)
}

const formatTitle = (dossier: UserDossier) => {
  const dateStr = dossier.date_creation
    ? new Date(dossier.date_creation).toLocaleDateString('fr-FR')
    : 'Date inconnue'
  return `Dossier #${dossier.numero_dossier} - Créé le ${dateStr}`
}
</script>
