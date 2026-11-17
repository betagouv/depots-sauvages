<template>
  <div class="preparation-step fr-py-3w">
    <DsfrCheckbox
      :id="`etape-${step.id}`"
      :name="`etape-${step.id}`"
      :label="step.label"
      :model-value="done"
      @update:model-value="(value: boolean) => emit('update:done', value)"
    />
    <div class="preparation-step__content">
      <p v-if="step.description" class="fr-text--sm fr-mt-1w fr-mb-1w">{{ step.description }}</p>
      <ul v-if="step.links.length || step.upcoming?.length" class="fr-raw-list fr-mt-1w">
        <li v-for="link in step.links" :key="link.label" class="fr-mb-1v">
          <button
            v-if="link.action === 'simulator'"
            type="button"
            class="fr-btn fr-btn--secondary fr-btn--sm fr-btn--icon-left fr-icon-question-line"
            @click="openSimulator(link.label)"
          >
            {{ link.label }}
          </button>
          <a
            v-else-if="link.href"
            :href="link.href"
            target="_blank"
            rel="noopener noreferrer"
            class="fr-link fr-text--sm"
            @click="trackResource(link.label)"
          >
            {{ link.label }}
            <span class="fr-sr-only">(nouvelle fenêtre)</span>
          </a>
          <router-link
            v-else-if="link.to"
            :to="link.to"
            class="fr-link fr-text--sm fr-icon-arrow-right-line fr-link--icon-right"
            @click="trackResource(link.label)"
          >
            {{ link.label }}
          </router-link>
        </li>
        <li v-for="label in step.upcoming" :key="label" class="fr-mb-1v">
          <span class="fr-text--sm fr-text-mention--grey">{{ label }}</span>
          <DsfrBadge label="Bientôt disponible" small no-icon class="fr-ml-1w" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrBadge, DsfrCheckbox } from '@gouvminint/vue-dsfr'
import type { PreparationStep } from '@/constants/preparation-steps'
import { trackEvent } from '@/services/matomo'
import { openTallyPopup } from '@/utils/tally'

defineProps<{
  step: PreparationStep
  done: boolean
}>()

const emit = defineEmits<{
  'update:done': [value: boolean]
}>()

const trackResource = (label: string) => trackEvent('Se préparer', 'Clic ressource', label)

const openSimulator = (label: string) => {
  trackResource(label)
  openTallyPopup('A7xA8z', { layout: 'modal', width: 900 })
}
</script>

<style scoped>
.preparation-step + .preparation-step {
  border-top: 1px solid var(--border-default-grey);
}
/* Aligns the description and links with the checkbox label rather than the box. */
.preparation-step__content {
  padding-left: 2rem;
}
</style>
