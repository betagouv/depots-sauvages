<template>
  <div>
    <div class="hero-section fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              Rejoindre le dispositif Stop Dépôt Sauvage
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center fr-mb-0">
              Vous êtes une collectivité touchée par les dépôts sauvages et vous souhaitez agir ?
              Stop Dépôt Sauvage peut vous aider, complétez ce formulaire pour rejoindre le
              dispositif.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="fr-container fr-my-4w">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
          <iframe
            :data-tally-src="tallySrc"
            loading="lazy"
            width="100%"
            height="600"
            frameborder="0"
            marginheight="0"
            marginwidth="0"
            title="Formulaire pour rejoindre le dispositif Stop Dépôt Sauvage"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { loadTallyEmbeds } from '@/utils/tally'

const tallySrc =
  'https://tally.so/embed/PdoNQe?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1'

onMounted(() => {
  loadTallyEmbeds()
})
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}
</style>
