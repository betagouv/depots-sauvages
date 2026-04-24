<template>
  <div class="step-decision">
    <DsfrHighlight v-if="!isNpai" class="fr-ml-0 fr-mb-4w">
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
            <li>Si la responsabilité de l'auteur présumé n'est pas clairement établie ;</li>
            <li>Si l'on souhaite faire preuve d'indulgence ;</li>
            <li>Si la réponse à la lettre d'information désigne un autre auteur présumé.</li>
          </ul>
        </li>
      </ul>
    </DsfrHighlight>

    <SelectableChoices
      v-model="suivi.decision_poursuite"
      :legend="currentLegend"
      :options="currentOptions"
      class="fr-mt-4w"
    />

    <transition name="fade-slide">
      <div v-if="isNpai && suivi.decision_poursuite === 'recherche_adresse'" class="fr-mt-3w">
        <DsfrAlert type="info">
          <p class="fr-text--sm fr-mb-2w">
            La procédure est en pause. Vous pouvez rechercher une nouvelle adresse :
          </p>
          <ul class="fr-text--sm fr-mb-2w">
            <li>Par vos propres moyens, notamment par internet.</li>
            <li>
              En allant porter plainte à la brigade ou au commissariat, et en écrivant par la suite
              au procureur de la République pour demander l'adresse de l'auteur.
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/files/0b9b0e3b-f25a-4848-ba5f-991e27dd25cd"
                target="_blank"
                rel="noopener noreferrer"
                >Modèle de lettre au procureur</a
              >
            </li>
          </ul>
          <p class="fr-text--sm fr-mb-0">
            <strong>Une fois la nouvelle adresse trouvée, </strong>
            <a :href="modifyUrl" target="_blank" rel="noopener noreferrer">mettez à jour</a>
            le rapport de constatation et la lettre d'information puis retournez à
            <a href="#" @click.prevent="$emit('back-to-notification')">l'étape précédente</a>
            pour indiquer la nouvelle date d'envoi et le statut de l'accusé de réception.
          </p>
        </DsfrAlert>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import SelectableChoices from '../shared/SelectableChoices.vue'

const props = defineProps<{
  suivi: SuiviProcedure
  modifyUrl?: string
}>()

defineEmits(['back-to-notification'])

const isNpai = computed(() => props.suivi.ar_statut === 'npai')

const currentLegend = computed(() =>
  isNpai.value
    ? "L'auteur n'habite pas à l'adresse indiquée, que souhaitez-vous faire ?"
    : 'Quelle issue souhaitez-vous donner à la procédure ?'
)

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
    value: 'recherche_adresse',
  },
]

const currentOptions = computed(() => (isNpai.value ? decisionOptionsNpai : decisionOptions))

watch(
  () => props.suivi.decision_poursuite,
  (newVal) => {
    if (newVal === 'abandon' && isNpai.value) {
      props.suivi.motif_abandon = 'Auteur introuvable (NPAI)'
    }
  }
)
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
