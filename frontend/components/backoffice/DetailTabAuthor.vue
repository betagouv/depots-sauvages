<template>
  <div class="premium-box fr-p-3w fr-mb-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-user-search-line fr-mr-1w"></span> Auteur Présumé & Indices
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Auteur identifié</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.auteur_identifie ? 'Oui' : 'Non présumé' }}</strong></p>
      </div>
      <div class="fr-col-6" v-if="procedure.statut_auteur">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Statut auteur</span>
        <p class="fr-text--md fr-mb-1w">{{ procedure.statut_auteur }}</p>
      </div>
      <div class="fr-col-12" v-if="procedure.auteur_nom || procedure.auteur_prenom">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Identité auteur</span>
        <p class="fr-text--md fr-mb-1w">
          <strong>{{ procedure.auteur_civilite }} {{ procedure.auteur_prenom }} {{ procedure.auteur_nom }}</strong>
          <span v-if="procedure.auteur_siret"> (SIRET: {{ procedure.auteur_siret }})</span>
          <span v-if="procedure.entreprise_francaise !== null" class="fr-text--xs fr-text-mention--grey">
            - {{ procedure.entreprise_francaise ? 'Entreprise française' : 'Entreprise étrangère' }}
          </span>
        </p>
      </div>
      <div class="fr-col-12" v-if="procedure.auteur_adresse">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Adresse auteur</span>
        <p class="fr-text--sm fr-mb-1w">{{ procedure.auteur_adresse }}</p>
      </div>
      <div class="fr-col-12 bo-dashed-separator">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Indices trouvés sur place</span>
        <div class="fr-mt-1v fr-mb-1w bo-flex-row-wrap">
          <span
            v-for="idx in procedure.indices_disponibles"
            :key="idx"
            class="fr-tag fr-tag--sm"
          >
            {{ idx }}
          </span>
          <span v-if="!procedure.indices_disponibles?.length" class="fr-text-mention--grey">Aucun indice</span>
        </div>
        <p class="fr-text--sm fr-mb-0 bo-pre-wrap" v-if="procedure.precisions_indices">
          {{ procedure.precisions_indices }}
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
