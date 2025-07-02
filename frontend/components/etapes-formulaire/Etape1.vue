<template>
  <div class="fr-container--sm fr-m-1w">
      <p class="fr-text--sm fr-mb-3w">
        Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires
      </p>
      <h2 class="fr-h5 fr-mb-3w">Localisation du dépôt</h2>
      <form @submit.prevent="handleSubmit" class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.commune"
            label="Commune du dépôt"
            required
          />
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.localisationDepot"
            label="Adresse du dépôt"
            hint="(numéro, lieu, type, libellé de voie...)"
            required
          />
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
            <p v-if="showNatureTerrainError" class="fr-error-text fr-my-2w" tabindex="-1" ref="natureTerrainErrorMessage">
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
                />
                <label class="fr-label" :for="option.id">{{ option.label }}</label>
              </div>
            </div>
          </fieldset>
        </div>

        <div class="fr-col-12 fr-form-group">
          <h2 class="fr-h5 fr-mb-3w">Détails de la constatation</h2>
          <DsfrSelect
              v-model="store.formData.auteurSignalement"
              label="Qui a constaté le dépôt ?"
              :options="auteurOptions"
              required
            />
            <DsfrInput
              v-model="store.formData.dateConstat"
              type="date"
              label="Date de la constatation"
              hint="au format JJ/MM/AAAA"
              required
            />
          <div class="fr-mt-3w">
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
              required
            />
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
import { DsfrInput } from '@gouvminint/vue-dsfr'
import { ref, warn, watch } from 'vue'
import {
  auteurOptions,
  natureTerrainOptions,
} from './form-data'

const store = useSignalementStore()

const isSubmitting = ref(false)
const showNatureTerrainError = ref(false)
const natureTerrainErrorMessage = ref<HTMLElement | null>(null)

watch(
  () => store.formData.typesDepot,
  (selectedOptions) => {
    if (Array.isArray(selectedOptions) && selectedOptions.length > 0) {
      showNatureTerrainError.value = false
    }
  },
  {deep: true }
)

const handleSubmit = async (event: Event) => {
  event.preventDefault()

  // Force le blur de l'élément actif pour éviter le blocage Safari
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
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
