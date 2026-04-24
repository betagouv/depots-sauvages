<template>
  <div class="fr-container fr-py-6w">
    <ChargementDossier v-if="showLoading" />
    <div v-else-if="error" class="fr-alert fr-alert--error fr-mb-4w">
      <p>{{ error }}</p>
    </div>
    <div v-else-if="dossierData">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-10 fr-col-offset-md-1">
          <header class="fr-mb-4w">
            <div class="fr-grid-row fr-grid-row--middle fr-mb-3w">
              <div class="fr-col-auto fr-mr-3w">
                <h1 class="fr-h1 fr-mb-0">Procédure #{{ dossierData.dn_numero_dossier }}</h1>
              </div>
              <div class="fr-col-auto" v-if="hasProcedure">
                <DsfrBadge
                  :type="auteurIdentifie ? 'success' : 'info'"
                  :label="auteurIdentifie ? 'Auteur identifié' : 'Auteur non identifié'"
                  class="fr-badge--no-icon"
                />
              </div>
            </div>

            <p class="fr-text--lead fr-mb-4w">Suivi des actions que vous devez réaliser.</p>

            <DossierMetadata :dossier="dossierData" class="fr-mb-3w" />

            <DsfrButton
              label="Modifier le dossier de constatation sur Démarche numérique"
              class="fr-btn--secondary"
              :icon="{ name: 'ri-external-link-line', class: 'fr-mr-1w' }"
              icon-right
              @click="openExternalLink(getDnModifyUrl(dossierData.dn_numero_dossier))"
            />
          </header>

          <InfosComplementaires v-if="hasProcedure && auteurIdentifie" :suivi="suiviProcedure" />

          <StepperProcedure :steps="steps" v-model:currentStep="activeStep">
            <template #step-0>
              <Constatation :auteur-identifie="auteurIdentifie" />
            </template>
            <template #step-1>
              <AucuneProcedure
                v-if="!hasProcedure"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
              <Documents
                v-else
                :suivi="suiviProcedure"
                :dossier-data="dossierData"
                :has-procedure="hasProcedure"
                :auteur-identifie="auteurIdentifie"
                :doc-constat-url="getDnDocConstatUrl(dossierData.id)"
                :lettre-info-url="getDnLettreInfoUrl(dossierData.id)"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
            </template>
            <template v-if="hasProcedure" #step-2>
              <Notification
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :lettre-info-url="getDnLettreInfoUrl(dossierData.id)"
                @next-step="activeStep = 3"
              />
              <Identification
                v-else
                :suivi="suiviProcedure"
                :auteur-identifie="auteurIdentifie"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
            </template>
            <template v-if="hasProcedure" #step-3>
              <SuiviDecision
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
                @back-to-notification="activeStep = 2"
              />
              <MettreAjourDossier
                v-else-if="suiviProcedure.identification_reussie === true"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
              <ClotureSansAuteur
                v-else-if="suiviProcedure.identification_reussie === false"
                :suivi="suiviProcedure"
              />
            </template>
            <template v-if="hasProcedure" #step-4>
              <SuiviActions
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
                @back-to-decision="activeStep = 3"
                @go-to-cloture="activeStep = 5"
              />
            </template>
            <template v-if="hasProcedure" #step-5>
              <Cloture
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                @back-to-decision="activeStep = 3"
              />
            </template>
          </StepperProcedure>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import StepperProcedure from '../components/StepperProcedure.vue'
import ChargementDossier from '../components/dossiers/ChargementDossier.vue'
import DossierMetadata from '../components/dossiers/DossierMetadata.vue'
import AucuneProcedure from '../components/steps/AucuneProcedure.vue'
import Cloture from '../components/steps/Cloture.vue'
import ClotureSansAuteur from '../components/steps/ClotureSansAuteur.vue'
import Constatation from '../components/steps/Constatation.vue'
import Documents from '../components/steps/Documents.vue'
import Identification from '../components/steps/Identification.vue'
import InfosComplementaires from '../components/steps/InfosComplementaires.vue'
import MettreAjourDossier from '../components/steps/MettreAjourDossier.vue'
import Notification from '../components/steps/Notification.vue'
import SuiviActions from '../components/steps/SuiviActions.vue'
import SuiviDecision from '../components/steps/SuiviDecision.vue'
import { API_URLS, createResource } from '../services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '../services/urls'
import { useSuiviStore } from '../stores/suivi-procedure'
import { openExternalLink } from '../utils/browser'
import { debounce } from '../utils/debounce'

const route = useRoute()
const suiviStore = useSuiviStore()

const dossierId = computed(
  () => (route.params.dossier_id as string) || (route.query.dossier_id as string)
)
const suiviProcedure = computed(() => suiviStore.getOrCreateSuivi(dossierId.value))
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)
const activeStep = computed({
  get: () => suiviProcedure.value.etape_en_cours,
  set: (val) => (suiviProcedure.value.etape_en_cours = val),
})

const hasProcedure = computed(() => dossierData.value?.created !== false)
const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)

const signalementId = computed(() => dossierData.value?.id)

// Auto-save logic with debounce
const debouncedSave = debounce(() => {
  if (dossierId.value && signalementId.value) {
    suiviStore.saveSuivi(dossierId.value, signalementId.value)
  }
}, 1000)

watch(
  () => suiviProcedure.value,
  () => {
    debouncedSave()
  },
  { deep: true }
)

const getStepStatus = (index: number) =>
  suiviStore.isStepCompleted(dossierId.value, index, {
    auteurIdentifie: auteurIdentifie.value,
    currentStep: activeStep.value,
  })

const steps = computed(() => {
  if (!dossierId.value) return []

  if (!hasProcedure.value) {
    return [
      { title: 'Constatation', completed: getStepStatus(0) },
      { title: 'Procédure à mettre à jour', completed: false },
    ]
  }

  if (!auteurIdentifie.value) {
    const baseSteps = [
      { title: 'Constatation', completed: getStepStatus(0) },
      { title: 'Pièces de procédure', completed: getStepStatus(1) },
      { title: "Identifier l'auteur", completed: getStepStatus(2) },
    ]

    if (suiviProcedure.value.identification_reussie === true) {
      baseSteps.push({ title: 'Mettre à jour le dossier', completed: false })
    } else if (suiviProcedure.value.identification_reussie === false) {
      baseSteps.push({ title: 'Clôture de la procédure', completed: getStepStatus(5) })
    }

    return baseSteps
  }

  const actionStepTitle =
    suiviProcedure.value.decision_poursuite === 'sanction'
      ? "Sanctionner l'auteur"
      : suiviProcedure.value.decision_poursuite === 'abandon'
        ? 'Abandonner les poursuites'
        : 'Action de poursuite'

  return [
    { title: 'Constatation', completed: getStepStatus(0) },
    { title: 'Signer les pièces de procédure', completed: getStepStatus(1) },
    { title: "Notifier l'auteur présumé", completed: getStepStatus(2) },
    { title: 'Décider des poursuites', completed: getStepStatus(3) },
    { title: actionStepTitle, completed: getStepStatus(4) },
    { title: 'Clôture de la procédure', completed: getStepStatus(5) },
  ]
})

onMounted(async () => {
  const dossierId = (route.params.dossier_id as string) || (route.query.dossier_id as string)

  if (!dossierId) {
    // For demo/dev purposes if no ID is provided, we might want to mock or show error
    // In a real app, we should probably redirect or show a robust error
    error.value = 'Identifiant de dossier manquant.'
    showLoading.value = false
    return
  }

  try {
    // Fetch dossier data first (it creates the signalement if needed)
    const dossierRes = await createResource(API_URLS.processDossier, { dossier_id: dossierId })
    dossierData.value = dossierRes

    // Then fetch procedure tracking data using the internal ID
    await suiviStore.fetchSuivi(dossierId, dossierRes.id)
  } catch (err: any) {
    error.value = err.error || 'Une erreur est survenue lors de la récupération du dossier.'
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
