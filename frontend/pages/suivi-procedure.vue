<template>
  <div class="fr-container fr-py-6w">
    <Chargement v-if="showLoading" />
    <LoginInvitation v-else-if="!isUserAuthenticated" />
    <div v-else-if="error" class="fr-alert fr-alert--error fr-mb-4w">
      <p>{{ error }}</p>
    </div>
    <div v-else-if="procedureData">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-10 fr-col-offset-md-1">
          <header class="fr-mb-4w">
            <div class="fr-grid-row fr-grid-row--middle fr-mb-3w">
              <div class="fr-col-auto fr-mr-3w">
                <h1 class="fr-h1 fr-mb-0">Procédure #{{ procedureData.id }}</h1>
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

            <Metadata :procedure="procedureData" class="fr-mb-3w" />

            <div v-if="procedureData" class="fr-mt-2w">
              <DsfrButton secondary @click="router.push(modifyUrl)">
                <span class="fr-icon-edit-line fr-mr-1w" aria-hidden="true"></span>
                Modifier la constatation
              </DsfrButton>
            </div>
          </header>

          <InfosComplementaires v-if="hasProcedure" :suivi="suiviProcedure" />

          <StepperProcedure :steps="steps" v-model:currentStep="activeStep">
            <template #step-0>
              <Constatation :auteur-identifie="auteurIdentifie" />
            </template>
            <template #step-1>
              <AucuneProcedure v-if="!hasProcedure" :modify-url="modifyUrl" />
              <Documents
                v-else
                :suivi="suiviProcedure"
                :has-procedure="hasProcedure"
                :auteur-identifie="auteurIdentifie"
                :doc-constat-url="getDocConstatUrl(procedureData.id)"
                :lettre-info-url="getLettreInfoUrl(procedureData.id)"
              />
            </template>
            <template v-if="hasProcedure" #step-2>
              <Notification
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :lettre-info-url="getLettreInfoUrl(procedureData.id)"
                @next-step="activeStep = 3"
              />
              <Identification v-else :suivi="suiviProcedure" :auteur-identifie="auteurIdentifie" />
            </template>
            <template v-if="hasProcedure" #step-3>
              <SuiviDecision
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                @back-to-notification="activeStep = 2"
              />
              <MettreAjourDossier
                v-else-if="suiviProcedure.identification_reussie === true"
                :modify-url="modifyUrl"
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
import { useRoute, useRouter } from 'vue-router'

import StepperProcedure from '../components/StepperProcedure.vue'
import Chargement from '../components/procedures/Chargement.vue'
import Metadata from '../components/procedures/Metadata.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
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
import { API_URLS, fetchResource, getUserInfo } from '../services/api'
import { getDocConstatUrl, getLettreInfoUrl } from '../services/urls'
import { useSuiviStore } from '../stores/suivi-procedure'
import { debounce } from '../utils/debounce'

const route = useRoute()
const router = useRouter()
const suiviStore = useSuiviStore()

// The identifier in the URL corresponds to the underlying Constatation ID.
// Each follow-up procedure (SuiviProcedure) is linked 1:1 to its Constatation.
const constatationId = computed(
  () => (route.params.constatation_id as string) || (route.query.constatation_id as string)
)
const suiviProcedure = computed(() => suiviStore.getOrCreateSuivi(constatationId.value))
const showLoading = ref(true)
const error = ref<string | null>(null)
const procedureData = ref<any>(null)
const isUserAuthenticated = ref(false)
const activeStep = computed({
  get: () => suiviProcedure.value.etape_en_cours,
  set: (val) => (suiviProcedure.value.etape_en_cours = val),
})

const hasProcedure = computed(() => procedureData.value?.created !== false)
const auteurIdentifie = computed(() => procedureData.value?.auteur_identifie ?? false)

const modifyUrl = computed(() => `/constatation/${constatationId.value}`)

// Auto-save logic with debounce
const debouncedSave = debounce(() => {
  if (constatationId.value && procedureData.value?.id) {
    suiviStore.saveSuivi(constatationId.value, procedureData.value.id)
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
  suiviStore.isStepCompleted(constatationId.value, index, {
    auteurIdentifie: auteurIdentifie.value,
    currentStep: activeStep.value,
  })

const steps = computed(() => {
  if (!constatationId.value) return []

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
  const currentConstatationId =
    (route.params.constatation_id as string) || (route.query.constatation_id as string)

  if (!currentConstatationId) {
    error.value = 'Identifiant de procédure manquant.'
    showLoading.value = false
    return
  }

  try {
    const user = await getUserInfo()
    isUserAuthenticated.value = user.is_authenticated

    if (!isUserAuthenticated.value) {
      showLoading.value = false
      return
    }

    // Fetch constatation data directly
    const procedureRes = await fetchResource(`${API_URLS.constatations}${currentConstatationId}/`)
    procedureData.value = procedureRes

    // Then fetch procedure tracking data using the internal ID
    await suiviStore.fetchSuivi(currentConstatationId, procedureRes.id)
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
