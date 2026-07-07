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
        <p class="fr-text--lead" style="margin-bottom: 0">
          Gestion et suivi opérationnel des procédures administratives collectives.
        </p>
      </div>
    </div>
    <div class="fr-tabs" style="box-shadow: none">
      <ul class="fr-tabs__list" role="tablist">
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'dashboard'"
            role="tab"
            @click="currentTab = 'dashboard'"
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
            @click="currentTab = 'list'"
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
            @click="currentTab = 'detail'"
          >
            <span class="fr-icon-file-text-line fr-mr-1w" aria-hidden="true"></span>
            Détail procédure {{ selectedProcedureId ? `#${selectedProcedureId}` : '' }}
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'stats'"
            role="tab"
            @click="currentTab = 'stats'"
          >
            <span class="fr-icon-line-chart-line fr-mr-1w" aria-hidden="true"></span>
            Statistiques
          </button>
        </li>
      </ul>
      <DashboardTab v-if="currentTab === 'dashboard'" />

      <ProceduresTab v-if="currentTab === 'list'" @view-detail="viewDetail" />

      <DetailTab v-if="currentTab === 'detail'" :selectedProcedureId="selectedProcedureId" />

      <StatsTab v-if="currentTab === 'stats'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import DashboardTab from '@/components/backoffice/DashboardTab.vue'
import DetailTab from '@/components/backoffice/DetailTab.vue'
import ProceduresTab from '@/components/backoffice/ProceduresTab.vue'
import StatsTab from '@/components/backoffice/StatsTab.vue'
import { useBackofficeStore } from '@/stores/backoffice'
import { onMounted, ref } from 'vue'

const store = useBackofficeStore()
const currentTab = ref('dashboard')
const selectedProcedureId = ref<number | null>(null)

onMounted(async () => {
  await store.fetchProcedures()
})

const viewDetail = (id: number) => {
  selectedProcedureId.value = id
  currentTab.value = 'detail'
}
</script>

<style>
@import '@/styles/backoffice.css';
</style>
