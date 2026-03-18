<template>
  <div class="step-constatation">
    <h4 class="fr-h6 fr-mb-2w">Actions déjà réalisées</h4>
    <ListeActions step-id="constat" :actions="actions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ListeActions from './ListeActions.vue'

const props = defineProps<{
  auteurIdentifie: boolean
}>()

const actions = computed(() => [
  {
    label: 'Constater le dépôt sauvage',
    completed: true,
  },
  {
    label: 'Remplir le formulaire sur Démarches Numériques',
    completed: true,
  },
])
</script>
