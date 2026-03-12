<template>
  <div class="cloture">
    <p class="fr-text--sm">
      Finalisation et archivage du dossier après information du Trésor Public.
    </p>
    <ListeActions
      step-id="cloture"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
      <template #actions>
        <DsfrButton label="Confirmer le paiement" icon="ri-check-line" size="sm" />
        <DsfrButton label="Clôturer le dossier" variant="secondary" size="sm" />
      </template>
    </ListeActions>
  </div>
</template>

<script setup lang="ts">
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

const actions = reactive([
  {
    label: "Confirmer la réception du paiement de l'amende administrative",
    completed: false,
  },
  {
    label: 'Signaler le recouvrement au Trésor Public',
    completed: false,
  },
  { label: 'Clôturer officiellement le dossier', completed: false },
  { label: 'Dossier archivé en mairie', completed: false },
])
</script>
