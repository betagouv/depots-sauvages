<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-2w">
    <div :class="rapportColClass">
      <div class="fr-card fr-card--download fr-card--sm">
        <div class="fr-card__body fr-px-3w">
          <div class="fr-card__content">
            <ul class="fr-btns-group fr-btns-group--full-width fr-mb-1w">
              <li>
                <DsfrButton
                  label="Télécharger le rapport de constatation"
                  :icon="{ name: 'ri-download-line', class: 'fr-mr-1w' }"
                  size="lg"
                  class="fr-py-1w"
                  @click="openUrl(docConstatUrl)"
                />
              </li>
            </ul>
            <p class="fr-card__desc fr-text--sm">
              Résumé des observations de terrain et des préjudices causés.
            </p>
            <div class="fr-card__end fr-mt-1w">
              <p class="fr-text-mention--grey fr-mb-0 fr-text--xs">
                <VIcon name="ri-folder-line" class="fr-mr-1w" scale="0.8" />
                À conserver en mairie.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="auteurIdentifie" class="fr-col-12 fr-col-md-6">
      <div class="fr-card fr-card--download fr-card--sm">
        <div class="fr-card__body fr-px-3w">
          <div class="fr-card__content">
            <ul class="fr-btns-group fr-btns-group--full-width fr-mb-1w">
              <li>
                <DsfrButton
                  label="Télécharger la lettre d'information"
                  :icon="{ name: 'ri-download-line', class: 'fr-mr-1w' }"
                  size="lg"
                  class="fr-py-1w"
                  @click="openUrl(lettreInfoUrl)"
                />
              </li>
            </ul>
            <p class="fr-card__desc fr-text--sm">
              Courrier rappelant les faits constatés et les obligations de l'auteur présumé.
            </p>
            <div class="fr-card__end fr-mt-1w">
              <p class="fr-text-mention--grey fr-mb-0 fr-text--xs">
                <VIcon name="ri-mail-send-line" class="fr-mr-1w" scale="0.8" />
                À envoyer à l'auteur présumé des faits.
              </p>
            </div>
          </div>
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
