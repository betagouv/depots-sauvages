<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- Stats Générales -->
    <div>
      <h3 class="fr-h5 bo-flex-center-gap">
        <span class="fr-icon-line-chart-fill fr-text-title-blue-france" aria-hidden="true"></span>
        Statistiques générales
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <!-- Cas réels -->
        <router-link
          :to="{ path: '/procedures-liste', query: { casReels: 'Oui', auteurIdentifie: 'Tous' } }"
          class="fr-col-12 fr-col-sm-6 fr-col-md-3 bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-kpi-card-new">
            <div class="bo-kpi-val">{{ store.generalStats.real }}</div>
            <div class="bo-kpi-lbl">Cas réels</div>
            <div class="bo-kpi-desc">Procédures issues de signalements réels</div>
          </div>
        </router-link>

        <!-- Cas test -->
        <router-link
          :to="{ path: '/procedures-liste', query: { casReels: 'Non', auteurIdentifie: 'Tous' } }"
          class="fr-col-12 fr-col-sm-6 fr-col-md-3 bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-kpi-card-new bo-kpi-card-new--test">
            <div class="bo-kpi-val bo-kpi-val--grey">{{ store.generalStats.test }}</div>
            <div class="bo-kpi-lbl">Cas de test</div>
            <div class="bo-kpi-desc">Procédures créées à des fins de test</div>
          </div>
        </router-link>

        <!-- Auteur identifié -->
        <router-link
          :to="{ path: '/procedures-liste', query: { casReels: 'Oui', auteurIdentifie: 'Oui' } }"
          class="fr-col-12 fr-col-sm-6 fr-col-md-3 bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-kpi-card-new bo-kpi-card-new--success">
            <div class="bo-kpi-val bo-kpi-val--success">{{ store.generalStats.authorIdentified }}</div>
            <div class="bo-kpi-lbl">Auteur identifié</div>
            <div class="bo-kpi-desc">Procédures réelles où l'auteur est identifié</div>
          </div>
        </router-link>

        <!-- Auteur non identifié -->
        <router-link
          :to="{ path: '/procedures-liste', query: { casReels: 'Oui', auteurIdentifie: 'Non' } }"
          class="fr-col-12 fr-col-sm-6 fr-col-md-3 bo-dashboard-card-link"
          style="display: flex; flex-direction: column; text-decoration: none"
        >
          <div class="premium-box fr-p-2w bo-kpi-card-new bo-kpi-card-new--warning">
            <div class="bo-kpi-val bo-kpi-val--warning">{{ store.generalStats.authorNotIdentified }}</div>
            <div class="bo-kpi-lbl">Auteur non identifié</div>
            <div class="bo-kpi-desc">Procédures réelles où l'auteur n'est pas identifié</div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Stats des étapes de la procédure -->
    <div class="fr-mt-4w">
      <h3 class="fr-h5 bo-flex-center-gap">
        <span class="fr-icon-arrow-right-line fr-text-title-blue-france" aria-hidden="true"></span>
        Suivi des étapes de la procédure
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <!-- Auteur Identifié Column -->
        <div class="fr-col-12 fr-col-md-6">
          <div class="premium-box fr-p-3w bo-step-container-card">
            <h4 class="fr-h6 bo-step-group-title bo-step-group-title--identified">
              <span class="fr-icon-user-fill fr-mr-1w" aria-hidden="true"></span>
              Auteur identifié
            </h4>
            <div class="bo-step-list">
              <template v-for="step in stepsIdentified" :key="step.number">
                <router-link
                  v-if="step.label"
                  :to="{ path: '/procedures-liste', query: { casReels: 'Oui', auteurIdentifie: 'Oui', etape: step.number } }"
                  class="bo-step-row-link"
                >
                  <div class="bo-step-row">
                    <div class="bo-step-num-badge">{{ step.number }}</div>
                    <div class="bo-step-name">{{ step.label }}</div>
                    <div class="bo-step-count-badge">
                      {{ store.proceduresByStepAndAuthor.identified[step.number] || 0 }}
                    </div>
                  </div>
                </router-link>
              </template>
            </div>
          </div>
        </div>

        <!-- Auteur Non Identifié Column -->
        <div class="fr-col-12 fr-col-md-6">
          <div class="premium-box fr-p-3w bo-step-container-card">
            <h4 class="fr-h6 bo-step-group-title bo-step-group-title--unidentified">
              <span class="fr-icon-user-line fr-mr-1w" aria-hidden="true"></span>
              Auteur non identifié
            </h4>
            <div class="bo-step-list">
              <template v-for="step in stepsNotIdentified" :key="step.number">
                <router-link
                  v-if="step.label"
                  :to="{ path: '/procedures-liste', query: { casReels: 'Oui', auteurIdentifie: 'Non', etape: step.number } }"
                  class="bo-step-row-link"
                >
                  <div class="bo-step-row">
                    <div class="bo-step-num-badge bo-step-num-badge--warning">{{ step.number }}</div>
                    <div class="bo-step-name">{{ step.label }}</div>
                    <div class="bo-step-count-badge">
                      {{ store.proceduresByStepAndAuthor.notIdentified[step.number] || 0 }}
                    </div>
                  </div>
                </router-link>
              </template>
            </div>
          </div>
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
          :to="{ path: '/procedures-liste', query: { assignee: getAssigneeIdByName(agent) } }"
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
import { getStepLabel } from '@/utils/backoffice'

const store = useBackofficeStore()

const stepsIdentified = [
  { number: 0, label: getStepLabel(0, true) },
  { number: 1, label: getStepLabel(1, true) },
  { number: 2, label: getStepLabel(2, true) },
  { number: 3, label: getStepLabel(3, true) },
  { number: 4, label: getStepLabel(4, true) },
  { number: 5, label: getStepLabel(5, true) },
]

const stepsNotIdentified = [
  { number: 0, label: getStepLabel(0, false) },
  { number: 1, label: getStepLabel(1, false) },
  { number: 2, label: getStepLabel(2, false) },
  { number: 3, label: getStepLabel(3, false) },
  { number: 4, label: getStepLabel(4, false) },
  { number: 5, label: getStepLabel(5, false) },
]

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
