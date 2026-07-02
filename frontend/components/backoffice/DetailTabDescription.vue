<template>
  <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
    <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
      <span class="fr-icon-road-map-line fr-mr-1w"></span> Description du Dépôt
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Terrain</span>
        <p class="fr-text--md fr-mb-1w">
          {{ procedure.nature_terrain?.join(', ') || 'N/A' }}
          <span v-if="procedure.proprietaire_terrain_prive" class="fr-text--xs" style="color: var(--text-mention-grey)">
            (Propriétaire privé: {{ procedure.proprietaire_terrain_prive }})
          </span>
        </p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Volume estimé</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.volume_depot || 'Non renseigné' }}</strong></p>
      </div>
      <div class="fr-col-12">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Types de déchets</span>
        <div class="fr-mt-1v" style="display: flex; flex-wrap: wrap; gap: 0.35rem">
          <span
            v-for="t in procedure.types_depot"
            :key="t"
            class="fr-tag fr-tag--sm"
          >
            {{ t }}
          </span>
          <span v-if="!procedure.types_depot?.length" style="color: var(--text-mention-grey)">N/A</span>
        </div>
      </div>
      <div class="fr-col-12" v-if="procedure.precisions_depot">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Précisions</span>
        <p class="fr-text--sm fr-mb-1w" style="white-space: pre-wrap">{{ procedure.precisions_depot }}</p>
      </div>
      <div class="fr-col-12">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Photos disponibles</span>
        <p class="fr-text--md fr-mb-0">
          <span v-if="procedure.photo_dispo" class="fr-icon-checkbox-circle-fill" style="color: #22C55E"></span>
          <span v-else class="fr-icon-close-circle-fill" style="color: #EF4444"></span>
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
