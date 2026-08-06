<template>
  <div class="fr-container fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
      </div>
      <div v-if="userInfo?.is_authenticated && procedures.length > 0" class="fr-col-auto">
        <router-link to="/demarrer-constatation" class="fr-btn">
          <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
          Démarrer une constatation
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
              <div class="fr-card__content fr-pb-2w">
                <div class="fr-grid-row fr-grid-row--middle fr-grid-row--gutters fr-mb-1w">
                  <div class="fr-col-auto">
                    <h3 class="fr-card__title fr-mb-0">Procédure #{{ procedure.id }}</h3>
                  </div>
                  <div class="fr-col-auto">
                    <DsfrBadge
                      :type="procedure.auteur_identifie ? 'success' : 'info'"
                      :label="
                        procedure.auteur_identifie ? 'Auteur identifié' : 'Auteur non identifié'
                      "
                      class="fr-badge--no-icon"
                    />
                  </div>
                </div>
                <div class="fr-card__desc">
                  <Metadata :procedure="procedure" />
                </div>
              </div>

              <div class="fr-card__footer">
                <DsfrBadge
                  v-if="procedure.is_draft"
                  type="warning"
                  label="Brouillon de constatation"
                  class="fr-mb-2w"
                />
                <DsfrBadge
                  v-else-if="procedure.suivi_procedure?.dossier_archive"
                  type="success"
                  label="Procédure clôturée"
                  class="fr-mb-2w"
                />
                <DsfrBadge
                  v-else-if="procedure.suivi_procedure"
                  type="info"
                  :label="`Prochaine étape : ${getNextStepTitle(procedure)}`"
                  class="fr-mb-2w"
                />
                <ul class="fr-btns-group fr-btns-group--inline-lg">
                  <li>
                    <DsfrButton
                      v-if="procedure.is_draft"
                      @click="router.push(`/constatation/${procedure.id}`)"
                    >
                      <span class="fr-icon-edit-line fr-mr-1w" aria-hidden="true"></span>
                      Reprendre la constatation
                    </DsfrButton>
                    <DsfrButton v-else @click="router.push(getSuiviProcedureUrl(procedure.id))">
                      <span
                        :class="
                          procedure.suivi_procedure?.dossier_archive
                            ? 'fr-icon-eye-line'
                            : 'fr-icon-file-line'
                        "
                        class="fr-mr-1w"
                        aria-hidden="true"
                      ></span>
                      {{
                        procedure.suivi_procedure?.dossier_archive
                          ? 'Consulter la procédure'
                          : 'Continuer la procédure'
                      }}
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
import { getUserInfo, type ProcedureOverview, type UserInfo } from '../services/api'
import { getSuiviProcedureUrl } from '../services/urls'
import { getCurrentStepTitle } from '../utils/procedure-steps'

const router = useRouter()
const userInfo = ref<UserInfo | null>(null)
const procedureStore = useProcedureStore()
const showLoading = ref(true)

const procedures = computed(() => procedureStore.procedures)

const getNextStepTitle = (procedure: ProcedureOverview) =>
  getCurrentStepTitle(procedure.suivi_procedure?.etape_en_cours ?? 0, {
    auteurIdentifie: procedure.auteur_identifie,
    identificationReussie: procedure.suivi_procedure?.identification_reussie,
    decisionPoursuite: procedure.suivi_procedure?.decision_poursuite,
  })

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
