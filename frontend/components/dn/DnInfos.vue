<template>
  <div v-if="dnNumeroDossier" class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-6">
      <div class="fr-card fr-card--lg">
        <div class="fr-card__body">
          <h2 class="fr-card__title">Informations du dossier</h2>
          <div class="fr-card__desc">
            <p><strong>Numéro de dossier:</strong> {{ dnNumeroDossier }}</p>
            <p v-if="dnDateCreation">
              <strong>Date de création:</strong> {{ formatDate(dnDateCreation) }}
            </p>
            <p v-if="dnDateModification">
              <strong>Dernière modification dossier:</strong>
              {{ formatDate(dnDateModification) }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="fr-col-12 fr-col-md-6">
      <DsfrCard
        title="Modifier votre dossier"
        description="Si vous avez besoin de modifier les informations, merci de modifier votre dossier sur votre démarche numérique."
        :buttons="[
          {
            label: 'Consulter ou modifier',
            icon: { name: 'ri-external-link-line', scale: 1.5, class: 'fr-mr-1w' },
            secondary: true,
            onClick: openModifyUrl,
          },
        ]"
        size="large"
        no-arrow
        title-tag="h2"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const props = defineProps<{
  dnNumeroDossier: number
  dnDateCreation?: string | null
  dnDateModification?: string | null
  modifyUrl: string
}>()

const openModifyUrl = () => {
  if (props.modifyUrl) {
    window.open(props.modifyUrl, '_blank', 'noopener,noreferrer')
  }
}

const formatDate = (dateString?: string | null) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
