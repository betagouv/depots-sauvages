<template>
  <div class="infos-complementaires fr-mb-4w">
    <div class="fr-card fr-card--no-border fr-p-3w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-mb-3w">
          <SelectableChoices
            v-model="suivi.nettoyage_fait"
            legend="Le dépôt sauvage a-t-il été nettoyé ?"
            :options="nettoyageOptions"
            class="fr-mb-2w"
          />
          <transition name="fade-slide">
            <div v-if="suivi.nettoyage_fait" class="fr-col-12 fr-col-md-6 fr-mt-2w">
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
            label="Notes internes"
            is-textarea
            placeholder=""
            hint="Vous pouvez ajouter ici des notes et des observations qui ne seront pas intégrées à la procédure."
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
.infos-complementaires .fr-card {
  background-color: var(--background-alt-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 8px;
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
