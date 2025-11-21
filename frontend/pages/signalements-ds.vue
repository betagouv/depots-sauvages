<template>
  <div>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">Télécharger vos documents</h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Téléchargez en un clic votre rapport de constatation et la lettre d'information
              associée à votre dossier.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showLoading" class="fr-container fr-pb-4w">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
          <div class="loading-section fr-p-4w fr-text--center">
            <VIcon name="ri-loader-4-line" :scale="3" animation="spin" class="fr-mb-2w" />
            <p class="fr-text--lg fr-mb-0">Préparation de vos documents en cours...</p>
            <p class="fr-text--sm fr-text-mention--grey">Veuillez patienter quelques instants.</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="fr-container fr-pb-4w">
      <div v-if="error" class="fr-alert fr-alert--error fr-mb-4w">
        <p class="fr-alert__title">Erreur</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="dossierData" class="fr-mb-4w">
        <div class="fr-card fr-mb-4w">
          <div class="fr-card__body">
            <h2 class="fr-card__title">Informations du dossier</h2>
            <div class="fr-mt-2w">
              <p><strong>Numéro de dossier:</strong> {{ dossierData.number }}</p>
              <p v-if="dossierData.dateDepot">
                <strong>Date de dépôt:</strong> {{ formatDate(dossierData.dateDepot) }}
              </p>
              <p v-if="dossierData.dateDerniereModification">
                <strong>Dernière modification:</strong>
                {{ formatDate(dossierData.dateDerniereModification) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Lettre d'information"
            description="Courrier type rappelant les faits constatés, les obligations du détenteur des déchets et le délai de réponse prévu par la procédure."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => {},
                disabled: isLoading,
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Rapport de constatation"
            description="Pièce officielle résumant les observations de terrain et les préjudices causés par le dépôt sauvage."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => {},
                disabled: isLoading,
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { API_URLS, createResource } from '@/services/api'
import { DsfrCard } from '@gouvminint/vue-dsfr'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showLoading = ref(true)
const isLoading = ref(false)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(async () => {
  const dossierId = (route.params.dossier_id as string) || (route.query.dossier_id as string)
  if (!dossierId) {
    error.value = 'dossier_id is required in the URL'
    showLoading.value = false
    return
  }
  isLoading.value = true
  error.value = null
  try {
    dossierData.value = await createResource(API_URLS.processDossier, {
      dossier_id: dossierId,
    })
  } catch (err: any) {
    error.value = err.error || 'An error occurred while processing the dossier'
  } finally {
    isLoading.value = false
    showLoading.value = false
  }
})
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}

.loading-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
}
</style>
