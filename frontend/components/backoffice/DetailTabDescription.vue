<template>
  <div class="premium-box fr-p-3w fr-mb-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-road-map-line fr-mr-1w"></span> Description du Dépôt
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Terrain</span>
        <p class="fr-text--md fr-mb-1w">
          {{ procedure.nature_terrain?.join(', ') || 'N/A' }}
          <span v-if="procedure.proprietaire_terrain_prive" class="fr-text--xs fr-text-mention--grey">
            (Propriétaire privé: {{ procedure.proprietaire_terrain_prive }})
          </span>
        </p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Volume estimé</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.volume_depot || 'Non renseigné' }}</strong></p>
      </div>
      <div class="fr-col-12">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Types de déchets</span>
        <div class="fr-mt-1v bo-flex-row-wrap">
          <span
            v-for="t in procedure.types_depot"
            :key="t"
            class="fr-tag fr-tag--sm"
          >
            {{ t }}
          </span>
          <span v-if="!procedure.types_depot?.length" class="fr-text-mention--grey">N/A</span>
        </div>
      </div>
      <div class="fr-col-12" v-if="procedure.precisions_depot">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Précisions</span>
        <p class="fr-text--sm fr-mb-1w bo-pre-wrap">{{ procedure.precisions_depot }}</p>
      </div>
      <div class="fr-col-12">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Photos disponibles</span>
        <p class="fr-text--md fr-mb-0">
          <span v-if="procedure.photo_dispo" class="fr-icon-checkbox-circle-fill fr-text-default--success"></span>
          <span v-else class="fr-icon-close-circle-fill bo-text-danger"></span>
          {{ procedure.photo_dispo ? ' Oui' : ' Non' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  procedure: any
}>()
</script>
