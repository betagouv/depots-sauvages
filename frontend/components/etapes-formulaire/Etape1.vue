<template>
  <div class="fr-container--sm fr-m-1w">
      <p class="fr-text--sm fr-mb-3w">
        Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires
      </p>
      <h3 class="fr-h5 fr-mb-3w">Localisation du dépôt</h3>
      <form @submit.prevent="handleSubmit" class="fr-grid-row fr-grid-row--gutters">
        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': store.errors.commune && !store.formData.commune }"
        >
          <label class="fr-label" for="commune">Commune du dépôt *</label>
          <input
            id="commune"
            type="text"
            v-model="store.formData.commune"
            @input="clearError('commune')"
            class="fr-input"
            aria-describedby="error-message-commune"
          />
          <p v-if="store.errors.commune && !store.formData.commune" class="fr-error-text" id="error-message-commune" aria-live="polite">
            {{ store.errors.commune }}
          </p>
        </div>

        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': store.errors.localisationDepot && !store.formData.localisationDepot }"
        >
          <label class="fr-label" for="adresse">Adresse du dépôt *</label>
          <span class="fr-hint-text">(numéro, lieu, type, libellé de voie...)</span>
          <input
            id="adresse"
            type="text"
            v-model="store.formData.localisationDepot"
            @input="clearError('localisationDepot')"
            class="fr-input"
            aria-describedby="error-message-localisationDepot"
          />
          <p v-if="store.errors.localisationDepot && !store.formData.localisationDepot" class="fr-error-text" id="error-message-localisationDepot" aria-live="polite">
            {{ store.errors.localisationDepot }}
          </p>
        </div>

        <div class="fr-col-12">
          <fieldset
            ref="natureTerrainFieldSet"
            class="fr-form-group fr-fieldset--no-border"
            :class="{ 'fr-form-group--error': showNatureTerrainError }"
          >
            <legend
              class="fr-text--regular"
              :class="{ 'fr-pb-2w': !showNatureTerrainError }"
            >
              Nature du terrain *
            </legend>
            <p v-if="showNatureTerrainError" class="fr-error-text fr-my-2w" tabindex="-1" ref="natureTerrainErrorMessage" id="error-message-natureTerrain" aria-live="polite">
              Le champ Nature du terrain est vide. Veuillez sélectionner au moins une option.
            </p>
            <div class="fr-fieldset__content">
              <div
                v-for="option in natureTerrainOptions"
                :key="option.value"
                class="fr-checkbox-group"
              >
                <input
                  type="checkbox"
                  :id="option.id"
                  :name="option.label"
                  :value="option.value"
                  v-model="store.formData.typesDepot"
                  aria-describedby="error-message-natureTerrain"
                />
                <label class="fr-label" :for="option.id">{{ option.label }}</label>
              </div>
            </div>
          </fieldset>
        </div>

        <div class="fr-col-12 fr-form-group">
          <h3 class="fr-h5 fr-mb-3w">Détails de la constatation</h3>
          <div class="fr-input-group" :class="{ 'fr-input-group--error': store.errors.auteurSignalement }">
            <label class="fr-label" for="auteurSignalement">Qui a constaté le dépôt ?</label>
            <select
              id="auteurSignalement"
              v-model="store.formData.auteurSignalement"
              @change="clearError('auteurSignalement')"
              class="fr-select"
              aria-describedby="error-message-auteur"
            >
              <option disabled value="">Veuillez sélectionner une option</option>
              <option v-for="option in auteurOptions" :key="option.value" :value="option.value">
                {{ option.text }}
              </option>
            </select>
            <p v-if="store.errors.auteurSignalement" class="fr-error-text" id="error-message-auteur" aria-live="polite">
              {{ store.errors.auteurSignalement }}
            </p>
          </div>

          <div class="fr-input-group" :class="{ 'fr-input-group--error': store.errors.dateConstat && !store.formData.dateConstat }">
            <label class="fr-label" for="date-constat">Date de la constatation</label>
            <input
              id="date-constat"
              type="date"
              v-model="store.formData.dateConstat"
              @input="clearError('dateConstat')"
              class="fr-input"
              aria-describedby="error-message-dateConstat"
            />
            <p v-if="store.errors.dateConstat" class="fr-error-text" id="error-message-dateConstat" aria-live="polite">
              {{store.errors.dateConstat}}
            </p>
          </div>

          <div class="fr-input-group" :class="{ 'fr-input-group--error': store.errors.heureConstat && !store.formData.heureConstat }">
            <label class="fr-label" for="heure-constatation">
              Heure de la constatation *
              <span class="fr-hint-text">Format attendu : HH:MM</span>
            </label>
            <input
              type="time"
              v-model="store.formData.heureConstat"
              id="heure-constatation"
              name="heure-constatation"
              class="fr-input"
              min="00:00"
              max="23:59"
              aria-describedby="error-message-heureConstatation"
            />
            <p  v-if="store.errors.heureConstat && !store.formData.heureConstat" class="fr-error-text fr-my-2w" id="error-message-heureConstatation" aria-live="polite">
              {{store.errors.heureConstat}}
            </p>
          </div>
        </div>

        <div class="fr-col-12 fr-mt-3w actions-row">
          <DsfrButton
            type="submit"
            label="Suivant"
            icon="fr-icon-arrow-right-line"
            icon-right
            :disabled="isSubmitting"
          />
        </div>
      </form>
  </div>
</template>

<script setup lang="ts">
import { useSignalementStore } from '@/stores/signalement'
import '@/styles/form-steps.css'
import { nextTick, ref, watch } from 'vue'
import {
  auteurOptions,
  natureTerrainOptions,
} from './form-data'

const store = useSignalementStore()

const isSubmitting = ref(false)
const showNatureTerrainError = ref(false)
const natureTerrainErrorMessage = ref<HTMLElement | null>(null)

const validateStep1 = () => {
  const errors: Record<string, string> = {}
  showNatureTerrainError.value = false

  if (!store.formData.commune) {
    errors.commune = 'Le champ Commune du dépôt est vide. Veuillez renseigner une commune.'
  }

  if (!store.formData.localisationDepot) {
    errors.localisationDepot = 'Le champ Adresse du dépôt est obligatoire. Veuillez renseigner une adresse.'
  }

  if (!store.formData.typesDepot || store.formData.typesDepot.length === 0) {
    showNatureTerrainError.value = true
  }

  if (!store.formData.auteurSignalement) {
    errors.auteurSignalement = 'Le champ Qui a constaté le dépôt est vide. Veuillez sélectionner une option dans la liste.'
  }

  if (!store.formData.dateConstat) {
    errors.dateConstat = 'Le champ Date de la constatation est vide. Veuillez renseigner une date.'
  }

  if (!store.formData.heureConstat) {
    errors.heureConstat = 'Le champ Heure de la constatation est vide. Veuillez renseigner une heure.'
  }

  store.errors = errors

  return Object.keys(errors).length === 0 && !showNatureTerrainError.value
}


watch(
  () => store.formData.typesDepot,
  (selectedOptions) => {
    if (Array.isArray(selectedOptions) && selectedOptions.length > 0) {
      showNatureTerrainError.value = false
    }
  },
  {deep: true }
)

const clearError = (field: string) => {
  if (store.errors[field]) {
    delete store.errors[field]
  }
}

const handleSubmit = async (event: Event) => {
  event.preventDefault()

  // Force le blur de l'élément actif pour éviter le blocage Safari
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
  }

  if (!validateStep1()) {
    nextTick(() => {
      const firstErrorInput = document.querySelector('.fr-input-group--error input, .fr-form-group--error input, .fr-error-text')
      if (firstErrorInput instanceof HTMLElement) {
        firstErrorInput.focus()
      }
    })
    return
  }

  showNatureTerrainError.value = store.formData.typesDepot.length === 0
  if (showNatureTerrainError.value) {
    natureTerrainErrorMessage.value?.focus()
    return
  }

  isSubmitting.value = true
  try {
    await store.saveFormData()
    store.updateStep(2)
  } catch (error) {
    console.error('Failed to save:', error)
  } finally {
    isSubmitting.value = false
  }
}

</script>

<style scoped>
@supports (-webkit-touch-callout: none) {
  input[type="time"] {
    min-height: 3rem;
    -webkit-appearance: none;
    appearance: none;
  }
}

::v-deep(input[type="time"]) {
  font-family: inherit;
  font-size: 1rem;
  padding: 1rem;
  height: auto;
  border: 1px solid #ddd;
  box-sizing: border-box;
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
}

::v-deep(input[type="time"]:focus) {
  outline: 2px solid #0a76f6;
  outline-offset: 2px;
}

.actions-row {
  display: flex;
  justify-content: flex-end;
}

.fr-fieldset--no-border {
  border: none;
  margin: 0;
  padding: 0;
  color: #161616 !important;
}

</style>
