<template>
  <div>
    <!-- Bandeau Webinaire -->
    <DsfrNotice
      title="Prochain webinaire de : jeudi 23 juillet à 11h00 — une heure pour comprendre la procédure et poser vos questions."
      :closeable="false"
      class="fr-mb-0"
    >
      <template #desc>
        <router-link to="/rdv" class="fr-link fr-ml-1w"> S'inscrire au webinaire </router-link>
      </template>
    </DsfrNotice>

    <AccueilHero />
    <AccueilOrientation />
    <AccueilPouvoirAgir />
    <AccueilReassurance />
    <AccueilTemoignages />
    <AccueilStats />
    <AccueilCta />
  </div>
</template>

<script setup lang="ts">
import { useTallyRoutes } from '@/composables/useTally'
import { DsfrNotice } from '@gouvminint/vue-dsfr'
import AccueilHero from '@/components/accueil/AccueilHero.vue'
import AccueilOrientation from '@/components/accueil/AccueilOrientation.vue'
import AccueilPouvoirAgir from '@/components/accueil/AccueilPouvoirAgir.vue'
import AccueilReassurance from '@/components/accueil/AccueilReassurance.vue'
import AccueilTemoignages from '@/components/accueil/AccueilTemoignages.vue'
import AccueilStats from '@/components/accueil/AccueilStats.vue'
import AccueilCta from '@/components/accueil/AccueilCta.vue'

useTallyRoutes({
  '/simulateur': { formId: 'A7xA8z', options: { layout: 'modal', width: 900 } },
  '/calculateur': { formId: '9qElYG', options: { layout: 'modal', width: 900 } },
})
</script>

<style scoped>
</style>
