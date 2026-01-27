<template>
  <div class="">
    <div class="fr-card fr-card--lg fr-mb-4w">
      <div class="fr-card__body">
        <h2 class="fr-card__title">
          <VIcon name="ri-pushpin-line" class="fr-mr-1w" /> Ce qu'il vous reste à faire
        </h2>
        <div class="fr-card__desc">
          <div class="fr-tabs fr-background-alt--grey fr-mt-3w">
            <ul class="fr-tabs__list" role="tablist" aria-label="Procédures">
              <li role="presentation">
                <button
                  id="admin-tab"
                  class="fr-tabs__tab fr-tabs__tab--selected"
                  aria-selected="true"
                  tabindex="0"
                  role="tab"
                  aria-controls="admin-panel"
                >
                  Procédure administrative
                </button>
              </li>
              <li role="presentation">
                <button
                  id="judicial-tab"
                  class="fr-tabs__tab"
                  aria-selected="false"
                  tabindex="-1"
                  role="tab"
                  aria-controls="judicial-panel"
                >
                  Procédure judiciaire
                </button>
              </li>
            </ul>
            <div
              id="admin-panel"
              class="fr-tabs__panel fr-tabs__panel--selected"
              role="tabpanel"
              aria-labelledby="admin-tab"
            >
              <ProcedureAdministrative />
            </div>
            <div
              id="judicial-panel"
              class="fr-tabs__panel"
              role="tabpanel"
              aria-labelledby="judicial-tab"
              hidden
            >
              <DsfrNotice type="info" class="fr-mb-3w"> Procédure facultative </DsfrNotice>
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
import ProcedureAdministrative from './tabs/ProcedureAdministrative.vue'
import ProcedureJudiciaire from './tabs/ProcedureJudiciaire.vue'
</script>
