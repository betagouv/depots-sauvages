<template>
  <div class="fr-container fr-grid-row fr-grid-row--center fr-mb-4w">
    <form @submit.prevent="handleSubmit">
      <h2>Vous êtes prêts à générer vos documents</h2>
      <div>
        <p>
          Le rapport de constatation et la lettre d'information vont être créés à partir des données
          que vous avez saisies.
        </p>
        <p>
          Ces documents vous permettront d'initier la procédure administrative au niveau de la
          mairie et/ou de porter plainte.
        </p>
        <p>
          Afin de recevoir par courriel vos documents, veuillez renseigner vos coordonnées. Cela
          nous permettra également de vous recontacter dans le cadre de l'accompagnement
          personnalisé.
        </p>
        <p>
          Si vous souhaitez modifier certaines informations, vous pouvez revenir à l'étape
          précédente à tout moment.
        </p>
      </div>

      <div class="fr-form-group">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <label class="fr-label" for="nom"> Nom * </label>
            <input
              class="fr-input"
              type="text"
              id="nom"
              name="nom"
              v-model="formData.nom"
              required
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <label class="fr-label" for="prenom"> Prénom * </label>
            <input
              class="fr-input"
              type="text"
              id="prenom"
              name="prenom"
              v-model="formData.prenom"
              required
            />
          </div>
        </div>
      </div>

      <div class="fr-form-group">
        <label class="fr-label" for="email"> Adresse e-mail * </label>
        <input
          class="fr-input"
          type="email"
          id="email"
          name="email"
          v-model="formData.email"
          required
        />
      </div>

      <div class="fr-form-group">
        <label class="fr-label" for="telephone"> Numéro de téléphone * </label>
        <input
          class="fr-input"
          type="tel"
          id="telephone"
          name="telephone"
          v-model="formData.telephone"
          required
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
import { useSignalementStore } from '@/stores/signalement'
import '@/styles/form-steps.css'
import { computed, ref } from 'vue'

const store = useSignalementStore()
const isSubmitting = ref(false)

const formData = ref({
  nom: '',
  prenom: '',
  email: '',
  telephone: '',
})

const isFormValid = computed(() => {
  return (
    formData.value.nom.trim() !== '' &&
    formData.value.prenom.trim() !== '' &&
    formData.value.email.trim() !== '' &&
    formData.value.telephone.trim() !== ''
  )
})

const handleSubmit = async (event: Event) => {
  event.preventDefault()
  if (!isFormValid.value) return

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
