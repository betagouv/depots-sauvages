<template>
  <DefaultLayout>
    <router-view />
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/default-layout.vue'
import { getUserInfo } from '@/services/api'
import { useProcedureStore } from '@/stores/procedure'
import { onMounted } from 'vue'

const procedureStore = useProcedureStore()

onMounted(async () => {
  try {
    const userInfo = await getUserInfo()
    if (userInfo.is_authenticated) {
      // Fetch initial data to make it available everywhere
      await procedureStore.fetchProcedures()
    }
  } catch (error) {
    console.error('Error checking auth:', error)
  }
})
</script>
