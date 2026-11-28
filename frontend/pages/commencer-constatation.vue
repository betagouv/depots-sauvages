<template>
  <div>
    <div v-if="showLoading" class="fr-container fr-py-6w">
      <PageLoader />
    </div>

    <div v-else>
      <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
        <div class="fr-container">
          <h1 class="fr-h1 fr-mb-3w">Démarrer une procédure dépôt sauvage</h1>
          <p class="fr-text fr-text--lead fr-mb-0">
            Nous allons vous guider étape par étape. Pour engager une procédure, la première étape
            consiste à établir le constat du dépôt sauvage.
          </p>
        </div>
      </div>

      <div class="fr-container fr-pb-8w">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <div
              class="premium-card premium-card--small premium-card--static premium-card--align-left"
            >
              <h2 class="fr-h4">Ce dont vous avez besoin pour commencer la constatation :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list">
                <li>
                  <span
                    class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span
                    >Informations concernant le dépôt sauvage : localisation, volume estimé, types
                    de déchets, etc.</span
                  >
                </li>
                <li>
                  <span
                    class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span>Identité de la personne habilitée qui a constaté les dépôts sauvages</span>
                </li>
                <li>
                  <span
                    class="fr-icon-checkbox-circle-line fr-text-default--success fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span>Informations sur l'auteur présumé (si connues)</span>
                </li>
                <li>
                  <span
                    class="fr-icon-time-line fr-text-default--info fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span>Temps estimé : 7 minutes</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <div
              class="premium-card premium-card--small premium-card--static premium-card--align-left"
            >
              <h2 class="fr-h4">À l'issue de cette étape :</h2>
              <ul class="fr-text--sm fr-mb-0 premium-choices-list">
                <li>
                  <span
                    class="fr-icon-file-text-line fr-text-default--info fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span>Rapport de constatation généré automatiquement</span>
                </li>
                <li>
                  <span
                    class="fr-icon-file-text-line fr-text-default--info fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span
                    >Lettre d'information prête à être envoyée (si l'auteur présumé est
                    identifié)</span
                  >
                </li>
                <li>
                  <span
                    class="fr-icon-arrow-right-line fr-text-default--info fr-mr-1w"
                    aria-hidden="true"
                  ></span>
                  <span
                    >Vous serez guidé étape par étape pour faire avancer la procédure adaptée à
                    votre situation</span
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="constatation-actions">
          <template v-if="userInfo?.is_authenticated">
            <!-- Action principale toujours prioritaire -->
            <div class="premium-text-center">
              <router-link
                to="/constatation"
                class="fr-btn fr-btn--lg"
                title="Démarrer une nouvelle constatation"
              >
                Démarrer une nouvelle constatation
              </router-link>
            </div>

            <!-- Si un seul brouillon personnel en cours -->
            <PremiumCallout
              v-if="userDrafts.length === 1"
              type="banner"
              title="Vous avez une constatation en cours de rédaction"
              :description="formatDraftDescription(userDrafts[0])"
              iconClass="fr-icon-edit-line"
              buttonText="Reprendre le brouillon"
              :buttonTo="`/constatation/${userDrafts[0].id}`"
              buttonVariant="secondary"
              class="fr-mb-2w"
            />

            <!-- Si plusieurs brouillons personnels en cours -->
            <div
              v-else-if="userDrafts.length > 1"
              class="fr-notice fr-notice--info drafts-notice"
            >
              <div class="fr-container">
                <div class="fr-notice__body">
                  <div class="drafts-section-header fr-mb-2w">
                    <p class="fr-notice__title fr-text--bold fr-mb-1v">
                      <span class="fr-icon-edit-line fr-mr-1v" aria-hidden="true"></span>
                      Vous avez {{ userDrafts.length }} constatations en cours de rédaction
                    </p>
                    <p class="fr-text--sm fr-mb-0 fr-text-mention--grey">
                      Vous pouvez reprendre l'un de vos brouillons personnels ci-dessous ou démarrer une nouvelle procédure.
                    </p>
                  </div>
                  <ul class="drafts-list fr-p-0 fr-m-0">
                    <li
                      v-for="draft in userDrafts"
                      :key="draft.id"
                      class="draft-item fr-p-2w fr-mb-2v"
                    >
                      <div class="draft-info">
                        <span class="fr-badge fr-badge--sm fr-badge--info fr-mr-1w">Brouillon n°{{ draft.id }}</span>
                        <span class="draft-location fr-text--bold fr-text--sm">
                          {{ draft.localisation_depot || 'Commune non renseignée' }}
                        </span>
                        <span v-if="draft.date_constat" class="draft-date fr-text--xs fr-text-mention--grey fr-ml-1w">
                          · Constat du {{ formatDate(draft.date_constat) }}
                        </span>
                      </div>
                      <router-link
                        :to="`/constatation/${draft.id}`"
                        class="fr-btn fr-btn--sm fr-btn--secondary"
                        :title="`Reprendre le brouillon n°${draft.id}`"
                      >
                        Reprendre
                      </router-link>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <PremiumCallout
              type="banner"
              title="Vous avez un doute ?"
              description="Vous ne savez pas si votre situation permet d'engager une procédure ?"
              iconClass="fr-icon-question-line"
              buttonText="Vérifier ma situation en 2 min"
              buttonTo="/demarrer-constatation/simulateur"
            />
          </template>

          <template v-else>
            <PremiumCallout
              type="banner"
              title="Vous avez un doute ?"
              description="Vous ne savez pas si votre situation permet d'engager une procédure ?"
              iconClass="fr-icon-question-line"
              buttonText="Vérifier ma situation en 2 min"
              buttonTo="/demarrer-constatation/simulateur"
            />

            <LoginInvitation
              title="Connectez-vous pour démarrer la constatation"
              description="Pour initier une procédure et accéder au formulaire de constatation de dépôt sauvage, vous devez vous connecter avec ProConnect."
              redirectTo="/constatation"
            />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import PageLoader from '../components/shared/PageLoader.vue'
import PremiumCallout from '../components/shared/PremiumCallout.vue'
import { useTallyRoutes } from '../composables/useTally'
import {
  getUserInfo,
  getUserProcedures,
  type ProcedureOverview,
  type UserInfo,
} from '../services/api'

const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)
const userProcedures = ref<ProcedureOverview[]>([])

// Filtrage strict : seuls les brouillons personnels (créés par l'utilisateur connecté)
const userDrafts = computed(() => {
  return userProcedures.value.filter((p) => p.is_draft)
})

const formatDraftDescription = (draft: ProcedureOverview) => {
  if (draft.localisation_depot) {
    return `Un brouillon a été sauvegardé pour « ${draft.localisation_depot} » (n°${draft.id}).`
  }
  return `Un brouillon sans adresse renseignée est enregistré (n°${draft.id}).`
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('fr-FR')
  } catch {
    return dateStr
  }
}

useTallyRoutes({
  '/demarrer-constatation/simulateur': {
    formId: 'A7xA8z',
    options: { layout: 'modal', width: 900 },
    returnPath: '/demarrer-constatation',
  },
})

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      userProcedures.value = await getUserProcedures()
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.premium-card--align-left {
  align-items: flex-start;
  text-align: left;
}

.premium-choices-list {
  padding-left: 0;
  list-style-type: none;
}

.premium-choices-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.premium-choices-list li:last-child {
  margin-bottom: 0;
}

.premium-choices-list li span:first-child {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.constatation-actions {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  margin-top: 3rem;
}

.constatation-actions :deep(.premium-alert-banner) {
  margin: 0 !important;
}

.constatation-actions :deep(.premium-block-container) {
  padding-top: 0 !important;
}

.drafts-notice {
  background-color: var(--background-alt-blue-france, #f5f5fe);
  border-left: 4px solid var(--border-plain-blue-france, #000091);
  border-radius: 4px;
}

.drafts-list {
  list-style: none;
}

.draft-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--background-default-grey, #fff);
  border: 1px solid var(--border-default-grey, #e5e5e5);
  border-radius: 4px;
  gap: 1rem;
}

.draft-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
</style>
