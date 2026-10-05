<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-2w">Accès réservé</h1>
        <p class="fr-text--lead fr-mb-0">
          L'espace de rédaction et de suivi des procédures est réservé aux collectivités et services
          compétents dans la lutte contre les dépôts sauvages.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-9 fr-col-lg-8">
          <DsfrAlert
            type="info"
            title="Votre établissement n'est pas encore activé d'office"
            title-tag="h2"
            class="fr-mb-4w"
          >
            <p class="fr-mb-0">
              L'accès est réservé aux collectivités et services compétents dans la lutte contre les
              dépôts sauvages. Si votre structure en fait partie, vous pouvez demander une
              activation ci-dessous.
            </p>
          </DsfrAlert>

          <DsfrAlert
            v-if="requestSent"
            type="success"
            title="Demande d'accès transmise avec succès"
            title-tag="h2"
            class="fr-mb-4w"
          >
            <p>
              Votre demande a bien été envoyée à notre équipe d'administration. Vous recevrez une
              réponse par email à l'adresse <strong>{{ form.email }}</strong> sous 24 heures
              ouvrées.
            </p>
            <div class="fr-mt-2w">
              <DsfrButton secondary @click="router.push('/')"> Retourner à l'accueil </DsfrButton>
            </div>
          </DsfrAlert>

          <div v-else class="fr-card fr-card--no-arrow shadow-card">
            <div class="fr-card__body fr-p-4w">
              <h2 class="fr-h3 fr-mb-2w">Demander l'accès pour votre établissement</h2>
              <p class="fr-text--sm fr-text--mention-grey fr-mb-4w">
                Ces informations ont été automatiquement pré-remplies à partir de votre profil
                ProConnect.
              </p>

              <form @submit.prevent="handleSubmit">
                <div class="fr-mb-3w">
                  <DsfrInputGroup
                    v-model="form.organization_label"
                    label="Établissement / Organisation"
                    hint="Nom de votre collectivité ou administration"
                    :readonly="true"
                    :required="true"
                  />
                </div>

                <div class="fr-grid-row fr-grid-row--gutters fr-mb-3w">
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInputGroup
                      v-model="form.siren"
                      label="Numéro SIREN"
                      hint="9 chiffres"
                      maxlength="9"
                      :readonly="true"
                    />
                  </div>
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInputGroup
                      v-model="form.siret"
                      label="Numéro SIRET (optionnel)"
                      hint="14 chiffres"
                      maxlength="14"
                      :readonly="true"
                    />
                  </div>
                </div>

                <div class="fr-grid-row fr-grid-row--gutters fr-mb-3w">
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInputGroup
                      v-model="form.name"
                      label="Nom et prénom de l'agent"
                      :readonly="true"
                    />
                  </div>
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInputGroup
                      v-model="form.email"
                      type="email"
                      label="Adresse e-mail professionnelle"
                      hint="Pour recevoir la notification d'activation"
                      :readonly="true"
                      :required="true"
                    />
                  </div>
                </div>

                <div class="fr-mb-4w">
                  <DsfrInputGroup
                    v-model="form.message"
                    :is-textarea="true"
                    label="Précision sur votre fonction ou mission (optionnel)"
                    hint="Ex : Police municipale, service environnement, gestion des déchets..."
                    placeholder="Expliquez brièvement votre rôle dans la lutte contre les dépôts sauvages..."
                    rows="3"
                  />
                </div>

                <DsfrAlert v-if="errorMessage" type="error" class="fr-mb-3w">
                  <p>{{ errorMessage }}</p>
                </DsfrAlert>

                <div class="fr-btns-group fr-btns-group--right fr-btns-group--inline-md">
                  <DsfrButton type="button" secondary @click="router.push('/')">
                    Annuler
                  </DsfrButton>
                  <DsfrButton type="submit" :disabled="isSubmitting || !form.email">
                    <span
                      v-if="isSubmitting"
                      class="fr-icon-refresh-line fr-icon--sm fr-mr-1w"
                      aria-hidden="true"
                    ></span>
                    {{ isSubmitting ? 'Transmission en cours...' : "Demander l'ouverture d'accès" }}
                  </DsfrButton>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert, DsfrButton, DsfrInputGroup } from '@gouvminint/vue-dsfr'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  getProConnectRejectedInfo,
  submitProConnectAccessRequest,
  type ProConnectAccessRequestPayload,
} from '../services/api'

const router = useRouter()

const form = reactive<ProConnectAccessRequestPayload>({
  organization_label: '',
  siren: '',
  siret: '',
  name: '',
  email: '',
  message: '',
})

const isSubmitting = ref(false)
const requestSent = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const data = await getProConnectRejectedInfo()
    if (data) {
      form.organization_label = data.organization_label || ''
      form.siret = data.siret || ''
      form.siren = data.siren || (data.siret ? data.siret.substring(0, 9) : '')
      form.name = data.name || ''
      form.email = data.email || ''
    }
  } catch (error) {}
})

const handleSubmit = async () => {
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    await submitProConnectAccessRequest({
      organization_label: form.organization_label,
      siren: form.siren,
      siret: form.siret,
      name: form.name,
      email: form.email,
      message: form.message,
    })
    requestSent.value = true
  } catch (error: any) {
    errorMessage.value =
      error?.error ||
      'Une erreur est survenue lors de l’envoi de votre demande. Veuillez réessayer ou contacter le support.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.shadow-card {
  height: auto !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e5e5;
  border-radius: 4px;
}

.shadow-card .fr-card__body {
  height: auto !important;
}

:deep(input[readonly]) {
  background-color: var(--background-contrast-grey) !important;
  color: var(--text-mention-grey) !important;
  cursor: not-allowed;
}
</style>
