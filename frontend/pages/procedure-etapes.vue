<template>
  <div class="fr-container fr-py-6w">
    <DnLoading v-if="showLoading" />
    <div v-else-if="error" class="fr-alert fr-alert--error fr-mb-4w">
      <p>{{ error }}</p>
    </div>
    <div v-else-if="dossierData">
      <nav class="fr-breadcrumb fr-mb-4w" aria-label="vous êtes ici :">
        <ol class="fr-breadcrumb__list">
          <li>
            <router-link to="/mes-dossiers" class="fr-breadcrumb__link">Mes procédures</router-link>
          </li>
          <li>
            <a class="fr-breadcrumb__link" aria-current="page">Suivi de la procédure</a>
          </li>
        </ol>
      </nav>

      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-10 fr-col-offset-md-1">
          <header class="fr-mb-6w">
            <h1 class="fr-h1 fr-mb-1w">Ma procédure de dépôt sauvage</h1>
            <div class="fr-display-flex fr-flex-between fr-flex-center fr-flex-wrap">
              <p class="fr-text--lead fr-mb-0">Dossier #{{ dossierData.dn_numero_dossier }}</p>
              <DsfrBadge
                :type="auteurIdentifie ? 'success' : 'warning'"
                :label="auteurIdentifie ? 'Auteur identifié' : 'Auteur non identifié'"
              />
            </div>
          </header>

          <ProceduralStepper :steps="steps" v-model:currentStep="activeStep">
            <template #step-0>
              <StepDocuments
                :dossier-data="dossierData"
                :has-procedure="hasProcedure"
                :auteur-identifie="auteurIdentifie"
                :doc-constat-url="getDnDocConstatUrl(dossierData.id)"
                :lettre-info-url="getDnLettreInfoUrl(dossierData.id)"
                :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
              />
            </template>
            <template #step-1>
              <StepConstatation />
            </template>
            <template #step-2>
              <StepNotification />
            </template>
            <template #step-3>
              <StepSuiviSanction />
            </template>
            <template #step-4>
              <StepCloture />
            </template>
            <template #step-5>
              <StepJudiciaire />
            </template>
          </ProceduralStepper>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrBadge } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import ProceduralStepper from '@/components/ProceduralStepper.vue'
import DnLoading from '@/components/dn/DnLoading.vue'
import StepCloture from '@/components/steps/StepCloture.vue'
import StepConstatation from '@/components/steps/StepConstatation.vue'
import StepDocuments from '@/components/steps/StepDocuments.vue'
import StepJudiciaire from '@/components/steps/StepJudiciaire.vue'
import StepNotification from '@/components/steps/StepNotification.vue'
import StepSuiviSanction from '@/components/steps/StepSuiviSanction.vue'

import { API_URLS, createResource } from '@/services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '@/services/urls'

const route = useRoute()
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)
const activeStep = ref(0)

const hasProcedure = computed(() => dossierData.value?.created !== false)
const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)

const steps = [
  {
    title: 'Documents & État Civil',
    description: "Récupération des documents types et vérification de l'auteur.",
  },
  {
    title: 'Constatation & Saisie',
    description: 'Remplir le dossier et collecter les preuves.',
  },
  {
    title: 'Notification',
    description: 'Envoi du courrier recommandé au responsable.',
  },
  {
    title: 'Suivi & Sanction',
    description: 'Remise en état et amende administrative.',
  },
  {
    title: 'Suivi & Clôture',
    description: 'Recouvrement, archivage et clôture.',
  },
  {
    title: 'Procédure Judiciaire',
    description: 'Dépôt de plainte (optionnelle).',
    optional: true,
  },
]

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
