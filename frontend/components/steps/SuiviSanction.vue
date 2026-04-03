<template>
  <div class="step-suivi">
    <DsfrHighlight class="fr-ml-0 fr-mb-4w">
      <p>
        La période du contradictoire s'étend sur un minimum de <strong>10 jours</strong> à compter
        de la réception de la lettre d'information. Une fois ce délai écoulé, vous devez décider de
        la suite à donner :
      </p>
    </DsfrHighlight>

    <div class="decision-section fr-mb-4w fr-p-2w">
      <DsfrRadioButtonSet
        v-model="suivi.decision_poursuite"
        legend="Proposition de suite de la procédure"
        :options="decisionOptions"
        name="decision-radios"
        inline
      />
    </div>

    <transition name="fade-slide" mode="out-in">
      <div v-if="suivi.decision_poursuite === 'sanction'" key="sanction" class="action-block">
        <h5 class="fr-h5 fr-mb-2w">Sanction administrative</h5>
        <ListeActions step-id="sanction" :actions="sanctionActions" @update-case="onUpdateSanction">
          <template #extra-0>
            <div class="fr-grid-row fr-grid-row--gutters">
              <div class="fr-col-12 fr-col-md-6">
                <DsfrInput
                  v-model="suivi.montant_amende"
                  label="Montant de l'amende administrative (€)"
                  label-visible
                  type="number"
                  hint="Montant proportionné à la gravité des faits (max 15 000 €)"
                  :min="0"
                  :max="15000"
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
                  label="Date prévue de recouvrement"
                  label-visible
                  type="date"
                  hint="Date indicative de mise en recouvrement"
                />
              </div>
            </div>
          </template>

          <template #extra-1>
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
          </template>

          <template #extra-3>
            <a
              href="https://fichiers.numerique.gouv.fr/explorer/items/files/563be397-7e6d-4d69-b1aa-42598d2f71c6"
              target="_blank"
              class="fr-btn fr-btn--secondary fr-btn--sm"
            >
              Modèle de courrier de notification
            </a>
          </template>
        </ListeActions>
      </div>

      <div v-else-if="suivi.decision_poursuite === 'abandon'" key="abandon" class="action-block">
        <h5 class="fr-h5 fr-mb-2w">Abandon de la procédure</h5>
        <ListeActions step-id="abandon" :actions="abandonActions" @update-case="onUpdateAbandon">
          <template #extra-0>
            <div class="fr-col-12 fr-col-md-8">
              <DsfrSelect
                v-model="suivi.motif_abandon"
                label="Indiquez le motif de l'abandon"
                :options="motifAbandonOptions"
                class="fr-mb-2w"
              />
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                target="_blank"
                class="fr-btn fr-btn--secondary fr-btn--sm"
              >
                Modèle de notification d'abandon
              </a>
            </div>
          </template>

          <template #extra-1>
            <p class="fr-text--sm">
              Si la réponse de l'auteur désigne une autre personne, vous pouvez créer une nouvelle
              procédure.
            </p>
            <a :href="modifyUrl" target="_blank" class="fr-btn fr-btn--secondary fr-btn--sm">
              Modifier sur Démarche Numérique
            </a>
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

const props = defineProps<{
  suivi: SuiviProcedure
  modifyUrl?: string
}>()

const decisionOptions = [
  {
    id: 'decision-sanction',
    label: "Sanctionner l'auteur",
    value: 'sanction',
  },
  {
    id: 'decision-abandon',
    label: 'Abandonner les poursuites',
    value: 'abandon',
  },
]

const motifAbandonOptions = [
  {
    text: 'Doute sur la culpabilité',
    value: 'Doute sur la culpabilité',
  },
  {
    text: 'Indulgence de l’autorité',
    value: 'Indulgence',
  },
  {
    text: 'Autre auteur identifié',
    value: 'Autre auteur',
  },
  {
    text: 'Le contrevenant a nettoyé le dépôt',
    value: 'Nettoyage effectué',
  },
]

const sanctionActions = computed((): Action[] => [
  {
    id: 'fixer_montant',
    label: "Fixer le montant de l'amende administrative",
    completed: props.suivi.montant_fixe,
  },
  {
    id: 'arrete_redige',
    label: "Rédiger l'arrêté de sanction et le soumettre au contrôle de légalité",
    completed: props.suivi.arrete_redige,
  },
  {
    id: 'titre_recette',
    label: 'Émettre un titre de recette à destination du Trésor public',
    completed: props.suivi.titre_recette_emis,
  },
  {
    id: 'notification_sanction',
    label: "Notifier l'auteur de l'amende administrative",
    completed: props.suivi.notification_sanction_envoyee,
  },
])

const abandonActions = computed((): Action[] => [
  {
    id: 'notification_abandon',
    label: "Notifier l'auteur de la décision d'abandon",
    completed: props.suivi.notification_abandon_envoyee,
  },
  {
    id: 'poursuite_autre',
    label: "Le cas échéant, poursuivre à l'encontre d'un autre auteur",
    completed: false,
  },
])

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
  background-color: var(--background-alt-blue-france);
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

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease-out;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
