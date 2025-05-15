<template>
  <div class="fr-container--sm">
    <h2 class="fr-h3 fr-mb-3w">Où se trouve le dépôt sauvage et comment vous contacter ?</h2>
    <div class="fr-form-group">
      <p class="fr-text--sm fr-mb-3w">
        Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires
      </p>
      <form @submit.prevent="handleSubmit" class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.commune"
            label="📍 Sur quelle commune a eu lieu le dépôt ?"
            required
          />
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.localisationDepot"
            label="🏠 Quelle est l'adresse du dépôt de déchets ?"
            hint="(numéro, lieu, type, libellé de voie...)"
            required
          />
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrSelect
            v-model="store.formData.auteurSignalement"
            label="👮 Qui a réalisé la constatation ?"
            :options="auteurOptions"
            required
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

        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.dateConstat"
            type="date"
            label="Date de la constatation"
            hint="au format JJ/MM/AAAA"
          />
        </div>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="store.formData.heureConstat"
            type="time"
            label="Heure de la constatation"
            hint=" au format HH:MM"
          />
        </div>

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
            v-model="store.formData.natureTerrain"
            name="nature-terrain"
            legend="🌍 Quelle est la nature du terrain concerné par le dépôt ?"
            :options="natureTerrainOptions"
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
          <DsfrRadioButtonSet
            @update:model-value="(value) => store.updateBooleanField('risqueEcoulement', value)"
            name="risque-ecoulement"
            legend="Existe-t-il un risque d'écoulement ?"
            :options="yesNoOptions"
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
  </div>
</template>

<script setup lang="ts">
import '@/assets/styles/form-steps.css'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrInput } from '@gouvminint/vue-dsfr'
import { ref } from 'vue'
import {
  auteurOptions,
  natureTerrainOptions,
  typesDepotOptions,
  volumeOptions,
  yesNoOptions,
} from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false)

const handleSubmit = async (event: Event) => {
  event.preventDefault()

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
.actions-row {
  display: flex;
  justify-content: flex-end;
}

/* Fix for Safari/iOS time input */
input[type='time'] {
  width: 100%;
  min-width: 0;
  display: block;
  box-sizing: border-box;
}
</style>
