<template>
  <div class="fr-container fr-py-6w">
    <PageLoader v-if="showLoading" />

    <ConstatationSuccess
      v-else-if="userInfo?.is_authenticated"
      @go-to-suivi="router.push(`/suivi-procedure/${constatationId}`)"
      @go-to-procedures="router.push('/mes-procedures')"
    />

    <LoginInvitation
      v-else
      title="Connectez-vous pour accéder au suivi"
      description="Pour accéder à vos procédures de constatation, vous devez vous connecter avec ProConnect."
      :redirectTo="`/constatation-fin/${constatationId}`"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import ConstatationSuccess from '../components/forms/constatation/ConstatationSuccess.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import PageLoader from '../components/shared/PageLoader.vue'
import { getUserInfo, type UserInfo } from '../services/api'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)
const constatationId = ref<number | null>(null)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    const idParam = router.currentRoute.value.params.id
    if (idParam) {
      const id = parseInt(idParam as string, 10)
      if (!isNaN(id)) {
        constatationId.value = id
      }
    }
  } catch (error) {
    console.error('Failed to load user info:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
</style>
