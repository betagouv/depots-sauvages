<template>
  <div class="cloture">
    <transition name="fade-slide" mode="out-in">
      <div v-if="suivi.decision_poursuite" key="content">
        <h4 class="fr-h6 fr-mb-2w">Actions pour clôturer la procédure</h4>
        <ListeActions step-id="cloture" :actions="actions" @update-case="onUpdateCase">
          <template #extra-montant_recouvre>
            <transition name="fade-slide">
              <div v-if="suivi.montant_recouvre" class="fr-pt-2w">
                <div class="fr-col-12 fr-col-md-6">
                  <DsfrInput
                    v-model="suivi.date_recouvrement_effective"
                    label="Date de recouvrement"
                    label-visible
                    type="date"
                    :max="today"
                  />
                </div>

                <p class="fr-mt-4w fr-mb-0">
                  <span class="fr-icon-info-line fr-mr-1v" aria-hidden="true"></span>
                  Le Trésor public se charge de la perception de l'amende. En cas d'insolvabilité de
                  l'auteur, la mairie n'est évidemment pas redevable de ce montant. La mairie actera
                  le non-recouvrement de l'amende en conseil municipal.
                </p>
              </div>
            </transition>
          </template>
        </ListeActions>
      </div>

      <AttenteDecision v-else key="no-decision" @action="$emit('back-to-decision')" />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import { getTodayISOString } from '../../utils/date'
import AttenteDecision from './AttenteDecision.vue'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const today = getTodayISOString()

defineEmits(['back-to-decision'])

const actions = computed((): Action[] => {
  const items: Action[] = []

  if (props.suivi.decision_poursuite === 'sanction') {
    items.push({
      id: 'titre_recette_confirme',
      label: "S'assurer auprès du Trésor public que l'amende a été payée",
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

<style scoped></style>
