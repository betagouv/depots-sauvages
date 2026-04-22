<template>
  <div class="infos-complementaires fr-mb-4w">
    <div class="fr-card fr-card--no-border fr-p-3w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-mb-3w">
          <DsfrRadioButtonSet
            v-model="suivi.nettoyage_fait"
            legend="Le dépôt sauvage a-t-il été nettoyé ?"
            :options="nettoyageOptions"
            name="nettoyage-radios"
            inline
            class="compact-radios"
          />
          <transition name="fade-slide">
            <div v-if="suivi.nettoyage_fait" class="fr-col-12 fr-col-md-4 fr-mt-1w">
              <DsfrSelect
                v-model="suivi.nettoyage_par"
                label="Par qui ?"
                :options="nettoyageParOptions"
              />
            </div>
          </transition>
        </div>

        <div class="fr-col-12">
          <DsfrInput
            v-model="suivi.observations_internes"
            label="Observations internes"
            is-textarea
            placeholder=""
            hint="Dans ce champs vous pouvez ajouter toutes les informations utiles au suivi du dossier. Ces notes internes ne sont pas intégrées aux différents documents de procédures mais peuvent vous aider à ajouter des commentaires complémentaires."
            rows="3"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SuiviProcedure } from '../../stores/suivi-procedure'

defineProps<{
  suivi: SuiviProcedure
}>()

const nettoyageOptions = [
  { label: 'Oui', value: true },
  { label: 'Non', value: false },
]

const nettoyageParOptions = [
  { text: 'L’auteur', value: 'auteur' },
  { text: 'La collectivité', value: 'mairie' },
  { text: 'Un tiers inconnu / prestataire', value: 'prestataire' },
]
</script>

<style scoped>
.infos-complementaires .fr-card {
  background-color: var(--background-alt-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 8px;
}

.compact-radios :deep(.fr-fieldset__legend) {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.compact-radios :deep(.fr-fieldset__content) {
  margin-top: 0;
}

:deep(.fr-label) {
  font-size: 0.9rem;
  font-weight: 700;
}
</style>
