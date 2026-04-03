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

            <DossierMetadata :dossier="dossierData" />
            <div v-if="hasProcedure">
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

          <InfosComplementaires v-if="hasProcedure && auteurIdentifie" :suivi="suiviProcedure" />

          <StepperProcedure :steps="steps" v-model:currentStep="activeStep">
            <template #step-0>
              <Constatation :auteur-identifie="auteurIdentifie" />
            </template>
            <template #step-1>
              <AucuneProcedure v-if="!hasProcedure" :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)" />
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
              <Notification v-if="auteurIdentifie" :suivi="suiviProcedure" />
              <Identification
                v-else
                :auteur-identifie="auteurIdentifie"
                :modify-url="getDnModifyUrl(dossierData.id)"
              />
            </template>
            <template v-if="hasProcedure" #step-3>
              <SuiviSanction
                v-if="auteurIdentifie"
                :suivi="suiviProcedure"
                :modify-url="getDnModifyUrl(dossierData.id)"
              />
            </template>
            <template v-if="hasProcedure" #step-4>
              <Cloture v-if="auteurIdentifie" :suivi="suiviProcedure" />
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
import DossierMetadata from '../components/dossiers/DossierMetadata.vue'
import ChargementDossier from '../components/dossiers/ChargementDossier.vue'
import Cloture from '../components/steps/Cloture.vue'
import Constatation from '../components/steps/Constatation.vue'
import Documents from '../components/steps/Documents.vue'
import Identification from '../components/steps/Identification.vue'
import AucuneProcedure from '../components/steps/AucuneProcedure.vue'
import Notification from '../components/steps/Notification.vue'
import SuiviSanction from '../components/steps/SuiviSanction.vue'
import InfosComplementaires from '../components/steps/InfosComplementaires.vue'
import { API_URLS, createResource } from '../services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '../services/urls'
import { openExternalLink } from '../utils/browser'
import { useSuiviStore } from '../stores/suivi-procedure'

const route = useRoute()
const suiviStore = useSuiviStore()

const dossierId = computed(() => (route.params.dossier_id as string) || (route.query.dossier_id as string))
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
        description: 'Constater le dépôt et remplir le formulaire.',
      },
      {
        title: 'Procédure à mettre à jour',
        description: 'Mettre à jour la procédure sur Démarches Numériques.',
      },
    ]
  }

  if (!auteurIdentifie.value) {
    return [
      {
        title: 'Constatation',
        description: 'Constater le dépôt et remplir le formulaire.',
      },
      {
        title: 'Pièces de procédure',
        description: 'Télécharger et compléter le rapport de constatation.',
      },
      {
        title: "Identification de l'auteur",
        description: "Identifier l'auteur des faits ou porter plainte.",
      },
    ]
  }

  return [
    {
      title: 'Constatation',
      description: 'Constater le dépôt et remplir le formulaire.',
    },
    {
      title: 'Pièces de procédure',
      description: 'Télécharger et compléter les pièces de procédure.',
    },
    {
      title: "Notifier l'auteur présumé",
      description: "Envoyer la lettre d'information à l'auteur présumé.",
    },
    {
      title: "Poursuites éventuelles de l'auteur présumé.",
      description: 'Déterminez les suites à donner à la procédure.',
    },
    {
      title: 'Clôture de la procédure',
      description: 'Finaliser et archiver la procédure.',
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
