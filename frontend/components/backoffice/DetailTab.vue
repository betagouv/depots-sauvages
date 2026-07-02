<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div v-if="!selectedProcedure" class="fr-text-center fr-py-5w">
      <span class="fr-icon-arrow-left-line fr-mr-1w" aria-hidden="true"></span>
      Veuillez sélectionner une procédure dans le tableau de bord ou la liste pour afficher ses
      détails.
    </div>

    <div v-else>
      <!-- Stepper/Timeline progress bar -->
      <div class="bo-stepper">
        <div
          v-for="step in 5"
          :key="step"
          class="bo-step"
          :class="{
            'bo-step--completed': selectedProcedure.suivi_procedure.etape_en_cours > step,
            'bo-step--active': selectedProcedure.suivi_procedure.etape_en_cours === step,
          }"
        >
          <div class="bo-step-num">{{ step }}</div>
          <div class="bo-step-lbl">{{ getStepLabel(step) }}</div>
        </div>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <!-- Left Info Panel -->
        <div class="fr-col-12 fr-col-md-7">
          <!-- Constatation Overview Card -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white">
            <h3
              class="fr-h5"
              style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem"
            >
              Constatation
            </h3>
            <div class="fr-grid-row fr-grid-row--gutters">
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  Commune
                </p>
                <p class="fr-text--md">
                  <strong>{{ selectedProcedure.commune }}</strong>
                </p>
              </div>
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  Agent Constatant
                </p>
                <p class="fr-text--md">{{ selectedProcedure.agent }}</p>
              </div>
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  Rôle
                </p>
                <p class="fr-text--md">{{ selectedProcedure.constatant_role }}</p>
              </div>
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  Date du Constat
                </p>
                <p class="fr-text--md">{{ formatDate(selectedProcedure.date_constat) }}</p>
              </div>
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  N° Procédure
                </p>
                <p class="fr-text--md">
                  <code>{{ selectedProcedure.id }}</code>
                </p>
              </div>
              <div class="fr-col-6">
                <p
                  class="fr-text--xs fr-mb-1v"
                  style="color: var(--text-mention-grey); text-transform: uppercase"
                >
                  Type de Terrain
                </p>
                <p class="fr-text--md">{{ selectedProcedure.nature_terrain.join(', ') }}</p>
              </div>
            </div>
          </div>

          <!-- Follow up checklists -->
          <div class="premium-box fr-p-3w" style="background: white">
            <h3
              class="fr-h5"
              style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem"
            >
              Éléments requis de procédure (Modèles réels)
            </h3>
            <div class="premium-choices-list">
              <div
                class="premium-action-item fr-p-1w"
                style="cursor: pointer"
                @click="store.toggleSuiviField(selectedProcedure.id, 'preuves')"
              >
                <span
                  class="fr-mr-2w"
                  :class="
                    selectedProcedure.suivi_procedure.preuves_fournies
                      ? 'fr-icon-checkbox-circle-fill'
                      : 'fr-icon-checkbox-blank-line'
                  "
                  :style="{
                    color: selectedProcedure.suivi_procedure.preuves_fournies
                      ? '#22C55E'
                      : '#9CA3AF',
                  }"
                ></span>
                <span class="action-label"
                  >Éléments de preuve joints au dossier (`preuves_fournies`)</span
                >
              </div>

              <div
                class="premium-action-item fr-p-1w"
                style="cursor: pointer"
                @click="store.toggleSuiviField(selectedProcedure.id, 'rapportSigne')"
              >
                <span
                  class="fr-mr-2w"
                  :class="
                    selectedProcedure.suivi_procedure.constatation_signee
                      ? 'fr-icon-checkbox-circle-fill'
                      : 'fr-icon-checkbox-blank-line'
                  "
                  :style="{
                    color: selectedProcedure.suivi_procedure.constatation_signee
                      ? '#22C55E'
                      : '#9CA3AF',
                  }"
                ></span>
                <span class="action-label"
                  >Rapport de constatation signé (`constatation_signee`)</span
                >
              </div>

              <div
                class="premium-action-item fr-p-1w"
                style="cursor: pointer"
                @click="store.toggleSuiviField(selectedProcedure.id, 'lettreSignee')"
              >
                <span
                  class="fr-mr-2w"
                  :class="
                    selectedProcedure.suivi_procedure.lettre_signe
                      ? 'fr-icon-checkbox-circle-fill'
                      : 'fr-icon-checkbox-blank-line'
                  "
                  :style="{
                    color: selectedProcedure.suivi_procedure.lettre_signe ? '#22C55E' : '#9CA3AF',
                  }"
                ></span>
                <span class="action-label">Lettre d'information signée (`lettre_signe`)</span>
              </div>

              <div
                class="premium-action-item fr-p-1w"
                style="cursor: pointer"
                @click="store.toggleSuiviField(selectedProcedure.id, 'auteurIdentifie')"
              >
                <span
                  class="fr-icon-user-search-line fr-mr-2w"
                  style="color: var(--border-active-blue-france)"
                ></span>
                <span class="action-label">
                  Identification de l'auteur (`identification_reussie`) :
                  <strong>{{
                    getAuteurIdentifieText(selectedProcedure.suivi_procedure.identification_reussie)
                  }}</strong>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Followup Panel -->
        <div class="fr-col-12 fr-col-md-5">
          <div
            class="premium-box fr-p-3w"
            style="background: white; border-left: 5px solid var(--border-active-blue-france)"
          >
            <h3
              class="fr-h5"
              style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem"
            >
              Pilotage déploiement
            </h3>

            <!-- Officer Assignee -->
            <div class="fr-select-group fr-mb-3w">
              <label class="fr-label" for="assignee-select">Chargé de déploiement assigné</label>
              <select
                id="assignee-select"
                class="fr-select"
                :value="selectedProcedure.suivi_procedure.charge_deploiement"
                @change="
                  store.assignCharge(
                    selectedProcedure.id,
                    ($event.target as HTMLSelectElement).value
                  )
                "
              >
                <option v-for="name in store.assignees" :key="name" :value="name">
                  {{ name }}
                </option>
              </select>
              <p
                v-if="selectedProcedure.suivi_procedure.date_assigned"
                class="fr-text--xs fr-mt-1w"
                style="color: var(--text-mention-grey)"
              >
                Assigné le {{ formatDate(selectedProcedure.suivi_procedure.date_assigned) }}
              </p>
            </div>

            <!-- Internal Notes -->
            <div class="fr-input-group">
              <label class="fr-label" for="internal-notes"
                >Notes internes & Suivi (`observations_internes`)</label
              >
              <textarea
                id="internal-notes"
                class="fr-input"
                placeholder="Écrivez vos notes de suivi ici (relance, appels, blocages...)"
                style="min-height: 120px"
                :value="selectedProcedure.suivi_procedure.observations_internes"
                @input="
                  store.updateNotes(
                    selectedProcedure.id,
                    ($event.target as HTMLTextAreaElement).value
                  )
                "
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { formatDate, getAuteurIdentifieText, getStepLabel } from '@/utils/backoffice'
import { computed } from 'vue'

const store = useBackofficeStore()

const props = defineProps<{
  selectedProcedureId: number | null
}>()

const selectedProcedure = computed(() => {
  if (!props.selectedProcedureId) return null
  return store.getProcedureById(props.selectedProcedureId)
})
</script>
