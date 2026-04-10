<template>
  <div class="step-actions">
    <transition name="fade-slide" mode="out-in">
      <div v-if="suivi.decision_poursuite === 'sanction'" key="sanction" class="action-block">
        <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
        <ListeActions step-id="sanction" :actions="sanctionActions" @update-case="onUpdateSanction">
          <template #extra-fixer_montant>
            <transition name="fade-slide">
              <div v-if="suivi.montant_fixe" class="fr-pt-2w">
                <div class="fr-grid-row">
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInputGroup
                      :error-message="montantError"
                      label="Montant de l'amende fixée (€)"
                      label-visible
                    >
                      <DsfrInput
                        v-model="suivi.montant_amende"
                        type="number"
                        :is-invalid="!!montantError"
                        :min="0"
                        step="50"
                      />
                    </DsfrInputGroup>
                  </div>
                </div>
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                  target="_blank"
                  class="fr-text--xs fr-mt-1w fr-display-block"
                >
                  <span class="fr-icon-links-line fr-icon--sm" aria-hidden="true"></span>
                  Consulter l'aide à l'évaluation
                </a>
              </div>
            </transition>
          </template>

          <template #extra-arrete_redige>
            <transition name="fade-slide">
              <div v-if="suivi.arrete_redige" class="fr-pt-2w">
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
        <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
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
                  description="La procédure peut être poursuivie à l'encontre d'un autre auteur identifié (ex. prestataire, sous-traitant, fournisseur, client, intermédiaire), vous pouvez démarrer une nouvelle procédure."
                  class="fr-mb-2w"
                />
                <a
                  :href="modifyUrl"
                  target="_blank"
                  class="fr-link fr-icon-add-circle-line fr-link--icon-left fr-mt-1w"
                  @click.prevent="openExternalLink(modifyUrl)"
                >
                  Démarrer une nouvelle procédure
                </a>
              </div>
            </div>
          </template>

          <template #extra-notification_abandon>
            <transition name="fade-slide">
              <div v-if="suivi.notification_abandon_envoyee" class="fr-pt-2w">
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                  target="_blank"
                  class="fr-btn fr-btn--secondary fr-btn--sm"
                >
                  Modèle de notification d'abandon
                </a>
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
import { openExternalLink } from '../../utils/browser'
import AttenteDecision from './AttenteDecision.vue'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
  modifyUrl: string
}>()

defineEmits(['back-to-decision'])

const montantError = computed(() => {
  if (props.suivi.montant_amende && props.suivi.montant_amende > 15000) {
    return 'Le montant ne peut pas dépasser 15 000 €'
  }
  return ''
})

const motifAbandonOptions = [
  { text: 'Sélectionnez une option', value: '', disabled: true },
  { text: 'Indulgence', value: 'Indulgence' },
  { text: 'Autre motif de classement sans suite', value: 'Autre motif de classement sans suite' },
  { text: 'Un autre auteur a été identifié', value: 'Un auteur identifié' },
  { text: 'Les éléments fournis par l’auteur sont convaincants', value: 'Éléments convaincants' },
]

const sanctionActions = computed((): Action[] => [
  {
    id: 'fixer_montant',
    label:
      "Fixer le montant de l'amende administrative (montant proportionné à la gravité des faits, jusqu'à 15 000 € maximum)",
    completed: props.suivi.montant_fixe,
  },
  {
    id: 'arrete_redige',
    label:
      "Rédiger l'arrêté de sanction administrative relatif à l'amende et le soumettre au contrôle de légalité",
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
      label: "Choisir le motif d'abandon de poursuite",
      completed: props.suivi.motif_abandon_choisi,
    },
  ]

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
  if (action.id === 'motif_abandon') {
    props.suivi.motif_abandon_choisi = val
    if (!val) {
      props.suivi.motif_abandon = '' // Reset on uncheck
    }
  } else if (action.id === 'notification_abandon') {
    props.suivi.notification_abandon_envoyee = val
  }
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
