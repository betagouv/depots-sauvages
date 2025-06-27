<template>
  <div class="fr-container--sm">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <h2>Récapitulatif</h2>

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
import { ref } from 'vue'

const store = useSignalementStore()
const isSubmitting = ref(false)

const handleSubmit = async (event: Event) => {
  event.preventDefault()
  isSubmitting.value = true
  try {
    await store.saveFormData()
    store.updateStep(5)
  } catch (error) {
    console.error('Failed to save:', error)
  } finally {
    isSubmitting.value = false
  }
}

const handlePrevious = () => store.updateStep(3)
</script>

<style scoped>
.actions-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
</style>
