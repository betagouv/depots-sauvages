<template>
  <div>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              <template v-if="auteurIdentifie">Télécharger les pièces de procédure</template>
              <template v-else>Télécharger le rapport de constatation</template>
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              <template v-if="auteurIdentifie">
                Vous trouverez ci-dessous vos pièces de procédure <strong>pré-remplies</strong>, à
                compléter avec les éléments manquants, par exemple la charte graphique de la mairie,
                la date et la signature de l'autorité compétente (maire ou personne habilitée à
                réaliser des constatations).
              </template>
              <template v-else>
                Vous trouverez ci-dessous votre rapport de constatation <strong>pré-rempli</strong>,
                à compléter avec les éléments manquants, par exemple la charte graphique de la
                mairie, la date et la signature de la personne habilitée à réaliser des
                constatations.
              </template>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="fr-container fr-pb-4w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div :class="rapportColClass">
          <DsfrCard
            title="Rapport de constatation"
            description="Résumé des observations de terrain et des préjudices causés. À conserver en mairie ou à transmettre lors d'un dépôt de plainte."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                onClick: () => openDocument(getDsDocConstatUrl(dossierData?.id ?? null)),
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          />
        </div>
        <div v-if="auteurIdentifie" class="fr-col-12 fr-col-md-6">
          <DsfrCard
            title="Lettre d'information"
            description="Courrier rappelant les faits constatés et les obligations de l'auteur du responsable probable du dépôt sauvage. À envoyer à l'auteur probable des faits (avec accusé de réception)."
            :buttons="[
              {
                label: 'Télécharger',
                icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
                onClick: () => openDocument(getDsLettreInfoUrl(dossierData?.id ?? null)),
              },
            ]"
            size="large"
            no-arrow
            title-tag="h2"
          >
            <template #end-details>
              <p class="fr-text--sm fr-text-mention--grey fr-mt-2w fr-mb-0">
                <VIcon name="ri-information-line" class="fr-mr-1w" />
                Utile uniquement pour la procédure administrative
              </p>
            </template>
          </DsfrCard>
        </div>
      </div>
    </div>
    <div v-if="showLoading" class="fr-container fr-pb-4w">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
          <div class="loading-section fr-p-4w fr-text--center" role="status" aria-live="polite">
            <VIcon
              name="ri-loader-4-line"
              :scale="3"
              animation="spin"
              class="fr-mb-2w"
              aria-hidden="true"
            />
            <p class="fr-text--lg fr-mb-0">Préparation de vos documents en cours...</p>
            <p class="fr-text--sm fr-text-mention--grey">Veuillez patienter quelques instants.</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="fr-container fr-pb-4w">
      <div v-if="error" class="fr-alert fr-alert--error fr-mb-4w" role="alert" aria-live="polite">
        <p class="fr-alert__title">Erreur</p>
        <p>{{ error }}</p>
      </div>

      <div v-if="dossierData">
        <InfoAuteurIdentifie v-if="auteurIdentifie" />
        <InfoAuteurNonIdentifie
          v-else
          :modify-url="getDsModifyUrl(dossierData.ds_numero_dossier)"
        />
      </div>

      <div v-if="dossierData" class="fr-grid-row fr-grid-row--gutters">
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
            description="Si vous avez besoin de modifier les informations, merci de modifier votre dossier sur votre démarche numérique."
            :buttons="[
              {
                label: 'Consulter ou modifier',
                icon: { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' },
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

      <div class="fr-grid-row fr-grid-row--gutters fr-mt-4w">
        <div class="fr-col-12">
          <div class="fr-card fr-card--lg">
            <div class="fr-card__body">
              <h3 class="fr-card__title">Ressources utiles</h3>
              <div class="fr-card__desc">
                <p class="fr-mb-2w">
                  <VIcon name="ri-arrow-right-line" class="fr-mr-1w" /> Pour un accompagnement pas à
                  pas, consultez le
                  <a
                    href="https://acdechets.smartidf.services/aide-verbalisation"
                    class="fr-link fr-icon-external-link-line fr-link--icon-right"
                    target="_blank"
                    rel="nopener"
                  >
                    guide ACDéchets de la Région Île-de-France
                  </a>
                </p>
                <p class="fr-mb-2w">
                  <VIcon name="ri-arrow-right-line" class="fr-mr-1w" /> Retrouvez des conseils
                  pratiques sur l'application à destination des élus, Gend'élus, accessible à tout
                  le monde :
                </p>
                <ul class="fr-pl-4w fr-mb-0">
                  <li>
                    <a
                      href="https://play.google.com/store/apps/details?id=com.gendelus&hl=fr&pli=1"
                      class="fr-link fr-icon-external-link-line fr-link--icon-right"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      Télécharger sur le Play Store
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://apps.apple.com/fr/app/gend%C3%A9lus/id6444316373"
                      class="fr-link fr-icon-external-link-line fr-link--icon-right"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      Télécharger sur l'App Store
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import InfoAuteurIdentifie from '../components/ds/InfoAuteurIdentifie.vue'
import InfoAuteurNonIdentifie from '../components/ds/InfoAuteurNonIdentifie.vue'
import { API_URLS, createResource } from '../services/api'
import { getDsDocConstatUrl, getDsLettreInfoUrl, getDsModifyUrl } from '../services/urls'

const route = useRoute()
const showLoading = ref(true)
const error = ref<string | null>(null)
const dossierData = ref<any>(null)

const auteurIdentifie = computed(() => dossierData.value?.auteur_identifie ?? false)
const rapportColClass = computed(() =>
  auteurIdentifie.value ? 'fr-col-12 fr-col-md-6' : 'fr-col-12 fr-col-lg-12'
)

const openDocument = (url: string) => {
  if (!url) return
  window.open(url, '_blank', 'noopener,noreferrer')
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
  error.value = null
  try {
    dossierData.value = await createResource(API_URLS.processDossier, {
      dossier_id: dossierId,
    })
  } catch (err: any) {
    error.value = err.error || 'An error occurred while processing the dossier'
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
