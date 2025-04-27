<template>
  <h2 class="step-question">Où se trouve le dépôt sauvage et comment vous contacter ?</h2>
  <div class="form-container">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <DsfrInput
        v-model="store.formData.commune"
        label="📍 Sur quelle commune a eu lieu le dépôt ?"
        required
      />

      <DsfrInput
        v-model="store.formData.localisationDepot"
        label="🏠 Quelle est l'adresse du dépôt de déchets ?"
        hint="(numéro, lieu, type, libellé de voie...)"
        required
      />

      <DsfrSelect
        v-model="store.formData.auteurSignalement"
        label="👮 Qui a réalisé la constatation ?"
        :options="auteurOptions"
        required
      />
      <DsfrInput
        v-if="store.formData.indicesDisponibles.includes('autre')"
        v-model="store.formData.precisionsIndices"
        label="Précisez les autres indices"
        name="precisions-indices"
        type="text"
      />

      <div class="date-time">
        <DsfrInput
          v-model="store.formData.dateConstat"
          type="date"
          label="Date de la constatation"
          hint="au format JJ/MM/AAAA"
          required
        />
        <DsfrInput
          v-model="store.formData.heureConstat"
          type="time"
          label="Heure de la constatation"
          hint=" au format HH:MM"
          required
        />
      </div>

      <div class="photo-section">
        <DsfrRadioButtonSet
          :model-value="store.formData.photoDispo ? 'oui' : 'non'"
          @update:model-value="(value) => store.updateBooleanField('photoDispo', value)"
          name="photo-dispo"
          legend="Avez-vous des photos du dépôt ?"
          :options="yesNoOptions"
          required
        />

        <!--        <DsfrFileUpload
          v-if="showPhotoUpload"
          v-model="store.formData.photos"
          label="Ajouter vos photos"
          hint="Formats acceptés : .jpg, .jpeg, .png, .pdf"
          accept=".jpg,.jpeg,.png,.pdf"
          multiple
          @change="handleFileChange"
        />-->
      </div>

      <DsfrRadioButtonSet
        v-model="store.formData.natureTerrain"
        name="nature-terrain"
        legend="🌍 Quelle est la nature du terrain concerné par le dépôt ?"
        :options="natureTerrainOptions"
        required
      />

      <DsfrSelect
        v-model="store.formData.volumeDepot"
        label="📏 Volume estimé"
        hint="en m3"
        :options="volumeOptions"
        required
      />
      <DsfrRadioButtonSet
        @update:model-value="(value) => store.updateBooleanField('risqueEcoulement', value)"
        name="risque-ecoulement"
        legend="Existe-t-il un risque d'écoulement ?"
        :options="yesNoOptions"
        required
      />

      <div class="fr-form-group">
        <legend class="fr-fieldset__legend fr-text--regular">Type de dépôts</legend>
        <div class="fr-fieldset__content">
          <div v-for="option in typesDepotOptions" :key="option.value" class="fr-checkbox-group">
            <input
              type="checkbox"
              :id="option.id"
              :name="option.name"
              :value="option.value"
              :checked="store.formData.typesDepot?.includes(option.value) ?? false"
              @change="handleTypesDepotChange($event, option.value)"
            />
            <label class="fr-label" :for="option.id">{{ option.label }}</label>
          </div>
        </div>
      </div>

      <DsfrInput
        v-model="store.formData.precisionsDepot"
        label="✏️ Autres informations"
        hint="Apportez tout autre élément (présence d'habitation, présence d'élevage, voie ferrée, etc.), identité du propriétaire du terrain (si terrain privé), zone particulière (zone agricole, zone forestière, zone naturelle, zone humide, zone Natura 2000, zone Ramsar, etc.), cours d'eau à proximité ou un captage d'eau, dernière date à laquelle le dépôt n'étais pas présent (si vous en avez connaissance)."
        :isTextarea="true"
      />

      <div class="form-actions">
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
import '@/assets/styles/form-steps.css'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrInput } from '@gouvminint/vue-dsfr'
import { computed, ref } from 'vue'
import {
  auteurOptions,
  natureTerrainOptions,
  typesDepotOptions,
  volumeOptions,
  yesNoOptions,
} from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false) // Make this reactive
const showPhotoUpload = computed(() => store.formData.photoDispo === true)

const handleSubmit = async (event: Event) => {
  event.preventDefault()

  isSubmitting.value = true
  try {
    await store.saveFormData()
    store.updateStep(2)
  } catch (error) {
    console.error('Failed to save:', error)
    // Add error feedback here
  } finally {
    isSubmitting.value = false
  }
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    store.formData.photos = Array.from(target.files)
  }
}

const handleTypesDepotChange = (event: Event, value: string) => {
  const checked = (event.target as HTMLInputElement).checked

  // Create a new array to ensure reactivity
  let newTypes = [...(store.formData.typesDepot || [])]

  if (checked) {
    // Add value if it doesn't exist
    newTypes = [...newTypes, value]
  } else {
    // Remove value
    newTypes = newTypes.filter((type) => type !== value)
  }

  store.formData.typesDepot = newTypes
}
</script>

<style scoped>
.photo-section {
  border-radius: 8px;
  margin-bottom: 1.5rem;
  margin-top: 1.5rem;
}

.photo-section :deep(.fr-upload) {
  margin-top: 1rem;
}

.date-time {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .date-time {
    grid-template-columns: 1fr;
  }
}
</style>
