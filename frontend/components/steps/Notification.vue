<template>
  <div class="notification">
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions
      step-id="notif"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
      <template #actions> </template>
    </ListeActions>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

const actions = reactive([
  {
    label: "Envoyer la lettre d'information en recommandé avec AR",
    completed: false,
  },
  {
    label: 'Conserver une copie de tous les documents pour vos archives',
    completed: false,
  },
  {
    label: "Réception de l'accusé de réception (point de départ du contradictoire)",
    completed: false,
  },
])
</script>
