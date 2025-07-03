<template>
  <div class="fr-container--sm fr-mb-3w">
    <DsfrStepper
      :title="'Signalement d\'un dépôt sauvage'"
      :steps="STEPS"
      :current-step="store.currentStep"
    />

    <div class="fr-container--fluid" :class="{ 'fr-text--center': isLastStep }">
      <div class="fr-container--sm">
        <Etape1 v-if="store.currentStep === 1" />
        <Etape2 v-if="store.currentStep === 2" />
        <Etape3 v-if="store.currentStep === 3" />
        <Etape4 v-if="store.currentStep === 4" />
        <Etape5 v-if="store.currentStep === 5" @restart="resetForm" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useScroll } from '@/composables/useScroll'
import { computed, nextTick, watch } from 'vue'
import { useSignalementStore } from '../stores/signalement'
import { STEPS } from './etapes-formulaire/form-data'
import Etape1 from './etapes-formulaire/Etape1.vue'
import Etape2 from './etapes-formulaire/Etape2.vue'
import Etape3 from './etapes-formulaire/Etape3.vue'
import Etape4 from './etapes-formulaire/Etape4.vue'
import Etape5 from './etapes-formulaire/Etape5.vue'

const store = useSignalementStore()
const isLastStep = computed(() => store.currentStep === STEPS.length)
const { scrollToTop } = useScroll()

// Watch for step changes and scroll to top
watch(
  () => store.currentStep,
  async () => {
    await nextTick()
    // petit délai pour Safari
    setTimeout(() => {
      scrollToTop()
    }, 30)
  }
)

const resetForm = () => {
  store.resetStore()
  scrollToTop()
}

defineEmits(['stepChange'])
</script>

<style scoped></style>
