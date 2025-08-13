<template>
  <div class="fr-container--sm">
    <h1 class="fr-h2 fr-py-3w">Procédure dépôt sauvage</h1>
    <DsfrCallout v-if="store.currentStep === 1" class="fr-mb-3w">
      <p>
        Ce formulaire vise à vous accompagner lorsque vous devez traiter un dépôt sauvage. Une fois
        le formulaire rempli, des documents personnalisés seront générés pour vous permettre
        d'initier une procédure administrative et faciliter un éventuel dépôt de plainte. Des
        conseils vous seront aussi proposés pour la suite des procédures.
      </p>
    </DsfrCallout>

    <WasteReportForm @step-change="store.updateStep" />
  </div>
</template>

<script setup lang="ts">
import WasteReportForm from '@/components/FormulaireSignalement.vue'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrCallout } from '@gouvminint/vue-dsfr'

const store = useSignalementStore()
</script>
