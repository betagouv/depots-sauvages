<template>
  <div class="cloture">
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions
      step-id="cloture"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
    </ListeActions>
  </div>
</template>

<script setup lang="ts">
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
