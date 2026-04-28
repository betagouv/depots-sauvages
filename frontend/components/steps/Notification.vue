<template>
  <div class="step-notification">
    <DsfrAlert type="info" title="Documents pour cette étape" class="fr-mb-4w">
      <p class="fr-mb-2w">
        Vous devez envoyer la lettre d'information à l'auteur présumé. Si vous ne l'avez pas encore
        téléchargée :
      </p>
      <DsfrButton secondary size="sm" @click="openUrl(lettreInfoUrl)">
        <span class="fr-icon-download-line fr-mr-1w" aria-hidden="true"></span>
        Télécharger la lettre d'information
      </DsfrButton>
    </DsfrAlert>

    <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire :</h4>
    <ListeActions step-id="notification" :actions="actions" @update-case="onUpdateCase">
      <template #extra-lettre_envoyee>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInput
            v-model="suivi.lettre_envoyee_date"
            label="Date d'envoi du courrier"
            label-visible
            type="date"
            :max="today"
          />
        </div>
      </template>

      <template #extra-ar_recu>
        <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrSelect
              v-model="suivi.ar_statut"
              label="Quel est le statut de l'accusé réception ?"
              :options="arStatusOptions"
            />
          </div>
          <div v-if="suivi.ar_statut && suivi.ar_statut !== 'npai'" class="fr-col-12 fr-col-md-6">
            <DsfrInput
              v-model="suivi.ar_presentation_date"
              label="Date de présentation du courrier recommandé"
              label-visible
              type="date"
              :max="today"
              hint="Utilisée pour calculer le délai du contradictoire"
            />
          </div>
        </div>
      </template>
    </ListeActions>

    <transition name="fade-slide">
      <div
        v-if="suivi.ar_presentation_date && suivi.ar_recu && suivi.ar_statut !== 'npai'"
        class="fr-mt-4w"
      >
        <DsfrAlert
          type="info"
          :title="`La période du contradictoire se termine le ${contradictoire.dateFin}`"
        >
          <p>
            {{ contradictoire.joursRestantsLabel }}
          </p>
        </DsfrAlert>
      </div>
    </transition>

    <transition name="fade-slide">
      <div v-if="suivi.ar_statut === 'npai' && suivi.ar_recu" class="fr-mt-4w">
        <DsfrAlert type="info" title="L'auteur n'habite pas à l'adresse indiquée">
          <p class="fr-mb-0 fr-text--sm">
            Pour continuer la procédure, il est indispensable de notifier l'auteur présumé.
            Rendez-vous à <a href="#" @click.prevent="$emit('next-step')">l'étape suivante</a> pour
            décider de la suite à donner.
          </p>
        </DsfrAlert>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import { getTodayISOString } from '../../utils/date'
import { calculateContradictoire } from '../../utils/procedure'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
  lettreInfoUrl: string
}>()

const openUrl = (url: string) => {
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

defineEmits(['next-step'])

const today = getTodayISOString()

const contradictoire = computed(() => calculateContradictoire(props.suivi.ar_presentation_date))

const arStatusOptions = [
  { text: 'Sélectionnez un statut', value: '' },
  { text: 'Distribué', value: 'distribue' },
  { text: 'Refusé', value: 'refuse' },
  { text: 'Non réclamé', value: 'non_reclame' },
  { text: 'NPAI', value: 'npai' },
]

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
