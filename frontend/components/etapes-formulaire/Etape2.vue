<template>
  <div class="fr-container--sm">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <div class="fr-col-12">
        <DsfrRadioButtonSet
          :model-value="store.formData.photoDispo ? 'oui' : 'non'"
          @update:model-value="(value) => store.updateBooleanField('photoDispo', value)"
          name="photo-dispo"
          legend="Avez-vous des photos du dépôt ?"
          :options="yesNoOptions"
          required
        />
      </div>
      <div class="fr-col-12">
        <DsfrRadioButtonSet
          @update:model-value="(value) => store.updateBooleanField('risqueEcoulement', value)"
          name="risque-ecoulement"
          legend="Existe-t-il un risque d'écoulement ?"
          :options="yesNoOptions"
          required
        />
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <DsfrSelect
          v-model="store.formData.volumeDepot"
          label="📏 Volume estimé"
          hint="en m3"
          :options="volumeOptions"
          required
        />
      </div>
      <div class="fr-col-12">
        <div class="fr-form-group">
          <legend class="fr-fieldset__legend fr-text--regular">Type de dépôts</legend>
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
              />
              <label class="fr-label" :for="option.id">{{ option.label }}</label>
            </div>
          </div>
        </div>
      </div>


      <div class="fr-col-12 fr-col-md-6">
        <DsfrInput
          v-model="store.formData.precisionsDepot"
          label="✏️ Autres informations"
          hint="Apportez tout autre élément (présence d'habitation, présence d'élevage, voie ferrée, etc.), identité du propriétaire du terrain (si terrain privé), zone particulière (zone agricole, zone forestière, zone naturelle, zone humide, zone Natura 2000, zone Ramsar, etc.), cours d'eau à proximité ou un captage d'eau, dernière date à laquelle le dépôt n'étais pas présent (si vous en avez connaissance)."
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
import { DsfrInput, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed, ref } from 'vue'
import {
  indicesDisponiblesOptions,
  statutAuteurOptions,
  typesDepotOptions,
  volumeOptions,
  yesNoOptions,
} from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false)
const showBlocAuteur = computed(() => store.formData.auteurIdentifie)

const handleSubmit = async (event: Event) => {
  event.preventDefault()
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
</style>
