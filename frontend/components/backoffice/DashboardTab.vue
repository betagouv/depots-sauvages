<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div class="bo-dashboard-grid">
      <div class="bo-kpi-card">
        <div class="bo-kpi-val">{{ store.stats.totalActive }}</div>
        <div class="bo-kpi-lbl">Procédures actives</div>
        <div class="bo-kpi-desc">
          Dossiers réels en cours d'instruction - non clos et non archivés
        </div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #d97706">{{ store.stats.actionRequired }}</div>
        <div class="bo-kpi-lbl">Action requise</div>
        <div class="bo-kpi-desc">Dossiers nécessitant une intervention prioritaire immédiate</div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #2563eb">{{ store.stats.arWaiting }}</div>
        <div class="bo-kpi-lbl">AR en attente</div>
        <div class="bo-kpi-desc">
          Lettres recommandées envoyées dont l'accusé de réception est attendu
        </div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #7c3aed">{{ store.stats.decisionToTake }}</div>
        <div class="bo-kpi-lbl">Décision à prendre</div>
        <div class="bo-kpi-desc">
          Procédures à l'étape en attente de choix de poursuite : sanction / abandon
        </div>
      </div>
      <div class="bo-kpi-card">
        <div class="bo-kpi-val" style="color: #059669">{{ store.stats.closedThisMonth }}</div>
        <div class="bo-kpi-lbl">Clôturées ce mois</div>
        <div class="bo-kpi-desc">Dossiers finalisés ou archivés au cours du mois</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'

const store = useBackofficeStore()
</script>
