<template>
  <PremiumBox
    title="Aucune procédure en cours"
    description="Vous n'avez pas encore créé de constatation pour initier une procédure administrative de lutte contre les dépôts sauvages."
    iconClass="fr-icon-folder-2-line"
  >
    <template #actions>
      <router-link to="/demarrer-constatation" class="fr-btn">
        <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
        Lancer une procédure
      </router-link>
      <button class="fr-btn fr-btn--secondary" @click="openSimulator">
        <span class="fr-icon-question-line fr-mr-1w" aria-hidden="true"></span>
        Simulateur d'éligibilité
      </button>
    </template>

    <template #footer>
      <div class="premium-info-footer fr-p-3w">
        <p class="fr-text--sm fr-mb-0 text-left">
          <span class="fr-icon-info-line fr-mr-1w" aria-hidden="true" style="vertical-align: middle; color: var(--text-active-blue-france)"></span>
          <strong>Comment ça marche ?</strong> Une fois la constatation du dépôt sauvage effectuée, Protect'Envi génère automatiquement vos documents de procédure et vous guide pas à pas.
        </p>
      </div>
    </template>
  </PremiumBox>
</template>

<script setup lang="ts">
import PremiumBox from '@/components/shared/PremiumBox.vue'
import { openTallyPopup } from '@/utils/tally'

const openSimulator = () => {
  openTallyPopup('A7xA8z', { layout: 'modal', width: 900 })
}
</script>

<style scoped>
.premium-info-footer {
  background-color: var(--background-alt-blue-france);
  border-left: 4px solid var(--border-active-blue-france);
  border-radius: 4px;
}
.text-left {
  text-align: left;
}
</style>
