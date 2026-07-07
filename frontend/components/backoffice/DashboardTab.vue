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
      <div class="bo-kpi-card">
        <div class="bo-kpi-val bo-kpi-val--success">{{ store.stats.closedThisMonth }}</div>
        <div class="bo-kpi-lbl">Clôturées ce mois</div>
        <div class="bo-kpi-desc">Procédures finalisées ou archivées au cours du mois</div>
      </div>
    </div>

    <div class="fr-mt-4w">
      <h3 class="fr-h5 bo-flex-center-gap">
        <span class="fr-icon-user-fill fr-text-title-blue-france" aria-hidden="true"></span>
        Répartition du traitement des procédures
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div
          v-for="(count, agent) in store.workloadByAssignee"
          :key="agent"
          class="fr-col-12 fr-col-md-4"
        >
          <div class="premium-box fr-p-2w bo-workload-card">
            <p class="fr-text--sm fr-mb-1v fr-text-mention--grey">
              {{ agent }}
            </p>
            <p class="fr-h3 fr-mb-0">{{ count }} {{ count > 1 ? 'procédures' : 'procédure' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'

const store = useBackofficeStore()
</script>
