<template>
  <div class="home-page">
    <DsfrCallout v-if="currentStep !== 3">
      <p>
        Ce formulaire vise à faciliter vos actions en matière de lutte contre les dépôts sauvages.
        Une fois le formulaire rempli, des documents types vous seront alors envoyés et pourront
        être joints à votre plainte (procédure pénale) et/ou au dossier de la procédure
        administrative.
      </p>
    </DsfrCallout>

    <WasteReportForm @step-change="updateStep" />
  </div>
</template>

<script setup lang="ts">
import WasteReportForm from '@/components/waste-report-form.vue'
import { ref } from 'vue'

const currentStep = ref(1)

const updateStep = (step: number) => {
  currentStep.value = step
}
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
