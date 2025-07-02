<template>
  <div class="fr-container fr-grid-row fr-grid-row--center fr-mb-4w">
    <form @submit.prevent="handleSubmit">
      <h2>Vous êtes prêts à générer vos documents</h2>
      <div>
        <p>Le rapport de constatation et la lettre d’information vont être créés à partir des données que vous avez saisies. </p>
        <p>Ces documents vous permettront de signaler officiellement le dépôt sauvage auprès des autorités compétentes. </p>
        <p>Après génération, vous pourrez télécharger ces documents ou les recevoir par e-mail.</p>
        <p>Si vous souhaitez modifier certaines informations, vous pouvez revenir à l’étape précédente à tout moment.</p>
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
          label="Générer les documents"
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
