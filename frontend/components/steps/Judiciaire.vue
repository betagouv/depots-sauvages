<template>
  <div class="judiciaire">
    <p class="fr-text--sm">Procédure optionnelle en cas d'échec de la procédure administrative.</p>
    <DsfrAlert
      type="info"
      title="Note"
      description="Déposer plainte en Gendarmerie ou Police Nationale. Utilisez le document de constatation déjà rédigé pour appuyer votre dépôt."
      small
      class="fr-mb-2w"
    />
    <ListeActions
      step-id="judiciaire"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    />
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert } from '@gouvminint/vue-dsfr'
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

const actions = reactive([
  {
    label: 'Relire et compléter le rapport de constatation pré-rempli',
    completed: false,
    icon: 'ri-file-edit-line',
  },
  {
    label: "Signer par l'autorité compétente (Maire, Adjoint, etc.)",
    completed: false,
    icon: 'ri-pen-nib-line',
  },
  {
    label: 'Prendre rendez-vous auprès de la gendarmerie ou du commissariat',
    completed: false,
    icon: 'ri-calendar-event-line',
  },
  {
    label: 'Déposer plainte et transmettre une copie du rapport',
    completed: false,
    icon: 'ri-police-car-line',
  },
])
</script>
