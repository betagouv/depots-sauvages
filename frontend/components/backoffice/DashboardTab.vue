<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- KPI Cards Grid -->
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

    <!-- Section: Actions requises -->
    <div class="fr-mb-3w">
      <h2 class="fr-h4" style="display: flex; align-items: center; gap: 0.5rem">
        <span
          class="fr-icon-warning-line style-icon"
          style="color: #d97706"
          aria-hidden="true"
        ></span>
        Procédures nécessitant une action prioritaire
      </h2>
      <div class="bo-table-container">
        <table class="bo-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Commune</th>
              <th>Utilisateur</th>
              <th>Étape</th>
              <th>Statut</th>
              <th>Depuis</th>
              <th>Chargé Dépl.</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="procedure in store.proceduresRequiringAction" :key="procedure.id">
              <td>
                <code>#{{ procedure.id }}</code>
              </td>
              <td>
                <strong>{{ procedure.commune }}</strong>
              </td>
              <td>
                <a :href="'mailto:' + procedure.user_email" style="font-size: 0.8rem">{{
                  procedure.user_email
                }}</a>
              </td>
              <td>
                <span class="bo-dot bo-dot--active fr-mr-1v"></span>
                {{ procedure.suivi_procedure.etape_en_cours }}
              </td>
              <td>
                <span :class="getBadgeClass(getProcedureStatut(procedure))">
                  {{ getProcedureStatut(procedure) }}
                </span>
              </td>
              <td>{{ getDepuisText(procedure.date_constat) }}</td>
              <td>
                <span
                  v-if="procedure.suivi_procedure.charge_deploiement === 'Non assigné'"
                  style="color: #d97706; font-weight: 700"
                >
                  ⚠ Non assigné
                </span>
                <span v-else>{{ procedure.suivi_procedure.charge_deploiement }}</span>
              </td>
              <td>
                <button class="fr-btn fr-btn--sm" @click="$emit('view-detail', procedure.id)">
                  Gérer
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { getBadgeClass, getDepuisText, getProcedureStatut } from '@/utils/backoffice'

const store = useBackofficeStore()

defineEmits<{
  (e: 'view-detail', id: number): void
}>()
</script>

<style scoped>
.style-icon {
  font-size: 1.15rem;
}
</style>
