<template>
  <div class="step-cloture-sans-auteur">
    <DsfrAlert type="info" title="Auteur non identifié" class="fr-mb-4w">
      L'auteur n'a pas pu être identifié. Dans cette situation, la procédure ne peut pas aboutir.
    </DsfrAlert>

    <h4 class="fr-h6 fr-mb-2w">Actions pour clôturer la procédure</h4>
    <ListeActions step-id="cloture-sans-auteur" :actions="actions" @update-case="onUpdateCase" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const actions = computed((): Action[] => [
  {
    id: 'archivage',
    label: 'Archiver le dossier',
    completed: props.suivi.dossier_archive,
  },
])

const onUpdateCase = (action: Action, val: boolean) => {
  if (action.id === 'archivage') {
    props.suivi.dossier_archive = val
  }
}
</script>

<style scoped></style>
