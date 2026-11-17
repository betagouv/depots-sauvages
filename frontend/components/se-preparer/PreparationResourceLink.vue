<template>
  <div>
    <button
      v-if="link.action === 'simulator'"
      type="button"
      class="fr-btn fr-btn--secondary fr-btn--sm fr-btn--icon-left fr-icon-question-line"
      @click="openSimulator"
    >
      {{ link.label }}
    </button>
    <a
      v-else-if="link.href"
      :href="link.href"
      target="_blank"
      rel="noopener noreferrer"
      class="fr-link fr-text--sm"
      @click="track"
    >
      {{ link.label }}
      <span class="fr-sr-only">(nouvelle fenêtre)</span>
    </a>
    <router-link
      v-else-if="link.to"
      :to="link.to"
      class="fr-link fr-text--sm fr-icon-arrow-right-line fr-link--icon-right"
      @click="track"
    >
      {{ link.label }}
    </router-link>
  </div>
</template>

<script setup lang="ts">
import type { PreparationLink } from '@/constants/preparation-steps'
import { trackEvent } from '@/services/matomo'
import { openTallyPopup } from '@/utils/tally'

const props = defineProps<{
  link: PreparationLink
}>()

const track = () => trackEvent('Se préparer', 'Clic ressource', props.link.label)

const openSimulator = () => {
  track()
  openTallyPopup('A7xA8z', { layout: 'modal', width: 900 })
}
</script>
