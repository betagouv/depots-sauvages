<template>
  <div class="fr-container--sm fr-m-1w">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <fieldset
        class="fr-form-group fr-fieldset--no-border fr-mb-3w"
        :class="{ 'fr-form-group--error': showPhotoDispoError }"
      >
        <legend
          class="fr-text--regular"
          :class="{ 'fr-pb-2w': !showPhotoDispoError }"
        >
          Avez-vous des photos du dépôt ? *
        </legend>
        <p v-if="showPhotoDispoError" class="fr-error-text fr-my-2w" tabindex="-1" ref="photoDispoErrorMessage" id="error-message-photoDispo" aria-live="polite">
          {{store.errors.photoDispo}}
        </p>
        <div class="fr-radio-group fr-my-1w fr-py-1w">
          <input
            type="radio"
            id="photosDipo-oui"
            name="photo-dispo"
            value="oui"
            :checked="store.formData.photoDispo === true"
            @change="store.updateBooleanField('photoDispo', 'oui')"
            aria-describedby="error-message-photoDispo"
            required
          />
          <label class="fr-label" for="photosDipo-oui">Oui</label>
        </div>

        <div class="fr-radio-group fr-my-1w">
          <input
            type="radio"
            id="photosDipo-non"
            name="photo-dispo"
            value="non"
            :checked="store.formData.photoDispo === false"
            @change="store.updateBooleanField('photoDispo', 'non')"
            aria-describedby="error-message-photoDispo"
            required
          />
          <label class="fr-label" for="photosDipo-non">Non</label>
        </div>
      </fieldset>

      <fieldset
        class="fr-form-group fr-fieldset--no-border fr-mb-3w"
        :class="{ 'fr-form-group--error': showRisqueEcoulementError }"
      >
        <legend
          class="fr-text--regular"
          :class="{ 'fr-pb-2w': !showRisqueEcoulementError }"
        >
          Existe-t-il un risque d’écoulement ? *
        </legend>
        <p v-if="showRisqueEcoulementError" class="fr-error-text fr-my-2w" tabindex="-1" ref="risqueEcoulementErrorMessage" id="error-message-risqueEcoulement" aria-live="polite">
          {{store.errors.risqueEcoulement}}
        </p>
        <div class="fr-radio-group fr-my-1w fr-py-1w">
          <input
            type="radio"
            id="risqueEcoulement-oui"
            name="risque-ecoulement"
            value="oui"
            :checked="store.formData.risqueEcoulement === true"
            @change="store.updateBooleanField('risqueEcoulement', 'oui')"
            aria-describedby="error-message-risqueEcoulement"
            required
          />
          <label class="fr-label" for="risqueEcoulement-oui">Oui</label>
        </div>

        <div class="fr-radio-group fr-my-1w">
          <input
            type="radio"
            id="risqueEcoulement-non"
            name="risque-ecoulement"
            value="non"
            :checked="store.formData.risqueEcoulement === false"
            @change="store.updateBooleanField('risqueEcoulement', 'non')"
            aria-describedby="error-message-risqueEcoulement"
            required
          />
          <label class="fr-label" for="risqueEcoulement-non">Non</label>
        </div>
      </fieldset>

      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-input-group" :class="{ 'fr-input-group--error': store.errors.volumeDepot }">
          <label class="fr-label" for="volumeDepot">Volume estimé (en m3) *</label>
          <select
            id="volumeDepot"
            v-model="store.formData.volumeDepot"
            @change="clearError('volumeDepot')"
            class="fr-select"
            aria-describedby="error-message-volumeDepot"
          >
            <option disabled value="">Veuillez sélectionner une option</option>
            <option v-for="option in volumeOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
          <p v-if="store.errors.volumeDepot" class="fr-error-text" id="error-message-volumeDepot" aria-live="polite">
            {{ store.errors.volumeDepot }}
          </p>
        </div>
      </div>

      <div class="fr-col-12 fr-mt-2w">
        <fieldset
          class="fr-form-group fr-fieldset--no-border"
          :class="{ 'fr-form-group--error': showTypeDepotsError }"
        >
          <legend
            class="fr-pb-2w fr-text--regular"
            :class="{ 'fr-pb-2w': !showTypeDepotsError }"
          >
            Type de dépôts *
          </legend>
          <p
            v-if="showTypeDepotsError"
            class="fr-error-text fr-my-2w"
            tabindex="-1"
            ref="typeDepotsErrorMessage"
            id="error-message-typeDepots"
            aria-live="polite"
          >
            Le champ Type de dépôts est vide. Veuillez sélectionner au moins une option.
          </p>
            <div class="fr-fieldset__content">
              <div
                v-for="option in typesDepotOptions"
                :key="option.value"
                class="fr-checkbox-group"
              >
                <input
                  type="checkbox"
                  :id="option.id"
                  :name="option.name"
                  :value="option.value"
                  v-model="store.formData.typesDepot"
                  aria-describedby="error-message-typeDepots"
                />
                <label class="fr-label" :for="option.id">{{ option.label }}</label>
              </div>
            </div>
          </fieldset>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrInput
          v-model="store.formData.precisionsDepot"
          label="Autres informations"
          hint="Apportez tout autre élément (présence d'habitation, présence d'élevage, voie ferrée, etc.), identité du propriétaire du terrain (si terrain privé), zone particulière (zone agricole, zone forestière, zone naturelle, zone humide, zone Natura 2000, zone Ramsar, etc.), cours d'eau à proximité ou un captage d'eau, dernière date à laquelle le dépôt n'était pas présent (si vous en avez connaissance)."
          :isTextarea="true"
        />
      </div>


      <div class="fr-col-12 fr-col-md-6">
        <DsfrInput
          v-if="store.formData.indicesDisponibles.includes('autre')"
          v-model="store.formData.precisionsIndices"
          label="Précisez les autres indices"
          name="precisions-indices"
          type="text"
        />
      </div>

      <div class="fr-mt-3w actions-row">
        <DsfrButton
          type="button"
          label="Précédent"
          icon="fr-icon-arrow-left-line"
          secondary
          @click="handlePrevious"
        />
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
import '@/styles/form-steps.css'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrInput } from '@gouvminint/vue-dsfr'
import { nextTick, ref, watch } from 'vue'
import {
  typesDepotOptions,
  volumeOptions
} from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false)
const showTypeDepotsError = ref(false)
const showPhotoDispoError = ref(false)
const showRisqueEcoulementError = ref(false)
const typeDepotsErrorMessage = ref<HTMLElement | null>(null)

const validateStep2 = () => {
  const errors: Record<string, string> = {}

  if (!store.formData.volumeDepot) {
    errors.volumeDepot = 'Le champ Volume estimé est vide. Veuillez sélectionner une option.'
  }

  if (store.formData.photoDispo === null || store.formData.photoDispo === undefined) {
    errors.photoDispo = 'Le champ Avez-vous des photos du dépôt est vide. Veuillez indiquer si vous avez des photos du dépôt.'
  }

  if (store.formData.risqueEcoulement === null || store.formData.risqueEcoulement === undefined) {
    errors.risqueEcoulement = 'Le champ Existe-t-il un risque d’écoulement ? est vide. Veuillez indiquer s’il existe un risque d’écoulement.'
  }

  showTypeDepotsError.value = !store.formData.typesDepot || store.formData.typesDepot.length === 0
  store.errors = errors
  return Object.keys(errors).length === 0 && !showTypeDepotsError.value
}


watch(
  () => store.formData.typesDepot,
  (selectedOptions) => {
    if (Array.isArray(selectedOptions) && selectedOptions.length > 0) {
      showTypeDepotsError.value = false
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

  const isValid = validateStep2()

  if (!isValid) {
    await nextTick()

    if (showTypeDepotsError.value && typeDepotsErrorMessage.value instanceof HTMLElement) {
      typeDepotsErrorMessage.value.focus()
    } else {
      const firstErrorElement = document.querySelector(
        '.fr-input-group--error select, .fr-input-group--error input, .fr-form-group--error input, .fr-error-text'
      )
      if (firstErrorElement instanceof HTMLElement) {
        firstErrorElement.focus()
      }
    }

    return
  }

  isSubmitting.value = true

  try {
    await store.saveFormData()
    store.updateStep(3)
  } catch (error) {
    console.error('Failed to save:', error)
  } finally {
    isSubmitting.value = false
  }
}

const handlePrevious = () => store.updateStep(1)
</script>

<style scoped>
.actions-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.fr-fieldset--no-border {
  border: none;
  margin: 0;
  padding: 0;
  color: #161616 !important;
}
</style>
