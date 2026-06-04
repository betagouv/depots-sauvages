<template>
  <div class="fr-container fr-py-6w">
    <PageLoader v-if="showLoading" />

    <div v-else-if="userInfo?.is_authenticated">
      <h1 class="fr-h1 fr-mb-2w">Constatation de dépôt sauvage</h1>

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
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import PageLoader from '../components/shared/PageLoader.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { useConstatationStore } from '../stores/constatation'

import camelcaseKeys from 'camelcase-keys'

const router = useRouter()
const store = useConstatationStore()
const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)

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
      }

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
      router.push(`/constatation-fin/${data.id}`)
    }
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    if (error && typeof error === 'object') {
      const camelErrors = camelcaseKeys(error as Record<string, any>)
      for (const [key, val] of Object.entries(camelErrors)) {
        if (Array.isArray(val) && val.length > 0) {
          store.errors[key] = val[0]
        } else if (typeof val === 'string') {
          store.errors[key] = val
        }
      }
      scrollToFirstError()
    }
  }
}
</script>

<style scoped>
</style>
