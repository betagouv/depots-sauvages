<template>
  <div class="cloture">
    <h4 class="fr-h6 fr-mb-2w">Étapes de clôture</h4>
    <ListeActions
      step-id="cloture"
      :actions="actions"
      @updateCase="(action, val) => (action.completed = val)"
    >
    </ListeActions>

    <DsfrHighlight class="fr-ml-0 fr-mt-4w">
      <span class="fr-icon-info-line" aria-hidden="true"></span>
      Le Trésor public se charge de la perception de l'amende. En cas d'insolvabilité de l'auteur,
      la mairie n'est évidemment pas redevable de ce montant.
    </DsfrHighlight>
  </div>
</template>

<script setup lang="ts">
import { DsfrHighlight } from '@gouvminint/vue-dsfr'
import { reactive } from 'vue'
import ListeActions from './ListeActions.vue'

const actions = reactive([
  {
    label: "S'assurer du nettoyage du dépôt par l'auteur, la mairie ou un prestataire tiers.",
    completed: false,
  },
  {
    label:
      "Dans le cas d'un amende administrative, s'assurer que le titre de recette a été émis par le Trésor Public",
    completed: false,
  },
  {
    label: "S'assurer que le montant de l'amende est recouvert par la mairie",
    completed: false,
    icon: 'fr-icon-info-line',
  },
  { label: 'Archiver le dossier', completed: false },
])
</script>
