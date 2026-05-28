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

    <ConstatationSuccess
      v-else-if="isSubmittedSuccessfully"
      @go-to-suivi="router.push(`/suivi-procedure/${createdConstatationId}`)"
      @go-to-procedures="router.push('/mes-procedures')"
    />

    <div v-else-if="userInfo?.is_authenticated">
      <h1 class="fr-h1 fr-mb-2w">Constatation de dépôt sauvage</h1>

      <div class="fr-mb-4w">
        <p class="fr-text--xs fr-text--mention-grey">
          Votre dossier est enregistré automatiquement après chaque modification. Vous pouvez à tout
          moment fermer la fenêtre et reprendre plus tard là où vous en étiez.
        </p>
      </div>

      <form @submit.prevent="submitForm">
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
import { nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import ConstatationForm from '../components/forms/constatation/ConstatationForm.vue'
import ConstatationSuccess from '../components/forms/constatation/ConstatationSuccess.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { useConstatationStore } from '../stores/constatation'

const router = useRouter()
const store = useConstatationStore()
const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)
const isSubmittedSuccessfully = ref(false)
const createdConstatationId = ref<number | null>(null)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      const editId = router.currentRoute.value.params.id
      if (editId) {
        const id = parseInt(editId as string, 10)
        if (!isNaN(id)) {
          await store.loadConstatation(id)
        }
      } else {
        store.resetStore()
        // The contact person fills the form and receives follow-ups.
        // He is by default the logged-in user.
        // He can also be the legal 'constatant',
        // or he can be filling the form on behalf of someone else.
        if (!store.formData.contactNom && userInfo.value.last_name) {
          store.formData.contactNom = userInfo.value.last_name
        }
        if (!store.formData.contactPrenom && userInfo.value.first_name) {
          store.formData.contactPrenom = userInfo.value.first_name
        }
        if (!store.formData.contactEmail && userInfo.value.email) {
          store.formData.contactEmail = userInfo.value.email
        }
      }
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})

watch(
  () => store.formData,
  () => {
    if (store.hasBeenSubmitted) store.validate(true)
  },
  { deep: true }
)

const scrollToFirstError = async () => {
  await nextTick()
  const firstError = document.querySelector<HTMLElement>(
    '.fr-fieldset--error, .fr-input-group--error, .fr-select-group--error, .fr-alert--error'
  )
  firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

const submitForm = async () => {
  if (!store.validate()) {
    scrollToFirstError()
    return
  }

  try {
    const data = await store.saveFormData()
    if (data && data.id) {
      createdConstatationId.value = data.id
      isSubmittedSuccessfully.value = true
    }
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
