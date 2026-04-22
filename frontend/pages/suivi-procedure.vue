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
                :auteur-identifie="auteurIdentifie"
                :modify-url="getDnModifyUrl(dossierData.id)"
              />
            </template>
            <template v-if="hasProcedure" #step-3>
              <SuiviDecision
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
                @back-to-notification="activeStep = 2"
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
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import StepperProcedure from '../components/StepperProcedure.vue'
import ChargementDossier from '../components/dossiers/ChargementDossier.vue'
import DossierMetadata from '../components/dossiers/DossierMetadata.vue'
import AucuneProcedure from '../components/steps/AucuneProcedure.vue'
import Cloture from '../components/steps/Cloture.vue'
import Constatation from '../components/steps/Constatation.vue'
import Documents from '../components/steps/Documents.vue'
import Identification from '../components/steps/Identification.vue'
import InfosComplementaires from '../components/steps/InfosComplementaires.vue'
import Notification from '../components/steps/Notification.vue'
import SuiviActions from '../components/steps/SuiviActions.vue'
import SuiviDecision from '../components/steps/SuiviDecision.vue'
import { API_URLS, createResource } from '../services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '../services/urls'
import { useSuiviStore } from '../stores/suivi-procedure'
import { openExternalLink } from '../utils/browser'

const route = useRoute()
const suiviStore = useSuiviStore()

const dossierId = computed(
  () => (route.params.dossier_id as string) || (route.query.dossier_id as string)
)
const suiviProcedure = computed(() => suiviStore.getOrCreateSuivi(dossierId.value))
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)
const activeStep = ref(1)

const hasProcedure = computed(() => dossierData.value?.created !== false)
const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)

const steps = computed(() => {
  if (!hasProcedure.value) {
    return [
      {
        title: 'Constatation',
        completed: suiviStore.isStepCompleted(dossierId.value, 0, {
          auteurIdentifie: auteurIdentifie.value,
          currentStep: activeStep.value,
        }),
      },
      {
        title: 'Procédure à mettre à jour',
        completed: false,
      },
    ]
  }

  if (!auteurIdentifie.value) {
    return [
      {
        title: 'Constatation',
        completed: suiviStore.isStepCompleted(dossierId.value, 0, {
          auteurIdentifie: auteurIdentifie.value,
          currentStep: activeStep.value,
        }),
      },
      {
        title: 'Pièces de procédure',
        completed: suiviStore.isStepCompleted(dossierId.value, 1, {
          auteurIdentifie: auteurIdentifie.value,
          currentStep: activeStep.value,
        }),
      },
      {
        title: "Identification de l'auteur",
        completed: false,
      },
    ]
  }

  return [
    {
      title: 'Constatation',
      completed: suiviStore.isStepCompleted(dossierId.value, 0, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
    {
      title: 'Compléter les pièces de procédure',
      completed: suiviStore.isStepCompleted(dossierId.value, 1, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
    {
      title: "Notifier l'auteur présumé :",
      completed: suiviStore.isStepCompleted(dossierId.value, 2, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
    {
      title: 'Décider des poursuites :',
      completed: suiviStore.isStepCompleted(dossierId.value, 3, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
    {
      title:
        suiviProcedure.value.decision_poursuite === 'sanction'
          ? "Sanctionner l'auteur"
          : suiviProcedure.value.decision_poursuite === 'abandon'
            ? 'Abandonner les poursuites'
            : 'Action de poursuite',
      completed: suiviStore.isStepCompleted(dossierId.value, 4, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
    {
      title: 'Clôture de la procédure',
      completed: suiviStore.isStepCompleted(dossierId.value, 5, {
        auteurIdentifie: auteurIdentifie.value,
        currentStep: activeStep.value,
      }),
    },
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
    dossierData.value = await createResource(API_URLS.processDossier, {
      dossier_id: dossierId,
    })
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
