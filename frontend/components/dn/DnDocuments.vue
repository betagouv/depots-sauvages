<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-2w">
    <div :class="rapportColClass">
      <DsfrCard
        title="Rapport de constatation"
        description="Résumé des observations de terrain et des préjudices causés."
        :buttons="[
          {
            label: 'Télécharger',
            icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
            onClick: () => openUrl(docConstatUrl),
          },
        ]"
        no-arrow
        size="large"
        title-tag="h2"
      >
        <template #end-details>
          <p class="fr-text-mention--grey">
            <VIcon name="ri-folder-line" class="fr-mr-1w" />
            À conserver en mairie.
          </p>
        </template>
      </DsfrCard>
    </div>
    <div v-if="auteurIdentifie" class="fr-col-12 fr-col-md-6">
      <DsfrCard
        title="Lettre d'information"
        description="Courrier rappelant les faits constatés et les obligations de l'auteur du responsable probable du dépôt sauvage."
        :buttons="[
          {
            label: 'Télécharger',
            icon: { name: 'ri-download-line', scale: 1.5, class: 'fr-mr-1w' },
            onClick: () => openUrl(lettreInfoUrl),
          },
        ]"
        no-arrow
        size="large"
        title-tag="h2"
      >
        <template #end-details>
          <p class="fr-text-mention--grey">
            <VIcon name="ri-mail-send-line" class="fr-mr-1w" />
            À envoyer à l'auteur probable des faits.
          </p>
        </template>
      </DsfrCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'
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

<style scoped>
:deep(.fr-card__content) {
  padding-bottom: 0;
}
</style>
