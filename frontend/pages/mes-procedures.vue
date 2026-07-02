<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
      </div>
      <div v-if="userInfo?.is_authenticated && procedures.length > 0" class="fr-col-auto">
        <router-link to="/demarrer-constatation" class="fr-btn">
          <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
          Démarrer une nouvelle constatation
        </router-link>
      </div>
    </div>

    <Chargement v-if="showLoading" message="Récupération de vos procédures..." />

    <div v-else-if="userInfo?.is_authenticated">
      <div v-if="userInfo && userInfo.is_authenticated" class="fr-mb-4w">
        <p v-if="userInfo.first_name && userInfo.last_name" class="fr-text--lead">
          Utilisateur connecté :
          <strong>{{ userInfo.first_name }} {{ userInfo.last_name }}</strong>
          <span v-if="userInfo.email"> - {{ userInfo.email }}</span>
        </p>
      </div>

      <div v-if="procedures.length > 0" class="fr-mb-2w">
        <p class="fr-text--bold">
          {{ procedures.length }} procédure{{ procedures.length > 1 ? 's' : '' }}
        </p>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-for="procedure in procedures" :key="procedure.id" class="fr-col-12">
          <div class="fr-card fr-card--no-arrow shadow-card">
            <div class="fr-card__body">
              <div class="fr-card__content">
                <h3 class="fr-card__title">Procédure #{{ procedure.id }}</h3>
                <div class="fr-card__desc">
                  <Metadata :procedure="procedure" class="fr-mb-2w" />
                  <StepperTimeline
                    v-if="procedure.suivi_procedure"
                    :current-step="procedure.suivi_procedure.etape_en_cours"
                  />
                </div>
              </div>

              <div class="fr-card__footer">
                <ul class="fr-btns-group fr-btns-group--inline-lg">
                  <li>
                    <DsfrButton
                      @click="router.push(getSuiviProcedureUrl(procedure.numero_dossier))"
                    >
                      <span class="fr-icon-file-line fr-mr-1w" aria-hidden="true"></span>
                      Suivre la procédure
                    </DsfrButton>
                  </li>
                  <li>
                    <DsfrButton
                      secondary
                      @click="router.push(`/constatation/${procedure.numero_dossier}`)"
                    >
                      <span class="fr-icon-edit-line fr-mr-1w" aria-hidden="true"></span>
                      Modifier la constatation
                    </DsfrButton>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <AucuneProcedureBox
        v-if="procedures.length === 0 && userInfo?.is_authenticated"
        class="fr-mt-5w"
      />
    </div>
    <LoginInvitation v-else />
  </div>
</template>

<script setup lang="ts">
import { useProcedureStore } from '@/stores/procedure'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import AucuneProcedureBox from '../components/procedures/AucuneProcedureBox.vue'
import Chargement from '../components/procedures/Chargement.vue'
import Metadata from '../components/procedures/Metadata.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import StepperTimeline from '../components/StepperTimeline.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { getSuiviProcedureUrl } from '../services/urls'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const procedureStore = useProcedureStore()
const showLoading = ref(true)

const procedures = computed(() => procedureStore.procedures)

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      await procedureStore.fetchProcedures(true)
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.shadow-card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e5e5;
}
</style>
