<template>
  <main class="home-page">
    <div class="fr-container">
      <h1 class="fr-h2">Signalement de dépôts sauvages</h1>
      <DsfrCallout v-if="store.currentStep !== 3">
        <p>
          Ce formulaire vise à faciliter vos actions en matière de lutte contre les dépôts sauvages.
          Une fois le formulaire rempli, des documents types vous seront alors envoyés et pourront
          être joints à votre plainte (procédure pénale) et/ou au dossier de la procédure
          administrative.
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
