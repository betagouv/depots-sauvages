<template>
  <div class="step-notification">
    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
    <ListeActions step-id="notification" :actions="actions" @update-case="onUpdateCase">
      <template #extra-lettre_envoyee>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="suivi.lettre_envoyee_date"
            label="Date d'envoi du courrier"
            label-visible
            type="date"
          />
        </div>
      </template>

      <template #extra-ar_recu>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrSelect
              v-model="suivi.ar_statut"
              label="Statut du recommandé"
              :options="arStatusOptions"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInput
              v-model="suivi.ar_presentation_date"
              label="Date de présentation / réception"
              label-visible
              type="date"
              hint="Utilisée pour calculer le délai de contradictoire"
            />
          </div>
        </div>
      </template>
    </ListeActions>

    <!-- Info complémentaire sur le contradictoire -->
    <transition name="fade-slide">
      <div v-if="suivi.ar_presentation_date && suivi.ar_recu" class="fr-mt-4w">
        <DsfrAlert
          type="info"
          :title="`Fin de la période du contradictoire : ${contradictoire.dateFin}`"
        >
          <p>
            {{ contradictoire.joursRestantsLabel }}
          </p>
        </DsfrAlert>
      </div>
    </transition>

    <!-- Alerte spécifique NPAI -->
    <transition name="fade-slide">
      <div v-if="suivi.ar_statut === 'inconnu' && suivi.ar_recu" class="fr-mt-2w">
        <DsfrAlert
          type="info"
          title="Adresse incomplète (NPAI)"
          description="L'auteur n'habite pas à l'adresse indiquée vous pouvez directement passer à l'étape de clôture de la procédure."
        />
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ListeActions, { type Action } from './ListeActions.vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import { calculateContradictoire } from '../../utils/procedure'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const contradictoire = computed(() => calculateContradictoire(props.suivi.ar_presentation_date))

const arStatusOptions = [
  { text: 'Distribué', value: 'distribue' },
  { text: 'Refusé', value: 'refuse' },
  { text: 'Non réclamé (Pli avisé non réclamé)', value: 'non_reclame' },
  { text: 'NPAI (Adresse incomplète / Inconnu à cette adresse)', value: 'inconnu' },
]

const actions = computed((): Action[] => [
  {
    id: 'lettre_envoyee',
    label: "Envoyer la lettre d'information en recommandé avec accusé de réception",
    completed: props.suivi.lettre_envoyee,
  },
  {
    id: 'copie_archives',
    label: "Conserver une copie de tous les documents pour vos archives",
    completed: props.suivi.copie_archives,
  },
  {
    id: 'ar_recu',
    label: "Réceptionner l'accusé de réception : c'est le point de départ de la période du contradictoire",
    completed: props.suivi.ar_recu,
  },
])

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
