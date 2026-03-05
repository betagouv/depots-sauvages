<template>
  <div class="constatation">
    <p class="fr-text--sm">
      Remplissez le dossier de procédure administrative et rassemblez les preuves.
    </p>
    <ListeActions
      step-id="constat"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
      <template #actions>
        <DsfrButton label="Générer les documents" icon="ri-file-list-3-line" />
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
    label: "Numériser et conserver les éléments d'identification de l'auteur",
    completed: false,
    icon: 'ri-scan-line',
  },
  {
    label: 'Prendre et conserver les photos du constat sur le terrain',
    completed: false,
    icon: 'ri-camera-line',
  },
  {
    label: 'Relire et compléter les documents pré-remplis (charte mairie, date, signature)',
    completed: false,
    icon: 'ri-file-edit-line',
  },
  {
    label: "Faire signer par l'autorité compétente (Maire ou Adjoint)",
    completed: false,
    icon: 'ri-pen-nib-line',
  },
])
</script>
