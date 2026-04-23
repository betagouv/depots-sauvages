<template>
  <div class="infos-complementaires fr-mb-4w">
    <div class="fr-grid-row">
      <div class="fr-col-12">
        <SelectableChoices
          v-model="suivi.nettoyage_fait"
          legend="Le dépôt sauvage a-t-il été nettoyé ?"
          :options="nettoyageOptions"
        >
          <transition name="fade-slide">
            <div v-if="suivi.nettoyage_fait" class="fr-mt-3w">
              <div class="fr-grid-row">
                <div class="fr-col-12 fr-col-md-6">
                  <DsfrSelect
                    v-model="suivi.nettoyage_par"
                    label="Par qui ?"
                    :options="nettoyageParOptions"
                  />
                </div>
              </div>
            </div>
          </transition>
        </SelectableChoices>
      </div>

      <div class="fr-col-12 fr-mt-4w">
        <div class="notes-section fr-p-3w">
          <h5 class="fr-h5 fr-mb-1w">Notes internes</h5>
          <p class="fr-text--sm fr-mb-2w">
            Vous pouvez ajouter ici des notes et des observations qui ne seront pas intégrées à la
            procédure.
          </p>
          <DsfrInput
            v-model="suivi.observations_internes"
            label=""
            is-textarea
            placeholder="Ajouter une observation..."
            rows="3"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import SelectableChoices from '../shared/SelectableChoices.vue'

defineProps<{
  suivi: SuiviProcedure
}>()

const nettoyageOptions = [
  { id: 'nettoyage-oui', label: 'Oui, le dépôt a été nettoyé', value: true },
  { id: 'nettoyage-non', label: 'Non, le dépôt est toujours présent', value: false },
]

const nettoyageParOptions = [
  { text: 'L’auteur', value: 'auteur' },
  { text: 'La collectivité', value: 'mairie' },
  { text: 'Un tiers inconnu / prestataire', value: 'prestataire' },
]
</script>

<style scoped>
.notes-section {
  background-color: var(--background-alt-blue-france);
  border: 1px solid var(--border-default-blue-france);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
  transition: all 0.2s ease;
}

.notes-section:focus-within {
  border-color: var(--border-plain-blue-france);
  box-shadow:
    0 0 0 1px var(--border-plain-blue-france),
    0 4px 12px rgba(0, 0, 145, 0.1);
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
