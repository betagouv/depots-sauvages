<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div class="bo-dashboard-grid">
      <div class="bo-kpi-card">
        <div class="bo-kpi-val">{{ store.stats.totalActive }}</div>
        <div class="bo-kpi-lbl">Procédures actives</div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #d97706">{{ store.stats.actionRequired }}</div>
        <div class="bo-kpi-lbl">Action requise</div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #2563eb">{{ store.stats.arWaiting }}</div>
        <div class="bo-kpi-lbl">AR en attente</div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #7c3aed">{{ store.stats.decisionToTake }}</div>
        <div class="bo-kpi-lbl">Décision à prendre</div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #059669">{{ store.stats.closedThisMonth }}</div>
        <div class="bo-kpi-lbl">Clôturées ce mois</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'

const store = useBackofficeStore()
</script>

