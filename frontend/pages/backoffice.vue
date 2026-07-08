<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-4w">
      <div class="fr-col">
        <h1
          class="fr-h1"
          style="margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem"
        >
          <span class="fr-icon-settings-5-line fr-text-title-blue-france" aria-hidden="true"></span>
          Back-office de Pilotage
        </h1>
      </div>
    </div>
    <div class="fr-tabs" style="box-shadow: none">
      <ul class="fr-tabs__list" role="tablist">
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'dashboard'"
            role="tab"
            @click="router.push('/tableau-de-bord')"
          >
            <span class="fr-icon-dashboard-line fr-mr-1w" aria-hidden="true"></span>
            Tableau de bord
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'list'"
            role="tab"
            @click="router.push('/procedures-liste')"
          >
            <span class="fr-icon-list-unordered fr-mr-1w" aria-hidden="true"></span>
            Procédures
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'detail'"
            role="tab"
            @click="
              router.push(
                selectedProcedureId
                  ? `/procedure-detail/${selectedProcedureId}`
                  : '/procedure-detail'
              )
            "
          >
            <span class="fr-icon-file-text-line fr-mr-1w" aria-hidden="true"></span>
            Détail procédure {{ selectedProcedureId ? `#${selectedProcedureId}` : '' }}
          </button>
        </li>
      </ul>
      <DashboardTab v-if="currentTab === 'dashboard'" />

      <ProceduresTab v-if="currentTab === 'list'" @view-detail="viewDetail" />

      <DetailTab v-if="currentTab === 'detail'" :selectedProcedureId="selectedProcedureId" />
    </div>
  </div>
</template>

<script setup lang="ts">
import DashboardTab from '@/components/backoffice/DashboardTab.vue'
import DetailTab from '@/components/backoffice/DetailTab.vue'
import ProceduresTab from '@/components/backoffice/ProceduresTab.vue'
import { useBackofficeStore } from '@/stores/backoffice'
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const store = useBackofficeStore()
const route = useRoute()
const router = useRouter()

const currentTab = computed(() => (route.meta.tab as string) || 'dashboard')
const selectedProcedureId = computed(() => {
  const id = route.params.procedureId
  return id ? parseInt(id as string, 10) : null
})

onMounted(async () => {
  await store.fetchProcedures()
})

const viewDetail = (id: number) => {
  router.push({
    path: `/procedure-detail/${id}`,
    query: route.query,
  })
}
</script>

<style>
@import '@/styles/backoffice.css';
</style>
