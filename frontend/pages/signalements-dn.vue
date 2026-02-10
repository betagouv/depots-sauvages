<template>
  <div>
    <DnLoading v-if="showLoading" />
    <div v-else>
      <div v-if="error" class="fr-container fr-mb-4w fr-mt-4w" role="alert" aria-live="polite">
        <div class="fr-alert fr-alert--error">
          <p class="fr-alert__title">Erreur</p>
          <p>{{ error }}</p>
        </div>
      </div>

      <div v-else-if="dossierData">
        <DnHero :has-procedure="hasProcedure" :auteur-identifie="auteurIdentifie" />

        <div class="fr-container">
          <DnDocuments
            v-if="hasProcedure"
            :auteur-identifie="auteurIdentifie"
            :doc-constat-url="getDnDocConstatUrl(dossierData?.id ?? null)"
            :lettre-info-url="getDnLettreInfoUrl(dossierData?.id ?? null)"
          />

          <div v-else class="fr-my-4w">
            <p class="">
              Pour récupérer vos documents, merci de mettre à jour votre dossier sur la plateforme
              Démarches Numériques.
            </p>
            <DsfrAlert
              type="info"
              title="Note"
              description="Les formulaires de Protect’Envi évoluent régulièrement. Si vous avez rempli une version antérieure, une mise à jour de certaines informations peut être nécessaire pour accéder à vos documents."
            />
          </div>

          <div v-if="hasProcedure">
            <InfoAuteurIdentifie v-if="auteurIdentifie" />
            <InfoAuteurNonIdentifie
              v-else
              :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
            />
          </div>

          <DnInfos
            :dn-numero-dossier="dossierData.dn_numero_dossier"
            :dn-date-creation="dossierData.dn_date_creation"
            :dn-date-modification="dossierData.dn_date_modification"
            :modify-url="getDnModifyUrl(dossierData.dn_numero_dossier)"
          />

          <div v-if="hasProcedure" class="fr-grid-row fr-grid-row--gutters fr-mt-2w">
            <div class="fr-col-12">
              <RessourcesUtiles />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDossierStore } from '@/stores/dossier.ts'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import DnDocuments from '../components/dn/DnDocuments.vue'
import DnHero from '../components/dn/DnHero.vue'
import DnInfos from '../components/dn/DnInfos.vue'
import DnLoading from '../components/dn/DnLoading.vue'
import InfoAuteurIdentifie from '../components/dn/InfoAuteurIdentifie.vue'
import InfoAuteurNonIdentifie from '../components/dn/InfoAuteurNonIdentifie.vue'
import RessourcesUtiles from '../components/dn/RessourcesUtiles.vue'

import { API_URLS, createResource } from '../services/api'
import { getDnDocConstatUrl, getDnLettreInfoUrl, getDnModifyUrl } from '../services/urls'

const route = useRoute()
const dossierStore = useDossierStore()
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)

const hasProcedure = computed(() => {
  return dossierData.value && dossierData.value.created !== false
})

const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)

onMounted(async () => {
  const dossierId = (route.params.dossier_id as string) || (route.query.dossier_id as string)

  if (!dossierId) {
    error.value = 'dossier_id is required in the URL'
    showLoading.value = false
    return
  }

  error.value = null

  // Verify ownership via store
  const loginRequired = import.meta.env.VITE_LOGIN_REQUIRED !== 'false'
  if (loginRequired) {
    await dossierStore.fetchDossiers()
    const dossier = dossierStore.getDossierById(dossierId)

    if (!dossier) {
      error.value = "Vous n'avez pas les droits pour accéder à ce dossier ou il n'existe pas."
      showLoading.value = false
      return
    }
  }

  try {
    dossierData.value = await createResource(API_URLS.processDossier, {
      dossier_id: dossierId,
    })
  } catch (err: any) {
    error.value = err.error || 'Une erreur est survenue lors du traitement du dossier'
  } finally {
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
