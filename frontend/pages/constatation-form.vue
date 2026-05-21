<template>
  <div class="fr-container fr-py-6w">
    <div v-if="showLoading" class="fr-grid-row fr-grid-row--center fr-my-8w">
      <div class="fr-col-12 fr-col-md-6 text-center">
        <span
          class="fr-icon-refresh-line fr-icon--lg"
          aria-hidden="true"
          style="animation: spin 1s linear infinite"
        ></span>
        <p class="fr-mt-2w">Chargement de la page...</p>
      </div>
    </div>

    <div v-else-if="userInfo?.is_authenticated">
      <h1 class="fr-h1 fr-mb-2w">Constatation d'un dépôt sauvage</h1>

      <div class="fr-mb-4w">
        <p class="fr-text--xs fr-text--mention-grey">
          Votre dossier est enregistré automatiquement après chaque modification. Vous pouvez à tout
          moment fermer la fenêtre et reprendre plus tard là où vous en étiez.
        </p>
      </div>

      <form @submit.prevent="submitForm">
        <DsfrAlert
          v-if="store.hasBeenSubmitted && Object.keys(store.errors).length > 0"
          type="error"
          title="Le formulaire contient des erreurs"
          class="fr-mb-4w"
        >
          Veuillez corriger les champs indiquant une erreur avant de soumettre le formulaire.
        </DsfrAlert>

        <ConstatationForm />
      </form>
    </div>

    <LoginInvitation
      v-else
      title="Connectez-vous pour démarrer"
      description="Pour initier une procédure et accéder au formulaire de constatation, vous devez vous connecter avec ProConnect."
      redirectTo="/constatation"
    />
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert } from '@gouvminint/vue-dsfr'
import { nextTick, onMounted, ref, watch } from 'vue'
import ConstatationForm from '../components/forms/constatation/ConstatationForm.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { useConstatationStore } from '../stores/constatation'

const store = useConstatationStore()
const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})

watch(
  () => store.formData,
  () => {
    if (store.hasBeenSubmitted) store.validate()
  },
  { deep: true },
)

const scrollToFirstError = async () => {
  await nextTick()
  const firstError = document.querySelector<HTMLElement>(
    '.fr-fieldset--error, .fr-input-group--error, .fr-select-group--error, .fr-alert--error',
  )
  firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

const submitForm = async () => {
  if (!store.validate()) {
    scrollToFirstError()
    return
  }

  try {
    await store.saveFormData()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.text-center {
  text-align: center;
}
</style>
