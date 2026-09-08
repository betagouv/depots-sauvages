<template>
  <section class="fr-mt-6w" :aria-labelledby="legendId">
    <div class="fr-callout fr-callout--blue-cumulus">
      <div v-if="!answer">
        <fieldset class="fr-fieldset fr-mb-0" :aria-labelledby="legendId">
          <legend :id="legendId" class="fr-fieldset__legend fr-text--regular fr-mb-2w">
            <span class="fr-h6 fr-mb-0">
              Ces informations vous ont-elles permis de comprendre la procédure&nbsp;?
            </span>
          </legend>
          <div class="fr-fieldset__element">
            <ul class="fr-btns-group fr-btns-group--inline-md fr-btns-group--sm">
              <li v-for="choice in choices" :key="choice.value">
                <button
                  type="button"
                  class="fr-btn fr-btn--secondary"
                  @click="submit(choice.value)"
                >
                  {{ choice.label }}
                </button>
              </li>
            </ul>
          </div>
        </fieldset>
      </div>

      <div v-else role="status">
        <p class="fr-text fr-mb-0">
          <span
            class="fr-icon-check-line fr-mr-1w fr-text-default--success"
            aria-hidden="true"
          ></span>
          Merci, votre retour est enregistré.
        </p>
        <div v-if="answer !== 'Oui'" class="fr-mt-2w">
          <p class="fr-text fr-mb-1w">Nous pouvons vous aider à aller plus loin&nbsp;:</p>
          <ul class="fr-btns-group fr-btns-group--inline-md fr-btns-group--sm fr-mb-0">
            <li>
              <router-link to="/rdv" class="fr-btn fr-btn--sm" @click="trackRecovery('Webinaire')">
                M'inscrire au webinaire
              </router-link>
            </li>
            <li>
              <router-link
                to="/contact"
                class="fr-btn fr-btn--sm fr-btn--secondary"
                @click="trackRecovery('Contact')"
              >
                Poser une question à l'équipe
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { trackEvent } from '@/services/matomo'
import { ref, useId } from 'vue'

const props = withDefaults(
  defineProps<{
    /** Page label sent to Matomo, e.g. 'Comprendre la procédure'. */
    pageName: string
    category?: string
  }>(),
  { category: 'Parcours information' }
)

const legendId = `clarte-question-${useId()}`

const choices = [
  { value: 'Oui', label: 'Oui, c’est clair' },
  { value: 'En partie', label: 'En partie' },
  { value: 'Non', label: 'Non' },
] as const

const answer = ref<string | null>(null)

const submit = (value: string) => {
  answer.value = value
  trackEvent(props.category, `Clarté - ${value}`, props.pageName)
}

const trackRecovery = (destination: string) => {
  trackEvent(props.category, `Clarté - Rebond ${destination}`, props.pageName)
}
</script>
