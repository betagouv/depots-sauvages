<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Se préparer avant sa première procédure</h1>
        <p class="fr-text fr-text--lead fr-mb-2w">
          Pas encore de dépôt sauvage à traiter ? Préparez votre collectivité dès maintenant : le
          jour où un dépôt arrive, vous saurez comment agir et qui peut le faire.
        </p>
        <p class="fr-text--sm fr-mb-2w">
          Vous avez déjà un dépôt à traiter ?
          <router-link to="/demarrer-constatation" class="fr-link fr-text--sm"
            >Démarrer une constatation</router-link
          >
        </p>
        <p v-if="userInfo?.is_authenticated" class="fr-text--bold fr-mb-0" aria-live="polite">
          {{ progressLabel }}
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <Chargement v-if="showLoading" message="Chargement..." />

      <template v-else-if="userInfo?.is_authenticated">
        <p class="fr-text--sm fr-text-mention--grey fr-mb-4w">
          Cochez chaque action une fois faite. Vos coches sont gardées sur cet ordinateur.
        </p>

        <section
          v-for="section in PREPARATION_SECTIONS"
          :key="section.id"
          :aria-labelledby="`section-${section.id}`"
          class="preparation-section fr-mb-4w fr-px-3w"
        >
          <h2 :id="`section-${section.id}`" class="fr-h5 fr-mb-0 fr-pt-3w">
            <span :class="section.icon" class="fr-mr-1w" aria-hidden="true"></span>
            {{ section.title }}
          </h2>
          <PreparationStep
            v-for="step in section.steps"
            :key="step.id"
            :step="step"
            :done="doneSteps.has(step.id)"
            @update:done="(value) => setDone(step.id, value)"
          />
          <div v-if="section.notes?.length" class="fr-callout fr-icon-information-line fr-mb-3w">
            <h3 class="fr-callout__title fr-h6">Bon à savoir</h3>
            <ul class="fr-raw-list">
              <li v-for="note in section.notes" :key="note.link.label" class="fr-mb-2w">
                <p class="fr-text--sm fr-mb-1v">{{ note.text }}</p>
                <PreparationResourceLink :link="note.link" />
              </li>
            </ul>
          </div>
        </section>

        <div v-if="allDone" class="fr-alert fr-alert--success fr-mt-6w" role="status">
          <h2 class="fr-alert__title">Votre collectivité est prête</h2>
          <p>
            Le jour où un dépôt arrive, démarrez une constatation : Stop Dépôt Sauvage génère
            automatiquement vos documents de procédure et vous guide pas à pas.
          </p>
        </div>
        <div class="fr-mt-4w">
          <router-link
            to="/demarrer-constatation"
            class="fr-btn fr-icon-add-line fr-btn--icon-left"
          >
            Démarrer une constatation
          </router-link>
        </div>
      </template>

      <LoginInvitation
        v-else
        title="Accéder aux étapes de préparation"
        description="Connectez-vous pour accéder à la liste des étapes qui vous préparent à traiter votre premier dépôt sauvage."
        redirect-to="/se-preparer"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Chargement from '@/components/procedures/Chargement.vue'
import PreparationResourceLink from '@/components/se-preparer/PreparationResourceLink.vue'
import PreparationStep from '@/components/se-preparer/PreparationStep.vue'
import LoginInvitation from '@/components/shared/LoginInvitation.vue'
import { PREPARATION_SECTIONS } from '@/constants/preparation-steps'
import { getUserInfo, type UserInfo } from '@/services/api'
import { trackEvent } from '@/services/matomo'

const STORAGE_KEY = 'se-preparer-etapes-faites'

const userInfo = ref<UserInfo | null>(null)
const showLoading = ref(true)
const doneSteps = ref<Set<string>>(new Set())

const stepIds = PREPARATION_SECTIONS.flatMap((section) => section.steps.map((step) => step.id))

// Ignores ids stored for steps that no longer exist, so the count never exceeds the total.
const doneCount = computed(() => stepIds.filter((id) => doneSteps.value.has(id)).length)
const allDone = computed(() => doneCount.value === stepIds.length)

const progressLabel = computed(() => {
  const count = doneCount.value
  return `${count} action${count > 1 ? 's' : ''} faite${count > 1 ? 's' : ''} sur ${stepIds.length}`
})

const loadDoneSteps = () => {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    doneSteps.value = new Set(Array.isArray(stored) ? stored : [])
  } catch {
    doneSteps.value = new Set()
  }
}

const setDone = (stepId: string, value: boolean) => {
  const next = new Set(doneSteps.value)
  if (value) {
    next.add(stepId)
    trackEvent('Se préparer', 'Étape cochée', stepId)
  } else {
    next.delete(stepId)
  }
  doneSteps.value = next
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...next]))
}

onMounted(async () => {
  loadDoneSteps()
  try {
    userInfo.value = await getUserInfo()
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.preparation-section {
  border: 1px solid var(--border-default-grey);
}
</style>
