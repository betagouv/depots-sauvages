<template>
  <div class="step-suivi">
    <p class="fr-text--sm">Gérez les suites de la mise en demeure et déterminez les sanctions.</p>
    <ListeActions
      step-id="suivi"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
      <template #actions>
        <!-- Boutons retirés pour l'instant :
        <DsfrButton label="Rédiger l'arrêté" icon="ri-edit-line" size="sm" />
        <DsfrButton label="Notifier la sanction" variant="secondary" size="sm" />-->
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
