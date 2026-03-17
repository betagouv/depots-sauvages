<template>
  <div class="judiciaire">
    <DsfrHighlight class="fr-ml-0 fr-mb-2w">
      Déposer plainte en Gendarmerie ou Police Nationale. Utilisez le document de constatation déjà rédigé pour appuyer votre dépôt.
    </DsfrHighlight>
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions
      step-id="judiciaire"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    />
  </div>
</template>

<script setup lang="ts">
import { DsfrHighlight } from '@gouvminint/vue-dsfr'
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

defineProps<{
  auteurIdentifie?: boolean
}>()

const actions = reactive([
  {
    label: 'Relire et compléter le rapport de constatation pré-rempli',
    completed: false,
  },
  {
    label: "Signer par l'autorité compétente (Maire, Adjoint, etc.)",
    completed: false,
  },
  {
    label: 'Prendre rendez-vous auprès de la gendarmerie ou du commissariat',
    completed: false,
  },
  {
    label: 'Déposer plainte et transmettre une copie du rapport',
    completed: false,
  },
])
</script>
