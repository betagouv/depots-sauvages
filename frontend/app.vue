<template>
  <DefaultLayout>
    <router-view />
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/default-layout.vue'
import { getUserInfo } from '@/services/api'
import { useDossierStore } from '@/stores/dossier'
import { onMounted } from 'vue'

const dossierStore = useDossierStore()

onMounted(async () => {
  try {
    const userInfo = await getUserInfo()
    if (userInfo.is_authenticated) {
      // Fetch initial data to make it available everywhere
      await dossierStore.fetchDossiers()

      // Trigger background sync if not already done in this session
      if (!dossierStore.isSynced) {
        dossierStore.syncDossiers()
      }
    }
  } catch (error) {
    console.error('Error checking auth for sync:', error)
  }
})
</script>
