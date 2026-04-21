<template>
  <div class="step-actions">
    <transition name="fade-slide" mode="out-in">
      <div v-if="suivi.decision_poursuite === 'sanction'" key="sanction" class="action-block">
        <DsfrAlert type="info" title="Modèles de documents" class="fr-mb-4w">
          <p class="fr-mb-2w">
            Pour vous accompagner dans vos démarches, des modèles sont à votre disposition :
          </p>
          <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--sm fr-mb-0">
            <li>
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/7b97c0e9-ffc9-4863-834f-759821aa1e0a"
                target="_blank"
                class="fr-btn fr-btn--secondary"
              >
                Modèle d'arrêté de sanction
              </a>
            </li>
            <li>
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/563be397-7e6d-4d69-b1aa-42598d2f71c6"
                target="_blank"
                class="fr-btn fr-btn--secondary"
              >
                Modèle de courrier de notification
              </a>
            </li>
            <li>
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                target="_blank"
                class="fr-btn fr-btn--secondary"
              >
                Aide à l'évaluation
              </a>
            </li>
          </ul>
        </DsfrAlert>

        <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
        <ListeActions step-id="sanction" :actions="sanctionActions" @update-case="onUpdateSanction">
          <template #extra-fixer_montant>
            <transition name="fade-slide">
              <div v-if="suivi.montant_fixe" class="fr-pt-2w">
                <div class="fr-grid-row">
                  <div class="fr-col-12 fr-col-md-6">
                    <DsfrInput
                      v-model="suivi.montant_amende"
                      type="number"
                      label="Montant de l'amende (€)"
                      label-visible
                      :error-message="montantError"
                      :is-invalid="!!montantError"
                      :min="0"
                      step="50"
                    />
                  </div>
                </div>
              </div>
            </transition>
          </template>

        </ListeActions>
      </div>

      <div v-else-if="suivi.decision_poursuite === 'abandon'" key="abandon" class="action-block">
        <template v-if="suivi.ar_statut === 'npai'">
          <DsfrAlert type="success" title="Aucune action requise" class="fr-mb-4w">
            Le statut NPAI a automatiquement validé l'abandon pour "Auteur introuvable". Dans ce cas
            précis, aucun courrier de notification n'est à envoyer.
            <div class="fr-mt-2w">
              <DsfrButton @click="$emit('go-to-cloture')" size="sm">
                Passer directement à la clôture
              </DsfrButton>
            </div>
          </DsfrAlert>
        </template>
        <template v-else>
          <DsfrAlert type="info" title="Modèles de documents" class="fr-mb-4w">
            <p class="fr-mb-2w">
              Pour vous accompagner dans vos démarches, un modèle est à votre disposition :
            </p>
            <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--sm fr-mb-0">
              <li>
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                  target="_blank"
                  class="fr-btn fr-btn--secondary"
                >
                  Modèle de notification d'abandon
                </a>
              </li>
            </ul>
          </DsfrAlert>

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
                    :href="newProcedureUrl"
                    target="_blank"
                    class="fr-link fr-icon-add-circle-line fr-link--icon-left fr-mt-1w"
                    @click.prevent="openExternalLink(newProcedureUrl)"
                  >
                    Démarrer une nouvelle procédure
                  </a>
                </div>
                <div
                  v-if="
                    suivi.motif_abandon &&
                    suivi.motif_abandon !== 'Un auteur identifié' &&
                    suivi.ar_statut !== 'npai'
                  "
                  class="fr-pt-2w"
                >
                  <DsfrRadioButtonSet
                    v-model="suivi.souhaite_notifier_abandon"
                    legend="Souhaitez vous notifier la personne concernée de la décision d'abandon de la procédure administrative"
                    :options="notificationChoiceOptions"
                    name="notifier-abandon-radios"
                    inline
                  />
                </div>
              </div>
            </template>

          </ListeActions>
        </template>
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

const newProcedureUrl = import.meta.env.VITE_DN_URL

defineEmits(['back-to-decision', 'go-to-cloture'])

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
  { text: 'Auteur introuvable (NPAI)', value: 'Auteur introuvable (NPAI)' },
]

const notificationChoiceOptions = [
  { label: 'Oui', value: true, id: 'notifier-oui' },
  { label: 'Non', value: false, id: 'notifier-non' },
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

  if (
    props.suivi.motif_abandon &&
    props.suivi.motif_abandon !== 'Un auteur identifié' &&
    props.suivi.motif_abandon !== 'Auteur introuvable (NPAI)' &&
    props.suivi.souhaite_notifier_abandon === true
  ) {
    items.push({
      id: 'notification_abandon',
      label: "Rédiger et envoyer la notification d'abandon",
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
      props.suivi.souhaite_notifier_abandon = null
      props.suivi.notification_abandon_envoyee = false
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
