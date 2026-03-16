<template>
  <div class="step-constatation">
    <h4 class="fr-h6 fr-mb-2w">Actions déjà réalisées</h4>
    <ListeActions
      step-id="constat"
      :actions="actions"
    />
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
    label: "Constat du dépôt sauvage",
    completed: true,
  },
  {
    label: props.auteurIdentifie 
      ? "Identification de l'auteur des faits" 
      : "Recherche d'éléments d'identification de l'auteur",
    completed: true,
  },
  {
    label: "Récupération de l'identité complète sur Démarche Numérique",
    completed: true,
  },
  {
    label: "Remplissage du formulaire de la procédure administrative sur Démarches Numériques",
    completed: true,
  }
])
</script>
