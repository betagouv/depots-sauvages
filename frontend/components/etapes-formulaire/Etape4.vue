<template>
  <div class="fr-container--sm">
    <div class="fr-bg--contrast">
      <div class="fr-p-4w">
        <form @submit.prevent="handleSubmit">
          <!-- Section 1 -->
          <section class="highlighted-section fr-py-3w fr-px-2w fr-mb-4w">
            <h2 class="fr-h3 highlighted-title fr-mb-1w">Vos informations de contact</h2>
            <p class="fr-mb-2w">
              Afin de vous identifier et pour recevoir vos documents par mail (Rapport de
              constatation et lettre d'information) vous devez renseigner vos coordonnées.
            </p>
            <p class="fr-text--sm fr-mb-3w">
              Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires
            </p>

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
          </section>

          <!-- Section 2 -->
          <section class="highlighted-section fr-py-3w fr-px-2w fr-mb-4w">
            <h2 class="fr-h3 highlighted-title fr-mb-1w">
              Accompagnement personnalisé (optionnel)
            </h2>
            <p class="fr-mb-3w">
              Vous pouvez choisir de bénéficier d'un accompagnement personnalisé. Dans ce cas, nous
              pourrons vous recontacter pour vous aider dans vos procédures.
            </p>

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

            <div v-if="store.formData.accepteAccompagnement" class="fr-form-group fr-mt-3w">
              <label class="fr-label" for="telephone"> Numéro de téléphone (facultatif) </label>
              <input
                class="fr-input"
                type="tel"
                id="telephone"
                name="telephone"
                v-model="store.formData.contactTelephone"
              />
            </div>
          </section>

          <!-- Informations sur les données personnelles -->
          <section class="fr-py-2w fr-px-2w fr-mb-4w">
            <h4 class="fr-h5 fr-mb-1w">Protection des données personnelles</h4>
            <p class="fr-text--sm fr-mb-2w">
              Les informations saisies dans ce formulaire sont uniquement utilisées pour :
            </p>
            <ul class="fr-text--sm fr-mb-2w">
              <li>
                Vous identifier et vous transmettre les documents demandés (rapport et lettre
                d'information)
              </li>
              <li>
                Échanger avec vous et assurer le suivi de votre demande si vous avez accepté un
                accompagnement personnalisé
              </li>
            </ul>
            <p class="fr-text--sm">
              Vos données seront conservées pendant 18 mois puis supprimées. Vous pouvez à tout
              moment réclamer la modification ou la suppression de ces données conformément à notre
              politique de confidentialité.
            </p>
          </section>

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
    </div>
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
  isSubmitting.value = true

  if (!isFormValid.value) {
    isSubmitting.value = false
    return
  }

  try {
    await store.saveFormData()

    store.sendContactPersonEmail().catch((emailError) => {
      console.error('Contact email sending failed:', emailError)
    })

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

.highlighted-section {
  background-color: #f5f5fe;
}

.highlighted-title {
  color: #000091;
}
</style>
