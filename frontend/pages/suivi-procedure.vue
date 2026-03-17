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
            <div class="fr-mb-3w">
              <h1 class="fr-h1 fr-mb-2w">Ma procédure de dépôt sauvage</h1>
            </div>

            <p class="fr-text--lead fr-mb-1w">Dossier #{{ dossierData.dn_numero_dossier }}</p>

            <div
              v-if="dossierData.date_creation"
              class="fr-text--xs fr-mb-2w fr-text-mention--grey"
            >
              <span class="fr-icon-calendar-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
              Créé le {{ formatDate(dossierData.date_creation) }}
              <span
                v-if="
                  shouldShowModificationDate(
                    dossierData.date_creation,
                    dossierData.date_modification
                  )
                "
              >
                &middot; Modifié le {{ formatDate(dossierData.date_modification) }}
              </span>
            </div>
            <div>
              <DsfrBadge
                :type="auteurIdentifie ? 'success' : 'info'"
                :label="auteurIdentifie ? 'Auteur identifié' : 'Auteur non identifié'"
                class="fr-badge--no-icon fr-mb-3w"
              />
            </div>
            <DsfrButton
              label="Modifier sur Démarche Numérique"
              class="fr-btn--secondary"
              :icon="{ name: 'ri-external-link-line', class: 'fr-mr-1w' }"
              icon-right
              @click="openExternalLink(getDnModifyUrl(dossierData.dn_numero_dossier))"
            />
          </header>

          <StepperProcedure :steps="steps" v-model:currentStep="activeStep">
            <template #step-0>
              <Constatation :auteur-identifie="auteurIdentifie" />
            </template>
            <template #step-1>
              <Documents
                :dossier-data="dossierData"
                :has-procedure="hasProcedure"
                :auteur-identifie="auteurIdentifie"
                :doc-constat-url="getDnDocConstatUrl(dossierData.id)"
                :lettre-info-url="getDnLettreInfoUrl(dossierData.id)"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
            </template>
            <template #step-2>
              <Notification v-if="auteurIdentifie" />
              <Judiciaire v-else :auteur-identifie="auteurIdentifie" />
            </template>
            <template #step-3>
              <SuiviSanction v-if="auteurIdentifie" />
            </template>
            <template #step-4>
              <Cloture v-if="auteurIdentifie" />
            </template>
          </StepperProcedure>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate, shouldShowModificationDate } from '@/utils/date'
import { DsfrBadge, DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import StepperProcedure from '../components/StepperProcedure.vue'
import ChargementDossier from '../components/dn/ChargementDossier.vue'
import Cloture from '../components/steps/Cloture.vue'
import Constatation from '../components/steps/Constatation.vue'
import Documents from '../components/steps/Documents.vue'
import Judiciaire from '../components/steps/Judiciaire.vue'
import Notification from '../components/steps/Notification.vue'
import SuiviSanction from '../components/steps/SuiviSanction.vue'

import { API_URLS, createResource } from '@/services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '@/services/urls'

const route = useRoute()
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)
const activeStep = ref(1)

const hasProcedure = computed(() => dossierData.value?.created !== false)
const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)

const steps = computed(() => {
  if (!auteurIdentifie.value) {
    return [
      {
        title: 'Constatation',
        description: 'Constater le dépôt et débuter de la procédure.',
      },
      {
        title: 'Documents de procédure',
        description:
          'Remplir le dossier, collecter les preuves et récupérer le rapport de constatation.',
      },
      {
        title: 'Procédure Judiciaire',
        description: 'Procédure judiciaire pour donner suite au constat du dépôt.',
      },
    ]
  }

  return [
    {
      title: 'Constatation',
      description: 'Constater le dépôt et débuter de la procédure.',
    },
    {
      title: 'Documents de procédure',
      description: 'Remplir le dossier, collecter les preuves et récupérer les documents types.',
    },
    {
      title: "Notifier l'auteur présumé",
      description: "Envoyer la notification officielle à l'auteur présumé.",
    },
    {
      title: "Suivi de l'amende et remise en état",
      description: 'Gérez les suites de la mise en demeure et déterminez les sanctions.',
    },
    {
      title: 'Clôture',
      description: 'Finalisation et archivage du dossier après information du Trésor Public.',
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

const openExternalLink = (url: string) => {
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
