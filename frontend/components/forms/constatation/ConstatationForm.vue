<template>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-3">
      <nav class="fr-summary fr-mb-4w sticky-summary" role="navigation" aria-labelledby="fr-summary-title">
        <p class="fr-summary__title" id="fr-summary-title">Sommaire</p>
        <ol class="fr-summary__list">
          <li>
            <a class="fr-summary__link" href="#localisation">Localisation du dépôt</a>
          </li>
          <li>
            <a class="fr-summary__link" href="#detail">Détail de la constatation</a>
          </li>
          <li>
            <a class="fr-summary__link" href="#description">Description du dépôt</a>
          </li>
          <li>
            <a class="fr-summary__link" href="#auteur">Auteur présumé du dépôt</a>
          </li>
          <li v-if="showPrejudice">
            <a class="fr-summary__link" href="#prejudice">Estimation du préjudice</a>
          </li>
          <li>
            <a class="fr-summary__link" href="#finalisation">Finalisation de la démarche</a>
          </li>
        </ol>
      </nav>
    </div>

    <div class="fr-col-12 fr-col-md-9">
      <div class="constatation-form fr-pb-10w">
        <DsfrCallout class="fr-mb-4w">
          Les champs marqués d'un astérisque (*) sont obligatoires.
        </DsfrCallout>
        <SectionLocalisation id="localisation" />
        <SectionConstatation id="detail" />
        <SectionDescription id="description" />
        <SectionAuteurDepot id="auteur" />
        <SectionPrejudice
          v-if="showPrejudice"
          id="prejudice"
        />
        <SectionFinalisation id="finalisation" />

        <div class="fr-grid-row fr-grid-row--center fr-mt-6w">
          <DsfrButton
            label="Enregistrer la constatation"
            :loading="store.loading"
            @click="store.submit"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConstatationStore } from '@/stores/constatation'
import { DsfrButton, DsfrCallout } from '@gouvminint/vue-dsfr'
import SectionConstatation from './SectionConstatation.vue'
import SectionDescription from './SectionDescription.vue'
import SectionFinalisation from './SectionFinalisation.vue'
import SectionLocalisation from './SectionLocalisation.vue'
import SectionPrejudice from './SectionPrejudice.vue'
import SectionAuteurDepot from './SectionAuteurDepot.vue'

const store = useConstatationStore()

const showPrejudice = computed(() => 
  ['Déposée', 'Sera déposée'].includes(store.formData.plainteEtat)
)
</script>

<style scoped>
.sticky-summary {
  position: sticky;
  top: 2rem;
}

.constatation-form {
  padding-bottom: 4rem;
}
</style>
