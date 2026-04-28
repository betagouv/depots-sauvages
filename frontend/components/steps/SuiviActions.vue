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
                Aide à l'évaluation de l'amende
              </a>
            </li>
            <li>
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/5f899dd5-ff04-4115-856a-31bfd29006cb"
                target="_blank"
                class="fr-btn fr-btn--secondary"
              >
                Exemple de titre de recette
              </a>
            </li>
          </ul>
        </DsfrAlert>

        <h4 class="fr-h6 fr-mb-3w">Ce qu'il vous reste à faire :</h4>
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

          <SelectableChoices
            v-model="suivi.motif_abandon"
            legend="Quel est le motif d'abandon de la poursuite ?"
            :options="motifAbandonOptions"
            layout="list"
            class="fr-my-4w"
            @update:model-value="onMotifUpdate"
          />

          <transition name="fade-slide">
            <div v-if="suivi.motif_abandon === 'Un auteur identifié'" class="fr-mt-3w">
              <DsfrAlert type="info" title="Poursuite à l'encontre d'un autre auteur">
                <p class="fr-text--sm fr-mb-2w">
                  La procédure peut être poursuivie à l'encontre d'un autre auteur identifié (ex.
                  prestataire, sous-traitant, fournisseur, client, intermédiaire).
                </p>
                <DsfrButton secondary size="sm" @click="openExternalLink(newProcedureUrl)">
                  <span class="fr-icon-add-circle-line fr-mr-1w" aria-hidden="true"></span>
                  Démarrer une nouvelle procédure
                </DsfrButton>
              </DsfrAlert>
            </div>
          </transition>

          <transition name="fade-slide">
            <SelectableChoices
              v-if="
                suivi.motif_abandon &&
                suivi.motif_abandon !== 'Un auteur identifié' &&
                suivi.motif_abandon !== 'Auteur introuvable (NPAI)'
              "
              v-model="suivi.souhaite_notifier_abandon"
              legend="Souhaitez-vous notifier la personne de l'abandon ?"
              :options="notificationOptions"
              class="fr-mt-4w"
            />
          </transition>

          <transition name="fade-slide">
            <div v-if="showActionsList" class="actions-list-container">
              <h4 class="fr-h6 fr-mb-3w">Ce qu'il vous reste à faire :</h4>
              <ListeActions
                step-id="abandon"
                :actions="abandonActions"
                @update-case="onUpdateAbandon"
              />
            </div>
          </transition>
        </template>
      </div>

      <AttenteDecision v-else key="no-decision" @action="$emit('back-to-decision')" />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import SelectableChoices from '../shared/SelectableChoices.vue'
import AttenteDecision from './AttenteDecision.vue'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
  modifyUrl: string
}>()

const newProcedureUrl = 'https://www.demarches-simplifiees.fr/commencer/sa-depot-sauvage'

const openExternalLink = (url: string) => {
  window.open(url, '_blank')
}

defineEmits(['back-to-decision', 'go-to-cloture'])

const montantError = computed(() => {
  if (props.suivi.montant_amende && props.suivi.montant_amende > 15000) {
    return 'Le montant ne peut pas dépasser 15 000 €'
  }
  return ''
})

const motifAbandonOptions = [
  { id: 'motif-indulgence', label: 'Indulgence', value: 'Indulgence' },
  {
    id: 'motif-elements',
    label: "La responsabilité de l'auteur présumé n'est pas clairement établie",
    value: 'Éléments convaincants',
  },
  {
    id: 'motif-autre-auteur',
    label: 'Un autre auteur a été identifié',
    value: 'Un auteur identifié',
  },
  { id: 'motif-npai', label: 'Auteur introuvable (NPAI)', value: 'Auteur introuvable (NPAI)' },
  {
    id: 'motif-autre',
    label: 'Autre motif de classement sans suite',
    value: 'Autre motif de classement sans suite',
  },
]

const notificationOptions = [
  { id: 'notify-yes', label: 'Oui, notifier', value: true },
  { id: 'notify-no', label: 'Non, ne pas notifier', value: false },
]

const onMotifUpdate = (val: string) => {
  // Si NPAI ou Autre auteur, on ne notifie pas (déjà géré ou pas pertinent)
  if (val === 'Auteur introuvable (NPAI)' || val === 'Un auteur identifié') {
    props.suivi.souhaite_notifier_abandon = false
  } else if (!val) {
    props.suivi.souhaite_notifier_abandon = null
  }
}

const showActionsList = computed(() => {
  if (!props.suivi.motif_abandon) return false
  if (
    props.suivi.motif_abandon === 'Auteur introuvable (NPAI)' ||
    props.suivi.motif_abandon === 'Un auteur identifié'
  )
    return false
  return props.suivi.souhaite_notifier_abandon === true
})

const sanctionActions = computed((): Action[] => [
  {
    id: 'fixer_montant',
    label: "Fixer le montant de l'amende administrative en utilisant l'aide à l'évaluation fournie",
    completed: props.suivi.montant_fixe,
  },
  {
    id: 'arrete_redige',
    label:
      "Rédiger l'arrêté de sanction administrative relatif à l'amende et le soumettre au contrôle de légalité  : utiliser le modèle d'arrêté fourni",
    completed: props.suivi.arrete_redige,
  },
  {
    id: 'titre_recette',
    label:
      "Émettre un titre de recette à destination du Trésor public  : utiliser l'exemple fourni",
    completed: props.suivi.titre_recette_emis,
  },
  {
    id: 'notification_sanction',
    label: "Notifier l'auteur  : utiliser le modèle de notification fourni",
    completed: props.suivi.notification_sanction_envoyee,
  },
])

const abandonActions = computed((): Action[] => {
  const items: Action[] = []

  if (
    props.suivi.motif_abandon &&
    props.suivi.motif_abandon !== 'Un auteur identifié' &&
    props.suivi.motif_abandon !== 'Auteur introuvable (NPAI)' &&
    props.suivi.souhaite_notifier_abandon === true
  ) {
    items.push({
      id: 'notification_abandon',
      label:
        "Rédiger et envoyer la notification d'abandon  : utiliser le modèle de notification fourni",
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
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
