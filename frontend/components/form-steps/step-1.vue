<script setup lang="ts">
import '@/assets/styles/form-steps.css'
import { useSignalementStore } from '@/stores/signalement'
import { computed } from 'vue'
import { auteurOptions, natureTerrainOptions, typesDepotOptions, volumeOptions } from './form-data'

const store = useSignalementStore()

const showPhotoUpload = computed(() => store.formData.hasPhotos === 'oui')

const yesNoOptions = [
  { label: 'Oui', value: 'oui' },
  { label: 'Non', value: 'non' },
]

const handleSubmit = async (event: Event) => {
  event.preventDefault()
  try {
    await store.saveFormData()
    store.updateStep(2)
  } catch (error) {
    console.error('Failed to save:', error)
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
  const currentTypes = [...(store.formData.typesDepot || [])]

  if (checked && !currentTypes.includes(value)) {
    currentTypes.push(value)
  } else if (!checked) {
    const index = currentTypes.indexOf(value)
    if (index > -1) {
      currentTypes.splice(index, 1)
    }
  }

  store.formData.typesDepot = currentTypes
}
</script>

<template>
  <h2 class="step-question">Où se trouve le dépôt sauvage et comment vous contacter ?</h2>
  <div class="form-container">
    <form @submit.prevent="handleSubmit">
      <DsfrInput
        v-model="store.formData.commune"
        label="📍 Sur quelle commune a eu lieu le dépôt ?"
        required
      />

      <DsfrInput
        v-model="store.formData.adresseDepot"
        label="🏠 Quelle est l'adresse du dépôt de déchets ?"
        required
      />

      <DsfrSelect
        v-model="store.formData.auteurSignalement"
        label="👮 Qui a réalisé la constatation ?"
        :options="auteurOptions"
        required
      />

      <div class="date-time">
        <DsfrInput
          v-model="store.formData.dateConstat"
          type="date"
          label="Date du constat"
          required
        />
        <DsfrInput
          v-model="store.formData.heureConstat"
          type="time"
          label="Heure du constat"
          required
        />
      </div>

      <div class="photo-section">
        <DsfrRadioButtonSet
          :model-value="store.formData.photoDispo ? 'oui' : 'non'"
          @update:model-value="store.updateBooleanField('photoDispo', $event)"
          name="photo-dispo"
          legend="Avez-vous des photos du dépôt ?"
          :options="yesNoOptions"
          required
        />

        <DsfrFileUpload
          v-if="showPhotoUpload"
          v-model="store.formData.photos"
          label="Ajouter vos photos"
          hint="Formats acceptés : .jpg, .jpeg, .png, .pdf"
          accept=".jpg,.jpeg,.png,.pdf"
          multiple
          @change="handleFileChange"
        />
      </div>

      <DsfrRadioButtonSet
        v-model="store.formData.natureTerrain"
        name="nature-terrain"
        legend="🌍 Nature du terrain"
        :options="natureTerrainOptions"
        required
      />

      <DsfrSelect
        v-model="store.formData.volumeDechets"
        label="📏 Volume estimé"
        :options="volumeOptions"
        required
      />

      <div class="fr-form-group">
        <legend class="fr-fieldset__legend fr-text--regular">Types de dépôts</legend>
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
        v-model="store.formData.precisionsDechets"
        label="✏️ Précisions sur les déchets"
        hint="N'inscrivez AUCUNE DONNÉE personnelle"
        :isTextarea="true"
      />

      <div class="form-actions">
        <DsfrButton type="submit" label="Suivant" icon="fr-icon-arrow-right-line" icon-right />
      </div>
    </form>
  </div>
</template>

<style scoped>
.photo-section {
  border-radius: 8px;
  margin-bottom: 1.5rem;
  margin-top: 1.5rem;
}

.photo-section :deep(.fr-upload) {
  margin-top: 1rem;
}
</style>
