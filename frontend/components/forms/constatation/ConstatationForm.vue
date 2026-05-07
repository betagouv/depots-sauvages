<template>
  <div class="constatation-form">
    <SectionLocalisation />
    <SectionConstatation />
    <SectionDescription />
    <SectionAuteurDepot />
    <SectionPrejudice v-if="['Déposée', 'Sera déposée'].includes(store.formData.plainteEtat)" />
    <SectionFinalisation />
  </div>
</template>

<script setup lang="ts">
import { useConstatationStore } from '@/stores/constatation'
import SectionConstatation from './SectionConstatation.vue'
import SectionDescription from './SectionDescription.vue'
import SectionFinalisation from './SectionFinalisation.vue'
import SectionLocalisation from './SectionLocalisation.vue'
import SectionPrejudice from './SectionPrejudice.vue'
import SectionAuteurDepot from './SectionAuteurDepot.vue'

const store = useConstatationStore()
</script>

<style scoped></style>
