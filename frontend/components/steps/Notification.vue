<template>
  <div class="notification">
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions step-id="notification" :actions="actions" @update-case="onUpdateCase">
      <template #extra-0>
        <div class="fr-col-12 fr-col-md-6 fr-mb-2w">
          <DsfrInput
            v-model="suivi.lettre_envoyee_date"
            label="Date d'envoi de la lettre d'information"
            label-visible
            type="date"
          />
        </div>
      </template>

      <template #extra-2>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrSelect
            v-model="suivi.ar_statut"
            label="Quel est le statut de l'accusé de réception ?"
            :options="arStatusOptions"
            class="fr-mb-2w"
          />

          <transition name="slide-up">
            <div v-if="showDatePresentation" class="fr-mt-2w">
              <DsfrInput
                v-model="suivi.ar_presentation_date"
                label="Date de présentation du courrier recommandé"
                label-visible
                type="date"
                hint="C'est le point de départ de la période du contradictoire (10 jours)"
              />
            </div>
          </transition>

          <transition name="slide-up">
            <DsfrAlert
              v-if="suivi.ar_statut === 'NPAI'"
              class="fr-mt-2w"
              type="info"
              title="L'auteur n'habite pas à l'adresse indiquée"
              description="Vous pouvez directement passer à l'étape de clôture de la procédure."
              small
            />
          </transition>
        </div>
      </template>
    </ListeActions>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ListeActions, { type Action } from './ListeActions.vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const actions = computed((): Action[] => [
  {
    id: 'lettre_envoyee',
    label: "Envoyer la lettre d'information en recommandé avec accusé de réception",
    completed: props.suivi.lettre_envoyee,
  },
  {
    id: 'copie_archives',
    label: 'Conserver une copie de tous les documents pour vos archives',
    completed: props.suivi.copie_archives,
  },
  {
    id: 'ar_recu',
    label:
      "Réceptionner l'accusé de réception : c'est le point de départ de la période du contradictoire",
    completed: props.suivi.ar_recu,
  },
])

const arStatusOptions = [
  { text: 'Distribué', value: 'Distribué' },
  { text: 'Refusé', value: 'Refusé' },
  { text: 'Non réclamé', value: 'Non réclamé' },
  { text: 'NPAI', value: 'NPAI' },
]

const showDatePresentation = computed(() =>
  ['Distribué', 'Refusé', 'Non réclamé'].includes(props.suivi.ar_statut)
)

const onUpdateCase = (action: Action, val: boolean) => {
  switch (action.id) {
    case 'lettre_envoyee':
      props.suivi.lettre_envoyee = val
      break
    case 'copie_archives':
      props.suivi.copie_archives = val
      break
    case 'ar_recu':
      props.suivi.ar_recu = val
      break
  }
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease-out;
  max-height: 500px;
  opacity: 1;
}

.slide-up-enter-from,
.slide-up-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>
