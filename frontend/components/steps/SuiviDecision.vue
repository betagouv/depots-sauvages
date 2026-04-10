<template>
  <div class="step-decision">
    <template v-if="suivi.ar_statut === 'npai'">
      <DsfrAlert type="info" class="fr-mb-4w" title="L'auteur n'habite pas à l'adresse indiquée">
        <p class="fr-mb-0">
          Pour continuer la procédure, il est indispensable de notifier l'auteur présumé.
        </p>
      </DsfrAlert>

      <div class="fr-mb-4w">
        <ListeActions step-id="decision-npai" :actions="npaiActions" @update-case="onUpdateCase">
          <template #extra-decision_npai>
            <DsfrRadioButtonSet
              v-model="suivi.decision_poursuite"
              legend="Que souhaitez-vous faire ?"
              :options="decisionOptionsNpai"
              name="decision-npai-radios"
              inline
            />
            <transition name="fade-slide">
              <div v-if="suivi.decision_poursuite === 'nouvelle_adresse'" class="fr-mt-2w">
                <p class="fr-mb-0 fr-text--sm">
                  Vous pouvez rechercher une nouvelle adresse par vos propres moyens. Vous pouvez
                  aussi vous rapprocher de la gendarmerie ou écrire au parquet pour obtenir de
                  l'aide.
                </p>
              </div>
            </transition>
          </template>
        </ListeActions>
      </div>
    </template>

    <template v-else>
      <DsfrHighlight class="fr-ml-0 fr-mb-4w">
        <p class="fr-mb-1w">
          Une fois le délai du contradictoire écoulé, deux issues sont possibles selon la réponse de
          l'auteur présumé :
        </p>
        <ul class="fr-mb-0">
          <li>
            <strong>Soit sanctionner l'auteur du dépôt sauvage</strong>
            <ul>
              <li>S'il a reconnu les faits ;</li>
              <li>
                S'il n'a pas répondu à la lettre d'information avant la fin de la période du
                contradictoire ;
              </li>
              <li>S'il nie les faits, mais les preuves contre lui sont accablantes.</li>
            </ul>
          </li>
          <li class="fr-mt-1w">
            <strong>Soit abandonner les poursuites</strong>
            <ul>
              <li>S'il y a un doute sur sa culpabilité ;</li>
              <li>Si les éléments fournis par l'auteur présumé sont jugés convaincants ;</li>
              <li>Si l'on souhaite faire preuve d'indulgence ;</li>
              <li>Si la réponse à la lettre d'information désigne un autre auteur présumé.</li>
            </ul>
          </li>
        </ul>
      </DsfrHighlight>

      <div class="fr-mb-4w">
        <ListeActions step-id="decision" :actions="decisionActions" @update-case="onUpdateCase">
          <template #extra-decision_poursuite>
            <DsfrRadioButtonSet
              v-model="suivi.decision_poursuite"
              legend="Quelle issue souhaitez-vous donner à la procédure ?"
              :options="decisionOptions"
              name="decision-radios"
              inline
            />
          </template>
        </ListeActions>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
}>()

const isDecisionBoxChecked = ref(false)

const isCompleted = computed(() => !!props.suivi.decision_poursuite || isDecisionBoxChecked.value)

const npaiActions = computed((): Action[] => [
  {
    id: 'decision_npai',
    label: 'Décider de la suite à donner',
    completed: isCompleted.value,
  },
])

const decisionActions = computed((): Action[] => [
  {
    id: 'decision_poursuite',
    label: "Décider de l'issue que vous souhaitez donner à la procédure",
    completed: isCompleted.value,
  },
])

const onUpdateCase = (action: Action, val: boolean) => {
  isDecisionBoxChecked.value = val
  if (!val) {
    props.suivi.decision_poursuite = ''
  }
}

const decisionOptions = [
  {
    id: 'decision-sanction',
    label: "Sanctionner l'auteur du dépôt sauvage",
    value: 'sanction',
  },
  {
    id: 'decision-abandon',
    label: 'Abandonner les poursuites',
    value: 'abandon',
  },
]

const decisionOptionsNpai = [
  {
    id: 'decision-npai-abandon',
    label: 'Abandonner la procédure',
    value: 'abandon',
  },
  {
    id: 'decision-npai-recherche',
    label: 'Rechercher une nouvelle adresse',
    value: 'nouvelle_adresse',
  },
]
</script>

<style scoped>
:deep(.fr-fieldset__legend) {
  font-weight: 500;
  margin-bottom: 0.8rem;
}
</style>
