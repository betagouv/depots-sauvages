<template>
  <div class="fr-container fr-grid-row fr-grid-row--center fr-mb-4w">
    <form @submit.prevent="handleSubmit">
      <div>
        <p>
          Vous êtes prêt à générer vos documents. Le rapport de constatation et la lettre
          d'information vont être créés à partir des données que vous avez saisies. Ces documents
          vous permettront d'initier la procédure administrative au niveau de la mairie et/ou de
          porter plainte. Si vous souhaitez modifier certaines informations, vous pouvez revenir à
          l'étape précédente à tout moment.
        </p>
      </div>

      <div class="fr-form-group">
        <h3 class="fr-h5">Identification et contact</h3>
        <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>

        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <label class="fr-label" for="nom"> Nom * </label>
            <input
              class="fr-input"
              type="text"
              id="nom"
              name="nom"
              v-model="store.formData.contactNom"
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
              v-model="store.formData.contactPrenom"
              required
            />
          </div>
        </div>

        <div class="fr-form-group">
          <label class="fr-label" for="email"> Adresse e-mail * </label>
          <input
            class="fr-input"
            type="email"
            id="email"
            name="email"
            v-model="store.formData.contactEmail"
            required
          />
          <p class="fr-hint-text">
            Format attendu : nom@domaine.fr (Vos documents seront envoyés à cette adresse.)
          </p>
        </div>
      </div>

      <div class="fr-form-group">
        <h3 class="fr-h5">Accompagnement personnalisé (optionnel)</h3>
        <p>
          Vous pouvez également choisir de bénéficier d'un accompagnement personnalisé. Dans ce cas,
          nous pourrons vous recontacter.
        </p>

        <div class="fr-form-group">
          <label class="fr-label" for="telephone"> Numéro de téléphone (facultatif) </label>
          <input
            class="fr-input"
            type="tel"
            id="telephone"
            name="telephone"
            v-model="store.formData.contactTelephone"
          />
        </div>

        <div class="fr-checkbox-group">
          <input
            type="checkbox"
            id="accompagnement"
            name="accompagnement"
            v-model="store.formData.accepteAccompagnement"
          />
          <label class="fr-label fr-mt-2w" for="accompagnement">
            J'accepte d'être recontacté(e) par téléphone ou par e-mail dans le cadre d'un
            accompagnement personnalisé.
          </label>
        </div>

        <p class="fr-text--sm fr-mt-2w">
          Les informations saisies dans ce formulaire sont uniquement utilisées pour:<br />
          - Vous transmettre les documents demandés (rapport et lettre d'information)<br />
          - Échanger avec vous et assurer le suivi de votre demande si vous avez accepté un
          accompagnement personnalisé.<br />
          Vos données seront conservées pendant [durée à définir] puis supprimées. Vous pouvez à
          tout moment réclamer la modification ou la suppression de ces données conformément à notre
          politique de confidentialité.
        </p>
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

const isFormValid = computed(() => {
  return (
    store.formData.contactNom.trim() !== '' &&
    store.formData.contactPrenom.trim() !== '' &&
    store.formData.contactEmail.trim() !== ''
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
