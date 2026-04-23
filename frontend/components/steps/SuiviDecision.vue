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

    <div class="decision-outcome fr-p-3w fr-mt-4w">
      <h5 class="fr-h5 fr-mb-3w text-center">{{ currentLegend }}</h5>
      <div class="fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-grid-row--stretch">
        <div v-for="option in currentOptions" :key="option.value" class="fr-col-12 fr-col-md-6">
          <DsfrCheckbox
            :name="option.id"
            :label="option.label"
            :model-value="suivi.decision_poursuite === option.value"
            @update:model-value="toggleDecision(option.value)"
          />
        </div>
      </div>

      <transition name="fade-slide">
        <div v-if="isNpai && suivi.decision_poursuite === 'recherche_adresse'" class="fr-mt-3w">
          <DsfrAlert type="info">
            <p class="fr-text--sm fr-mb-2w">
              La procédure est en pause. Vous pouvez rechercher une nouvelle adresse :
            </p>
            <ul class="fr-text--sm fr-mb-2w">
              <li>Par vos propres moyens, notamment par internet.</li>
              <li>
                En allant porter plainte à la brigade ou au commissariat, et en écrivant par la
                suite au procureur de la République pour demander l'adresse de l'auteur.
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
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import type { SuiviProcedure } from '../../stores/suivi-procedure'

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

const toggleDecision = (val: string) => {
  if (props.suivi.decision_poursuite === val) {
    props.suivi.decision_poursuite = ''
  } else {
    props.suivi.decision_poursuite = val
  }
}

watch(
  () => props.suivi.decision_poursuite,
  (newVal) => {
    if (newVal === 'abandon' && isNpai.value) {
      props.suivi.motif_abandon = 'Auteur introuvable (NPAI)'
      props.suivi.motif_abandon_choisi = true
    }
  }
)
</script>

<style scoped>
.decision-outcome {
  background-color: var(--background-alt-blue-france);
  border-radius: 12px;
  border: 1px solid var(--border-default-blue-france);
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
}

.decision-outcome :deep(.fr-checkbox-group) {
  background-color: var(--background-default-grey);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-default-grey);
  transition: all 0.2s ease;
  height: 100%;
  margin-bottom: 0;
}

.decision-outcome :deep(.fr-checkbox-group:hover) {
  background-color: var(--background-alt-grey-hover);
}

.decision-outcome :deep(.fr-checkbox-group input[type='checkbox']:checked + label) {
  font-weight: bold;
}

.text-center {
  text-align: center;
}

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
