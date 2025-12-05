<template>
  <div class="fr-mt-4w">
    <div class="fr-card fr-card--lg fr-mb-4w">
      <div class="fr-card__body">
        <h2 class="fr-card__title">
          <VIcon name="ri-pushpin-line" class="fr-mr-1w" /> Ce qu'il vous reste à faire
        </h2>
        <div class="fr-card__desc">
          <DsfrNotice class="fr-mb-3w">Avant d'entamer la procédure</DsfrNotice>
          <p class="fr-mb-3w">
            Pour lancer officiellement une procédure à l'encontre de l'auteur présumé de ce dépôt
            sauvage :
          </p>
          <div class="fr-mb-3w">
            <div class="fr-mb-2w">
              <VIcon name="ri-download-line" class="fr-mr-1w" /> Téléchargez le rapport de
              constatation et la lettre d'information
            </div>
            <div>
              <VIcon name="ri-edit-line" class="fr-mr-1w" /> Relisez, complétez et signez ces deux
              documents (ou faites-les signer par votre autorité compétente : maire ou personne
              habilitée à réaliser des constatations).
            </div>
          </div>

          <div class="fr-tabs fr-mt-3w fr-background-alt--grey fr-p-3w tabs-section">
            <ul class="fr-tabs__list" role="tablist" aria-label="Procédures">
              <li role="presentation">
                <button
                  id="admin-tab"
                  class="fr-tabs__tab"
                  :class="{ 'fr-tabs__tab--selected': selectedTab === 0 }"
                  :aria-selected="selectedTab === 0"
                  :tabindex="selectedTab === 0 ? 0 : -1"
                  role="tab"
                  aria-controls="admin-panel"
                  @click="selectedTab = 0"
                >
                  Procédure administrative (recommandé)
                </button>
              </li>
              <li role="presentation">
                <button
                  id="judicial-tab"
                  class="fr-tabs__tab"
                  :class="{ 'fr-tabs__tab--selected': selectedTab === 1 }"
                  :aria-selected="selectedTab === 1"
                  :tabindex="selectedTab === 1 ? 0 : -1"
                  role="tab"
                  aria-controls="judicial-panel"
                  @click="selectedTab = 1"
                >
                  Procédure judiciaire (facultatif)
                </button>
              </li>
            </ul>
            <div
              id="admin-panel"
              class="fr-tabs__panel"
              :class="{ 'fr-tabs__panel--selected': selectedTab === 0 }"
              role="tabpanel"
              aria-labelledby="admin-tab"
              :hidden="selectedTab !== 0"
            >
              <ProcedureAdministrative />
            </div>
            <div
              id="judicial-panel"
              class="fr-tabs__panel"
              :class="{ 'fr-tabs__panel--selected': selectedTab === 1 }"
              role="tabpanel"
              aria-labelledby="judicial-tab"
              :hidden="selectedTab !== 1"
            >
              <ProcedureJudiciaire />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrNotice } from '@gouvminint/vue-dsfr'
import { ref } from 'vue'
import ProcedureAdministrative from './tabs/ProcedureAdministrative.vue'
import ProcedureJudiciaire from './tabs/ProcedureJudiciaire.vue'

defineProps<{
  modifyUrl?: string | null
}>()

const selectedTab = ref(0)
</script>

<style scoped>
.tabs-section {
  border-radius: 4px;
}
</style>
