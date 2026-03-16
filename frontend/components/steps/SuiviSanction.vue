<template>
  <div class="step-suivi">
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions
      step-id="suivi"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    />
  </div>
</template>

<script setup lang="ts">
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

const actions = reactive([
  {
    label: 'La période du contradictoire (10 jours minimum) est écoulée',
    completed: false,
  },
  {
    label: "Analyser les éventuelles observations de l'auteur",
    completed: false,
  },
  {
    label: "Déterminer le montant de l'amende administrative (jusqu'à 15 000 €)",
    completed: false,
  },
  {
    label: "Rédiger l'arrêté de sanction administrative",
    completed: false,
  },
])
</script>
