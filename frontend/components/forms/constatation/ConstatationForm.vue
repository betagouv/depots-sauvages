<template>
  <div class="constatation-form">
    <SectionLocalisation />
    <SectionConstatation />
    <SectionDescription />
    <SectionResponsable />
    <SectionPrejudice />
    <SectionFinalisation />
  </div>
</template>

<script setup lang="ts">
import SectionConstatation from './SectionConstatation.vue'
import SectionDescription from './SectionDescription.vue'
import SectionFinalisation from './SectionFinalisation.vue'
import SectionLocalisation from './SectionLocalisation.vue'
import SectionPrejudice from './SectionPrejudice.vue'
import SectionResponsable from './SectionResponsable.vue'
</script>

<style scoped></style>
