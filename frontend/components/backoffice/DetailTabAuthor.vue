<template>
  <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
    <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
      <span class="fr-icon-user-search-line fr-mr-1w"></span> Auteur Présumé & Indices
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Auteur identifié</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.auteur_identifie ? 'Oui' : 'Non présumé' }}</strong></p>
      </div>
      <div class="fr-col-6" v-if="procedure.statut_auteur">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Statut auteur</span>
        <p class="fr-text--md fr-mb-1w">{{ procedure.statut_auteur }}</p>
      </div>
      <div class="fr-col-12" v-if="procedure.auteur_nom || procedure.auteur_prenom">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Identité auteur</span>
        <p class="fr-text--md fr-mb-1w">
          <strong>{{ procedure.auteur_civilite }} {{ procedure.auteur_prenom }} {{ procedure.auteur_nom }}</strong>
          <span v-if="procedure.auteur_siret"> (SIRET: {{ procedure.auteur_siret }})</span>
          <span v-if="procedure.entreprise_francaise !== null" class="fr-text--xs" style="color: var(--text-mention-grey)">
            - {{ procedure.entreprise_francaise ? 'Entreprise française' : 'Entreprise étrangère' }}
          </span>
        </p>
      </div>
      <div class="fr-col-12" v-if="procedure.auteur_adresse">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Adresse auteur</span>
        <p class="fr-text--sm fr-mb-1w">{{ procedure.auteur_adresse }}</p>
      </div>
      <div class="fr-col-12" style="border-top: 1px dashed var(--border-default-grey); padding-top: 1rem">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Indices trouvés sur place</span>
        <div class="fr-mt-1v fr-mb-1w" style="display: flex; flex-wrap: wrap; gap: 0.35rem">
          <span
            v-for="idx in procedure.indices_disponibles"
            :key="idx"
            class="fr-tag fr-tag--sm"
          >
            {{ idx }}
          </span>
          <span v-if="!procedure.indices_disponibles?.length" style="color: var(--text-mention-grey)">Aucun indice</span>
        </div>
        <p class="fr-text--sm fr-mb-0" v-if="procedure.precisions_indices" style="white-space: pre-wrap">
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
