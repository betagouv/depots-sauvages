<template>
  <div class="cloture">
    <h4 class="fr-h6 fr-mb-2w">Actions pour clôturer la procédure</h4>
    <ListeActions step-id="cloture" :actions="actions" @update-case="onUpdateCase">
      <template #extra-montant_recouvre>
        <transition name="fade-slide">
          <div v-if="suivi.montant_recouvre" class="fr-col-12 fr-col-md-6 fr-pt-2w">
            <DsfrInput
              v-model="suivi.date_recouvrement_effective"
              label="Date de recouvrement"
              label-visible
              type="date"
              :max="today"
              hint="Date à laquelle la mairie a acté le recouvrement"
            />
          </div>
        </transition>
      </template>
    </ListeActions>

    <DsfrHighlight v-if="suivi.decision_poursuite === 'sanction'" class="fr-ml-0 fr-mt-4w">
      <span class="fr-icon-info-line" aria-hidden="true"></span>
      Le Trésor public se charge de la perception de l'amende. En cas d'insolvabilité de l'auteur,
      la mairie n'est évidemment pas redevable de ce montant. La mairie actera le non-recouvrement
      de l'amende en conseil municipal.
    </DsfrHighlight>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import { getTodayISOString } from '../../utils/date'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const today = getTodayISOString()

const actions = computed((): Action[] => {
  const items: Action[] = []

  if (props.suivi.decision_poursuite === 'sanction') {
    items.push({
      id: 'titre_recette_confirme',
      label: "S'assurer que le titre de recette a été émis par le Trésor public",
      completed: props.suivi.titre_recette_confirme,
    })
    items.push({
      id: 'montant_recouvre',
      label: "S'assurer que le montant de l'amende est recouvert par la mairie",
      completed: props.suivi.montant_recouvre,
    })
  }

  items.push({
    id: 'archivage',
    label: 'Archiver le dossier',
    completed: props.suivi.dossier_archive,
  })

  return items
})

const onUpdateCase = (action: Action, val: boolean) => {
  switch (action.id) {
    case 'titre_recette_confirme':
      props.suivi.titre_recette_confirme = val
      break
    case 'montant_recouvre':
      props.suivi.montant_recouvre = val
      break
    case 'archivage':
      props.suivi.dossier_archive = val
      break
  }
}
</script>
