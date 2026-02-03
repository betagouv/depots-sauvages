<template>
  <div class="fr-container fr-py-5w">
    <h1>Mes dossiers</h1>

    <div v-if="userInfo && userInfo.is_authenticated" class="fr-mb-4w">
      <p v-if="userInfo.first_name && userInfo.last_name" class="fr-text--lead">
        Utilisateur connecté :
        <strong>{{ userInfo.first_name }} {{ userInfo.last_name }}</strong>
        <span v-if="userInfo.email">({{ userInfo.email }})</span>
      </p>
    </div>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="dossier in dossiers" :key="dossier.id" class="fr-col-12 fr-col-md-6">
        <DsfrCard
          :title="dossier.title"
          :description="dossier.description"
          :detail-display="dossier.detailDisplay"
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
import { getUserInfo, type UserInfo } from '../services/api'
import { getDnModifyUrl } from '../services/urls'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
})

const openDn = (dossier: any) => {
  const url = getDnModifyUrl(dossier.numero_dossier)
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

const openLocal = (id: string) => {
  router.push(`/signalements-dn/${id}`)
}

const dossiers = ref([
  {
    id: 'DN-2026-001',
    numero_dossier: '2026001',
    title: 'Dossier #2026001 - Créé le 12/01/2026',
    detailDisplay: 'En cours',
  },
  {
    id: 'DN-2026-002',
    numero_dossier: '2026002',
    title: 'Dossier #2026002 - Créé le 28/01/2026',
  },
])
</script>
