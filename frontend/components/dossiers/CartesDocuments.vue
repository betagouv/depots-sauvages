<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-2w">
    <div :class="rapportColClass">
      <div class="fr-card fr-card--download fr-card--sm">
        <div class="fr-card__body fr-p-4w">
          <ul class="fr-btns-group fr-btns-group--full-width fr-mb-4w">
            <li>
              <DsfrButton
                label="Télécharger le rapport de constatation"
                :icon="{ name: 'ri-download-line', class: 'fr-mr-1w' }"
                size="lg"
                @click="openUrl(docConstatUrl)"
              />
            </li>
          </ul>

          <p class="fr-text-mention--grey fr-mb-0">
            <VIcon name="ri-folder-line" class="fr-mr-1w" />
            À conserver en mairie.
          </p>
        </div>
      </div>
    </div>

    <div v-if="auteurIdentifie" class="fr-col-12 fr-col-md-6">
      <div class="fr-card fr-card--download fr-card--sm">
        <div class="fr-card__body fr-p-4w">
          <ul class="fr-btns-group fr-btns-group--full-width fr-mb-4w">
            <li>
              <DsfrButton
                label="Télécharger la lettre d'information"
                :icon="{ name: 'ri-download-line', class: 'fr-mr-1w' }"
                size="lg"
                @click="openUrl(lettreInfoUrl)"
              />
            </li>
          </ul>

          <p class="fr-text-mention--grey fr-mb-0">
            <VIcon name="ri-mail-send-line" class="fr-mr-1w" />
            À envoyer à l'auteur présumé des faits.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const props = defineProps<{
  auteurIdentifie: boolean
  docConstatUrl: string
  lettreInfoUrl: string
}>()

const rapportColClass = computed(() =>
  props.auteurIdentifie ? 'fr-col-12 fr-col-md-6' : 'fr-col-12 fr-col-lg-12'
)

const openUrl = (url: string) => {
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}
</script>

<style scoped></style>
