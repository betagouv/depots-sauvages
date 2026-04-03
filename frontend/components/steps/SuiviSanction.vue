<template>
  <div class="step-suivi">
    <!-- Affichage du délai de contradictoire -->
    <DsfrHighlight class="fr-ml-0 fr-mb-4w" :title="deadlineTitle">
      <p v-if="contradictoire.dateFin">
        Fin du délai de contradictoire : <strong>{{ contradictoire.dateFin }}</strong> —
        <span :class="{ 'text-warning-custom': contradictoire.isClose }">
          {{ contradictoire.joursRestantsLabel }}
        </span>
      </p>
      <div v-else>
        <p>
          La période du contradictoire s'étend sur un minimum de <strong>10 jours</strong> à compter
          de la réception de la lettre d'information. Une fois ce délai écoulé, deux issues sont possibles selon la réponse de l'auteur présumé :
        </p>
        <ul class="fr-mb-0">
          <li>
            <strong>Soit sanctionner l'auteur du dépôt sauvage</strong>
            <ul>
              <li>S'il a reconnu les faits ;</li>
              <li>S'il n'a pas répondu à la lettre d'information avant la fin de la période du contradictoire ;</li>
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
      </div>
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

    <transition name="fade-slide" mode="out-in">
      <div v-if="suivi.decision_poursuite === 'sanction'" key="sanction" class="action-block">
        <h5 class="fr-h5 fr-mb-2w">4.1 Sanctionner l'auteur</h5>
        <ListeActions step-id="sanction" :actions="sanctionActions" @update-case="onUpdateSanction">
          <template #extra-fixer_montant>
            <transition name="fade-slide">
              <div v-if="suivi.montant_fixe" class="fr-grid-row fr-grid-row--gutters fr-pt-2w">
                <div class="fr-col-12 fr-col-md-6">
                  <DsfrInput
                    v-model="suivi.montant_amende"
                    label="Montant de l'amende fixée (€)"
                    label-visible
                    type="number"
                    hint="Montant proportionné à la gravité des faits (max 15 000 €, 2 décimales max)"
                    :min="0"
                    :max="15000"
                    step="0.01"
                  />
                  <a
                    href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                    target="_blank"
                    class="fr-text--xs fr-mt-1w fr-display-block"
                  >
                    <span class="fr-icon-links-line fr-icon--sm" aria-hidden="true"></span>
                    Consulter l'aide à l'évaluation
                  </a>
                </div>
                <div class="fr-col-12 fr-col-md-6">
                  <DsfrInput
                    v-model="suivi.date_recouvrement"
                    label="Date prévisionnelle de recouvrement"
                    label-visible
                    type="date"
                    hint="Date indicative pour le suivi"
                  />
                </div>
              </div>
            </transition>
          </template>

          <template #extra-arrete_redige>
            <transition name="fade-slide">
              <div v-if="suivi.arrete_redige" class="fr-pt-2w">
                <p class="fr-text--sm fr-mb-1w">
                  L'arrêté doit être transmis en préfecture pour le contrôle de légalité.
                </p>
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/7b97c0e9-ffc9-4863-834f-759821aa1e0a"
                  target="_blank"
                  class="fr-btn fr-btn--secondary fr-btn--sm"
                >
                  Voir le modèle d'arrêté
                </a>
              </div>
            </transition>
          </template>

          <template #extra-notification_sanction>
            <transition name="fade-slide">
              <div v-if="suivi.notification_sanction_envoyee" class="fr-pt-2w">
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/563be397-7e6d-4d69-b1aa-42598d2f71c6"
                  target="_blank"
                  class="fr-btn fr-btn--secondary fr-btn--sm"
                >
                  Modèle de courrier de notification
                </a>
              </div>
            </transition>
          </template>
        </ListeActions>
      </div>

      <div v-else-if="suivi.decision_poursuite === 'abandon'" key="abandon" class="action-block">
        <h5 class="fr-h5 fr-mb-2w">4.2 Abandonner les poursuites</h5>
        <ListeActions step-id="abandon" :actions="abandonActions" @update-case="onUpdateAbandon">
          <template #extra-motif_abandon>
            <div class="fr-col-12 fr-col-md-8">
              <DsfrSelect
                v-model="suivi.motif_abandon"
                label="Choisir le motif d'abandon de la procédure"
                :options="motifAbandonOptions"
                class="fr-mb-2w"
              />
              <div v-if="suivi.motif_abandon === 'Un auteur identifié'" class="fr-pt-2w">
                <DsfrAlert
                  type="info"
                  title="Poursuite à l'encontre d'un autre auteur"
                  description="La procédure peut être poursuivie à l'encontre d'un autre auteur identifié (ex. prestataire, sous-traitant, fournisseur, client, intermédiaire). Vous pouvez démarrer une nouvelle procédure."
                  class="fr-mb-2w"
                />
                <DsfrButton label="Démarrer une nouvelle procédure" class="fr-btn--sm" disabled />
              </div>
              <transition v-else-if="suivi.motif_abandon" name="fade-slide">
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                  target="_blank"
                  class="fr-btn fr-btn--secondary fr-btn--sm"
                >
                  Modèle de notification d'abandon
                </a>
              </transition>
            </div>
          </template>
        </ListeActions>
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
  modifyUrl?: string
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

const motifAbandonOptions = [
  { text: 'Indulgence', value: 'Indulgence' },
  { text: 'Autre motif de classement sans suite', value: 'Autre motif de classement sans suite' },
  { text: 'Un autre auteur a été identifié', value: 'Un auteur identifié' },
  { text: 'Les éléments fournis par l’auteur sont convaincants', value: 'Éléments convaincants' },
]

// Calcul du délai de contradictoire via l'utilitaire
const contradictoire = computed(() => calculateContradictoire(props.suivi.ar_presentation_date))

const deadlineTitle = computed(() => (contradictoire.value.dateFin ? 'Suivi du contradictoire' : ''))

const sanctionActions = computed((): Action[] => [
  {
    id: 'fixer_montant',
    label: "Fixer le montant de l'amende administrative (montant proportionné à la gravité des faits, jusqu'à 15 000 € maximum)",
    completed: props.suivi.montant_fixe,
  },
  {
    id: 'arrete_redige',
    label: "Rédiger l'arrêté de sanction administrative relatif à l'amende et le soumettre au contrôle de légalité",
    completed: props.suivi.arrete_redige,
  },
  {
    id: 'titre_recette',
    label: 'Émettre un titre de recette à destination du Trésor public',
    completed: props.suivi.titre_recette_emis,
  },
  {
    id: 'notification_sanction',
    label: "Notifier l'auteur",
    completed: props.suivi.notification_sanction_envoyee,
  },
])

const abandonActions = computed((): Action[] => {
  const items: Action[] = [
    {
      id: 'motif_abandon',
      label: 'Choisir le motif d’abandon de poursuite',
      completed: !!props.suivi.motif_abandon,
    },
  ]

  // Si c'est un autre auteur, on n'affiche pas la notification à cette personne
  if (props.suivi.motif_abandon && props.suivi.motif_abandon !== 'Un auteur identifié') {
    items.push({
      id: 'notification_abandon',
      label: "Notifier la personne concernée de la décision d'abandon",
      completed: props.suivi.notification_abandon_envoyee,
    })
  }

  return items
})

const onUpdateSanction = (action: Action, val: boolean) => {
  switch (action.id) {
    case 'fixer_montant':
      props.suivi.montant_fixe = val
      break
    case 'arrete_redige':
      props.suivi.arrete_redige = val
      break
    case 'titre_recette':
      props.suivi.titre_recette_emis = val
      break
    case 'notification_sanction':
      props.suivi.notification_sanction_envoyee = val
      break
  }
}

const onUpdateAbandon = (action: Action, val: boolean) => {
  if (action.id === 'notification_abandon') {
    props.suivi.notification_abandon_envoyee = val
  }
}
</script>

<style scoped>
.decision-section {
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  border: 1px solid var(--border-default-blue-france);
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
