<template>
  <div class="step-decision">
    <template v-if="suivi.ar_statut === 'npai'">
      <DsfrAlert type="info" class="fr-mb-4w" title="L'auteur n'habite pas à l'adresse indiquée">
        <p class="fr-mb-0">
          Pour continuer la procédure, il est indispensable de notifier l'auteur présumé.
        </p>
      </DsfrAlert>

      <div class="decision-section fr-mb-4w fr-p-2w">
        <DsfrRadioButtonSet
          v-model="suivi.decision_poursuite"
          legend="Que souhaitez-vous faire ?"
          :options="decisionOptionsNpai"
          name="decision-npai-radios"
          inline
        />

        <transition name="fade-slide">
          <div
            v-if="suivi.decision_poursuite === 'nouvelle_adresse'"
            class="fr-mt-3w fr-ml-1w border-left-blue fr-pl-2w"
          >
            <p class="fr-mb-0 fr-text--sm">
              Vous pouvez rechercher une nouvelle adresse par vos propres moyens. Vous pouvez aussi
              vous rapprocher de la gendarmerie ou écrire au parquet pour obtenir de l'aide.
            </p>
          </div>
        </transition>
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

      <div class="decision-section fr-mb-4w fr-p-2w">
        <DsfrRadioButtonSet
          v-model="suivi.decision_poursuite"
          legend="Quelle issue souhaitez-vous donner à la procédure ?"
          :options="decisionOptions"
          name="decision-radios"
          inline
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { SuiviProcedure } from '../../stores/suivi-procedure'

defineProps<{
  suivi: SuiviProcedure
}>()

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
.decision-section {
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  border: 1px solid var(--border-default-blue-france);
}

.border-left-blue {
  border-left: 2px solid var(--border-default-blue-france);
}

@media (max-width: 767px) {
  .decision-section {
    padding: 1rem !important;
    margin-bottom: 1.5rem !important;
  }
}

:deep(.fr-fieldset__legend) {
  font-weight: 500;
  margin-bottom: 0.8rem;
}
</style>
