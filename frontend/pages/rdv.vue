<template>
  <div>
    <div class="hero-section fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Prenez rendez-vous avec Protect'Envi</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Inscrivez-vous à notre prochain webinaire pour comprendre comment mieux lutter contre les
          dépôts sauvages dans votre collectivité.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-10">
          <DsfrCard :link="anctLink" enlarge-link class="rdv-card fr-p-2w" :title="title">
            <template #title>
              <div class="fr-badges-group fr-mb-2v">
                <span class="fr-badge fr-badge--info fr-badge--sm fr-badge--no-icon">
                  <span
                    class="fr-icon-computer-line fr-icon--sm fr-mr-1v"
                    aria-hidden="true"
                  ></span>
                  PAR VISIOCONFÉRENCE
                </span>
                <span class="fr-badge fr-badge--purple-glycine fr-badge--sm fr-badge--no-icon">
                  <span class="fr-icon-team-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
                  RDV COLLECTIF
                </span>
              </div>
              <h2 class="fr-card__title fr-text--lg fr-mb-0 fr-mt-1w">
                {{ title }}
              </h2>
            </template>
          </DsfrCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr'

const title =
  "🧑‍💻 Webinaire de présentation Protect'Envi (45 min) : Comprendre comment mieux lutter contre les dépôts sauvages"
const anctLink =
  'https://rdv.anct.gouv.fr/prendre_rdv?departement=&motif_name_with_location_type=1_webinaire_de_presentation_protect_envi_45_min_comprendre_comment_mieux_lutter_contre_les_depots_sauvages-visio&public_link_organisation_id=1769'
</script>

<style scoped>
.hero-section {
  background-color: #f5f5fe;
}

.rdv-card {
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  transition:
    background-color 0.2s ease-in-out,
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
}

.rdv-card:hover {
  background-color: var(--background-alt-grey);
  transform: translateY(-4px);
  box-shadow: var(--shadow-raised-shadow);
}

.fr-card__title {
  color: var(--text-title-blue-france);
}
</style>
