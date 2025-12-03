<template>
  <div>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              <template v-if="dossierData?.auteur_identifie">Téléchargez vos documents</template>
              <template v-else>Téléchargez votre document</template>
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              <template v-if="dossierData?.auteur_identifie">
                Téléchargez le rapport de constatation et la lettre d'information associée au
                signalement de dépôt sauvage.
              </template>
              <template v-else>
                Téléchargez le rapport de constatation associé au signalement de dépôt sauvage.
              </template>
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

      <div v-else-if="dossierData" class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <div class="fr-card fr-card--lg">
            <div class="fr-card__body">
              <h2 class="fr-card__title">Informations du dossier</h2>
              <div class="fr-card__desc">
                <p><strong>Numéro de dossier:</strong> {{ dossierData.ds_numero_dossier }}</p>
                <p v-if="dossierData.ds_date_depot">
                  <strong>Date de dépôt:</strong> {{ formatDate(dossierData.ds_date_depot) }}
                </p>
                <p v-if="dossierData.ds_date_modification">
                  <strong>Dernière modification:</strong>
                  {{ formatDate(dossierData.ds_date_modification) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="dossierData.ds_numero_dossier" class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Modifier votre dossier"
            description="Vous pouvez consulter ou modifier votre dossier sur le site Démarches Simplifiées."
            :buttons="[
              {
                label: 'Consulter ou modifier',
                icon: { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                secondary: true,
                onClick: () => openDocument(getDsModifyUrl(dossierData.ds_numero_dossier)),
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-if="dossierData?.auteur_identifie" class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Lettre d'information"
            description="Courrier rappelant les faits constatés et les obligations du détenteur."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => openDocument(getDsLettreInfoUrl(dossierData?.id ?? null)),
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>

        <div
          class="fr-col-12"
          :class="dossierData?.auteur_identifie ? 'fr-col-md-6' : 'fr-col-lg-12'"
        >
          <DsfrCard
            title="Rapport de constatation"
            description="Résumé des observations de terrain et des préjudices causés."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                iconOnly: false,
                onClick: () => openDocument(getDsDocConstatUrl(dossierData?.id ?? null)),
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>
      </div>

      <div v-if="dossierData">
        <DsInfoAuteurIdentifie
          v-if="dossierData.auteur_identifie"
          :modify-url="getDsModifyUrl(dossierData.ds_numero_dossier)"
        />
        <DsInfoAuteurNonIdentifie
          v-else
          :modify-url="getDsModifyUrl(dossierData.ds_numero_dossier)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import DsInfoAuteurIdentifie from '../components/ds/DsInfoAuteurIdentifie.vue'
import DsInfoAuteurNonIdentifie from '../components/ds/DsInfoAuteurNonIdentifie.vue'
import { API_URLS, createResource } from '../services/api'
import { getDsDocConstatUrl, getDsLettreInfoUrl, getDsModifyUrl } from '../services/urls'

const route = useRoute()
const showLoading = ref(true)
const isLoading = ref(false)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)

const openDocument = (url: string) => {
  if (!url) return
  window.open(url, '_blank', 'noopener')
}

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
