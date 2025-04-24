<template>
  <main class="home-page">
    <div class="fr-container">
      <h1 class="fr-h2">Signalement de dépôts sauvages</h1>
      <DsfrCallout v-if="store.currentStep !== 3">
        <p>
          Ce formulaire vise à vous accompagner lorsque vous devez traiter un dépôt sauvage. Une fois le formulaire rempli, un rapport de constatation personnalisé sera généré pour vous permettre d’initier une procédure administrative et faciliter un éventuel dépôt de plainte. Des conseils vous seront aussi proposés pour la suite des procédures.
        </p>
      </DsfrCallout>

      <WasteReportForm @step-change="store.updateStep" />
    </div>
  </main>
</template>

<script setup lang="ts">
import WasteReportForm from '@/components/waste-report-form.vue'
import { useSignalementStore } from '@/stores/signalement'

const store = useSignalementStore()
</script>

<style scoped>
.home-page {
  max-width: 1000px;
  margin: 0 auto;
}

.fr-callout {
  margin-bottom: 2rem;
}
</style>
