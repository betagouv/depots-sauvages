<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div class="bo-dashboard-grid">
      <div class="bo-kpi-card">
        <div class="bo-kpi-val">{{ store.stats.totalActive }}</div>
        <div class="bo-kpi-lbl">Procédures actives</div>
        <div class="bo-kpi-desc">
          Procédures réelles en cours d'instruction - non closes et non archivées
        </div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val bo-kpi-val--info">{{ store.stats.arWaiting }}</div>
        <div class="bo-kpi-lbl">AR en attente</div>
        <div class="bo-kpi-desc">
          Lettres recommandées envoyées dont l'accusé de réception est attendu
        </div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val bo-kpi-val--purple">{{ store.stats.decisionToTake }}</div>
        <div class="bo-kpi-lbl">Décision à prendre</div>
        <div class="bo-kpi-desc">
          Procédures à l'étape en attente de choix de poursuite : sanction / abandon
        </div>
      </div>
    </div>

    <!-- Treatment Status Distribution -->
    <div class="fr-mt-4w">
      <h3 class="fr-h5 bo-flex-center-gap">
        <span class="fr-icon-clipboard-fill fr-text-title-blue-france" aria-hidden="true"></span>
        Statut de traitement des procédures
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <router-link
          v-for="(count, status) in store.proceduresByStatus"
          :key="status"
          :to="{ path: '/procedures-liste', query: { traitement: status } }"
          class="fr-col-12 fr-col-sm-6 fr-col-md bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-status-card" :class="getStatusCardClass(status)">
            <p class="fr-text--sm fr-mb-1v fr-text-mention--grey">
              {{ status }}
            </p>
            <p class="fr-h3 fr-mb-0">{{ count }} {{ count > 1 ? 'procédures' : 'procédure' }}</p>
          </div>
        </router-link>
      </div>
    </div>

    <div class="fr-mt-4w">
      <h3 class="fr-h5 bo-flex-center-gap">
        <span class="fr-icon-user-fill fr-text-title-blue-france" aria-hidden="true"></span>
        Répartition du traitement des procédures
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <router-link
          v-for="(count, agent) in store.workloadByAssignee"
          :key="agent"
          :to="{ path: '/procedures-liste', query: { charge: getAssigneeIdByName(agent) } }"
          class="fr-col-12 fr-col-md-4 bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-workload-card">
            <p class="fr-text--sm fr-mb-1v fr-text-mention--grey">
              {{ agent }}
            </p>
            <p class="fr-h3 fr-mb-0">{{ count }} {{ count > 1 ? 'procédures' : 'procédure' }}</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'

const store = useBackofficeStore()

const getStatusCardClass = (status: string) => {
  if (status === 'Nouveau') return 'bo-status-card--nouveau'
  if (status === 'Ouvert') return 'bo-status-card--ouvert'
  if (status === 'En pause') return 'bo-status-card--pause'
  if (status === 'Résolu') return 'bo-status-card--resolu'
  if (status === 'Clôturé') return 'bo-status-card--cloture'
  return ''
}

const getAssigneeIdByName = (name: string) => {
  const assignee = store.assignees.find((a) => a.name === name)
  return assignee ? (assignee.id ?? 'None') : 'Tous'
}
</script>
