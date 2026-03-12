<template>
  <div class="notification">
    <p class="fr-text--sm">Envoyez la notification officielle à l'auteur présumé.</p>
    <ListeActions
      step-id="notif"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
      <template #actions>
        <div class="fr-input-group fr-mb-0">
          <label class="fr-label fr-text--xs" for="notif-date">Date de réception du pli</label>
          <input class="fr-input fr-input--sm" type="date" id="notif-date" name="notif-date" />
        </div>
        <DsfrButton label="Valider la réception" variant="secondary" size="sm" class="fr-mt-2w" />
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
    label: "Signer ou faire signer par l'autorité compétente",
    completed: false,
  },
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
