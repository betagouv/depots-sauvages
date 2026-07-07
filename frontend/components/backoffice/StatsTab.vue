<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div class="fr-mb-4w">
      <h3 class="fr-h5" style="display: flex; align-items: center; gap: 0.5rem">
        <span
          class="fr-icon-notification-3-line fr-text-title-blue-france"
          aria-hidden="true"
        ></span>
        Suivi des Objectifs & Résultats Clés (OKR S2 2026)
      </h3>
      <p
        class="fr-text--sm"
        style="color: var(--text-mention-grey); margin-top: -0.5rem; margin-bottom: 1.5rem"
      >
        Cibles prioritaires de l'équipe produit d'ici au 31 décembre 2026 (les indicateurs avec ⚡️
        sont calculés en temps réel).
      </p>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-for="(okr, key) in liveOkrs" :key="key" class="fr-col-12 fr-col-md-4">
          <div
            class="premium-box fr-p-2w"
            style="
              background: white;
              border-left: 4px solid var(--border-active-blue-france);
              height: 100%;
              display: flex;
              flex-direction: column;
              justify-content: space-between;
            "
          >
            <div>
              <div
                class="fr-text--xs fr-mb-1v"
                style="
                  color: var(--text-mention-grey);
                  font-weight: 700;
                  text-transform: uppercase;
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                "
              >
                <span
                  >{{ String(key).replace('_', '.').toUpperCase() }}
                  {{ okr.isLive ? '⚡️' : '' }}</span
                >
                <button
                  v-if="!okr.isLive && editingOkrKey !== key"
                  class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-icon-edit-line"
                  style="
                    padding: 0;
                    min-height: auto;
                    font-size: 0.8rem;
                    color: var(--border-active-blue-france);
                  "
                  title="Modifier manuellement la valeur"
                  @click="startEditOkr(String(key), okr.current)"
                ></button>
              </div>
              <p class="fr-text--sm fr-text--bold fr-mb-2w" style="line-height: 1.3">
                {{ okr.label }}
              </p>
            </div>
            <div>
              <div
                v-if="editingOkrKey === key"
                style="display: flex; gap: 0.5rem; align-items: center"
                class="fr-mb-2w"
              >
                <input
                  type="number"
                  v-model.number="editingOkrValue"
                  class="fr-input fr-input--sm"
                  style="width: 100px"
                />
                <button
                  class="fr-btn fr-btn--sm fr-icon-checkbox-circle-line"
                  style="padding: 0.25rem 0.5rem"
                  title="Enregistrer"
                  @click="saveOkr(String(key))"
                ></button>
                <button
                  class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-close-line"
                  style="padding: 0.25rem 0.5rem"
                  title="Annuler"
                  @click="editingOkrKey = null"
                ></button>
              </div>
              <div class="fr-grid-row fr-grid-row--middle fr-mb-1v">
                <div class="fr-col">
                  <span class="fr-text--md fr-text--bold">
                    {{ okr.current }}
                  </span>
                  <span class="fr-text--xs" style="color: var(--text-mention-grey)">
                    / {{ okr.target }} {{ okr.unit }}
                  </span>
                </div>
                <div class="fr-col-auto">
                  <span
                    class="bo-badge"
                    :class="
                      Math.round((okr.current / okr.target) * 100) >= 100
                        ? 'bo-badge--green'
                        : 'bo-badge--blue'
                    "
                  >
                    {{ Math.round((okr.current / okr.target) * 100) }}%
                  </span>
                </div>
              </div>
              <div
                style="
                  background-color: var(--border-default-grey);
                  height: 6px;
                  border-radius: 3px;
                  width: 100%;
                  overflow: hidden;
                "
              >
                <div
                  :style="{
                    width: Math.min(Math.round((okr.current / okr.target) * 100), 100) + '%',
                    backgroundColor:
                      Math.round((okr.current / okr.target) * 100) >= 100 ? '#22C55E' : '#000091',
                    height: '100%',
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fr-mb-4w">
      <h3 class="fr-h5" style="display: flex; align-items: center; gap: 0.5rem">
        <span class="fr-icon-user-fill fr-text-title-blue-france" aria-hidden="true"></span>
        Répartition du traitement
      </h3>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div
          v-for="(count, agent) in store.workloadByAssignee"
          :key="agent"
          class="fr-col-12 fr-col-md-4"
        >
          <div
            class="premium-box fr-p-2w"
            style="
              background: white;
              border-top: 4px solid var(--border-active-blue-france);
              text-align: center;
            "
          >
            <p class="fr-text--sm fr-mb-1v" style="color: var(--text-mention-grey)">
              {{ agent }}
            </p>
            <p class="fr-h3 fr-mb-0">{{ count }} {{ count > 1 ? 'dossiers' : 'dossier' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Filters -->
    <div class="bo-filter-bar fr-mt-4w">
      <div class="bo-filter-group">
        <span class="bo-filter-label">Période :</span>
        <select
          v-model="statsFilters.periode"
          class="fr-select"
          style="width: auto; padding-right: 2rem"
        >
          <option value="Période globale (6 derniers mois)">
            Période globale (6 derniers mois)
          </option>
          <option value="Cette semaine">Cette semaine</option>
          <option value="Semaine dernière">Semaine dernière</option>
          <option value="Ce mois">Ce mois</option>
          <option value="Mois dernier">Mois dernier</option>
        </select>
      </div>

      <div class="bo-filter-group">
        <span class="bo-filter-label">Cas réel de dépôt sauvage:</span>
        <select
          v-model="statsFilters.exclureTests"
          class="fr-select"
          style="width: auto; padding-right: 2rem"
        >
          <option value="Oui">Oui</option>
          <option value="Non">Non</option>
        </select>
      </div>

      <div class="bo-filter-group">
        <span class="bo-filter-label">Auteur identifié :</span>
        <select
          v-model="statsFilters.auteurIdentifie"
          class="fr-select"
          style="width: auto; padding-right: 2rem"
        >
          <option value="Tous">Tous</option>
          <option value="Oui uniquement">Oui uniquement</option>
          <option value="Non uniquement">Non uniquement</option>
        </select>
      </div>
    </div>

    <!-- Render interactive stats chart -->
    <StatsChart :data="store.stats.history" title="Activité historique & Performances globales" />

    <!-- Compilation table of stats (matching stats-sample.md weekly tracking) -->
    <div class="fr-grid-row fr-grid-row--middle fr-mt-4w fr-mb-1w">
      <div class="fr-col">
        <h3 class="fr-h5" style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0">
          <span class="fr-icon-table-line fr-text-title-blue-france" aria-hidden="true"></span>
          Suivi Hebdomadaire
        </h3>
        <p class="fr-text--sm fr-mb-0" style="color: var(--text-mention-grey)">
          Données d'activité de l'équipe de déploiement, actualisées toutes les semaines.
        </p>
      </div>
      <div class="fr-col-auto">
        <button class="fr-btn fr-icon-add-circle-line fr-btn--icon-left" @click="openAddSnapshot">
          Saisir une semaine
        </button>
      </div>
    </div>

    <!-- Inline snapshot entry form -->
    <div
      v-if="showSnapshotForm"
      class="premium-box fr-p-3w fr-mb-3w"
      style="background: #f6f6f6; border-left: 4px solid var(--border-active-blue-france)"
    >
      <h4 class="fr-h6 fr-mb-2w">
        {{ editingSnapshotIndex !== -1 ? 'Modifier la semaine' : 'Saisir une nouvelle semaine' }}
      </h4>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-date">Date / Semaine (ex. 07/07)</label>
            <input
              id="snap-date"
              v-model="formSnapshot.date"
              type="text"
              class="fr-input"
              placeholder="JJ/MM"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-procedures">Procédures Lancées</label>
            <input
              id="snap-procedures"
              v-model.number="formSnapshot.procedures"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-col">Collectivités Actives</label>
            <input
              id="snap-col"
              v-model.number="formSnapshot.activeCollectivities"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-fines">Nb Amendes Prononcées</label>
            <input
              id="snap-fines"
              v-model.number="formSnapshot.finesCount"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-amount">Montant Prononcé (€)</label>
            <input
              id="snap-amount"
              v-model.number="formSnapshot.amountFines"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-cleaned">Dépôts Nettoyés</label>
            <input
              id="snap-cleaned"
              v-model.number="formSnapshot.cleanedCount"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-volume">Volume Nettoyé (m³)</label>
            <input
              id="snap-volume"
              v-model.number="formSnapshot.cleanedVolume"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="fr-input-group">
            <label class="fr-label" for="snap-webinars">Webinaires (Partic. cumulés)</label>
            <input
              id="snap-webinars"
              v-model.number="formSnapshot.webinarsCount"
              type="number"
              class="fr-input"
            />
          </div>
        </div>
      </div>
      <div class="fr-mt-2w" style="display: flex; gap: 1rem">
        <button class="fr-btn fr-btn--sm" @click="saveSnapshot">Enregistrer</button>
        <button class="fr-btn fr-btn--sm fr-btn--secondary" @click="showSnapshotForm = false">
          Annuler
        </button>
      </div>
    </div>

    <div class="bo-table-container">
      <table class="bo-table">
        <thead>
          <tr>
            <th>Semaine</th>
            <th>Procédures Admin Lancées (PA)</th>
            <th>Nb Collectivités Actives</th>
            <th>Nb Amendes Prononcées</th>
            <th>Montant Prononcé (€)</th>
            <th>Dépôts Nettoyés</th>
            <th>Webinaires (Participants cumulés)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="snapshot in sortedWeeklySnapshots" :key="snapshot.date">
            <td>
              <strong>{{ snapshot.date }}</strong>
            </td>
            <td>
              {{ snapshot.procedures }}
              <span
                class="fr-text--xs"
                style="color: var(--text-mention-grey); font-weight: 600; margin-left: 0.25rem"
              >
                (soit {{ Math.round((snapshot.procedures / 500) * 100) }}% de l'obj. 500)
              </span>
            </td>
            <td>{{ snapshot.activeCollectivities }}</td>
            <td>{{ snapshot.finesCount }}</td>
            <td>
              <strong
                >{{
                  snapshot.amountFines.toLocaleString('fr-FR', { minimumFractionDigits: 2 })
                }}
                €</strong
              >
            </td>
            <td>{{ snapshot.cleanedCount }} ({{ snapshot.cleanedVolume }}m³)</td>
            <td>{{ snapshot.webinarsCount }}</td>
            <td>
              <div style="display: flex; gap: 0.5rem">
                <button
                  class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-edit-line"
                  style="padding: 0.25rem 0.5rem"
                  title="Modifier"
                  @click="editSnapshot(snapshot)"
                ></button>
                <button
                  class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-delete-line"
                  style="padding: 0.25rem 0.5rem; color: #dc2626"
                  title="Supprimer"
                  @click="deleteSnapshot(snapshot.date)"
                ></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import StatsChart from '@/components/StatsChart.vue'
import { useBackofficeStore } from '@/stores/backoffice'
import { computed, ref } from 'vue'

const store = useBackofficeStore()

// Filters for TAB 4 (Statistics)
const statsFilters = ref({
  periode: 'Période globale (6 derniers mois)',
  exclureTests: 'Oui',
  auteurIdentifie: 'Tous',
})

// Saisie manuelle des Snapshots
const showSnapshotForm = ref(false)
const editingSnapshotIndex = ref(-1)
const formSnapshot = ref({
  date: '',
  procedures: 0,
  activeCollectivities: 0,
  finesCount: 0,
  amountFines: 0,
  cleanedCount: 0,
  cleanedVolume: 0,
  webinarsCount: 0,
})

const openAddSnapshot = () => {
  editingSnapshotIndex.value = -1
  formSnapshot.value = {
    date: '',
    procedures: 0,
    activeCollectivities: 0,
    finesCount: 0,
    amountFines: 0,
    cleanedCount: 0,
    cleanedVolume: 0,
    webinarsCount: 0,
  }
  showSnapshotForm.value = true
}

const editSnapshot = (snapshot: any) => {
  editingSnapshotIndex.value = store.stats.weeklySnapshots.findIndex(
    (s) => s.date === snapshot.date
  )
  formSnapshot.value = { ...snapshot }
  showSnapshotForm.value = true
}

const saveSnapshot = () => {
  if (!formSnapshot.value.date) {
    alert('Veuillez indiquer la date / semaine.')
    return
  }
  store.saveWeeklySnapshot(formSnapshot.value)
  showSnapshotForm.value = false
}

const deleteSnapshot = (date: string) => {
  if (confirm(`Confirmer la suppression du snapshot de la semaine ${date} ?`)) {
    store.deleteWeeklySnapshot(date)
  }
}

// Inline OKR Editing states
const editingOkrKey = ref<string | null>(null)
const editingOkrValue = ref<number>(0)

const startEditOkr = (key: string, currentValue: number) => {
  editingOkrKey.value = key
  editingOkrValue.value = currentValue
}

const saveOkr = (key: string) => {
  store.updateOkrValue(key, editingOkrValue.value)
  editingOkrKey.value = null
}

const sortedWeeklySnapshots = computed(() => {
  return [...store.stats.weeklySnapshots].sort((a, b) => {
    // Basic date parsing "DD/MM" for sorting
    const [dayA, monthA] = a.date.split('/').map(Number)
    const [dayB, monthB] = b.date.split('/').map(Number)
    return monthA * 100 + dayA - (monthB * 100 + dayB)
  })
})

// Live OKR computing
const liveOkrs = computed(() => {
  const base = { ...store.stats.okrs }

  // Overwriting with live calculated values
  base.kr1_1 = {
    ...base.kr1_1,
    current: store.realProcedures.length,
    isLive: true,
  }
  base.kr1_2 = {
    ...base.kr1_2,
    current: store.liveCompletionRate,
    isLive: true,
  }
  base.kr2_2 = {
    ...base.kr2_2,
    current: store.activeCommunesCount,
    isLive: true,
  }

  return base
})
</script>
