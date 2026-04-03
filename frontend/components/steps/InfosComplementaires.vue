<template>
  <div class="infos-complementaires fr-mb-4w">
    <div class="fr-card fr-card--no-border fr-p-3w">
      <div class="fr-grid-row">
        <!-- Nettoyage -->
        <div class="fr-col-12 fr-mb-3w">
          <DsfrRadioButtonSet
            v-model="suivi.nettoyage_fait"
            legend="Dépôt nettoyé ?"
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

        <!-- Observations -->
        <div class="fr-col-12">
          <DsfrInput
            v-model="suivi.observations_internes"
            label="Observations internes (mairie)"
            is-textarea
            placeholder="Notes, détails sur le contrevenant, historique..."
            hint="Ces informations ne sont pas transmises à l'auteur."
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
  { text: 'L\'auteur du dépôt', value: 'auteur' },
  { text: 'La collectivité (Régie)', value: 'mairie' },
  { text: 'Prestataire tiers', value: 'prestataire' },
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
