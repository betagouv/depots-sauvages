<template>
  <div class="premium-box fr-p-3w fr-mb-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-money-euro-box-line fr-mr-1w"></span> Évaluation du Préjudice Financier
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">État de la plainte</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.plainte_etat || 'Aucune plainte' }}</strong></p>
      </div>
      <div class="fr-col-6 fr-text--right">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Montant total du préjudice</span>
        <p class="fr-h4 fr-mb-0" :class="procedure.prejudice_montant ? 'bo-text-danger' : 'fr-text-mention--grey'">
          {{ procedure.prejudice_montant !== null && procedure.prejudice_montant !== undefined ? `${procedure.prejudice_montant.toLocaleString('fr-FR')} €` : (['Déposée', 'Sera déposée'].includes(procedure.plainte_etat) ? 'Calcul en cours' : '0 €') }}
        </p>
      </div>

      <div class="fr-col-12 bo-dashed-separator">
        <div class="fr-grid-row fr-grid-row--gutters fr-text--xs">
          <div class="fr-col-4">
            <span class="fr-text-mention--grey">Agents</span>
            <p class="fr-text--sm fr-mb-0 fr-text--bold">{{ procedure.prejudice_nombre_personnes || 0 }}</p>
          </div>
          <div class="fr-col-4">
            <span class="fr-text-mention--grey">Heures</span>
            <p class="fr-text--sm fr-mb-0 fr-text--bold">{{ procedure.prejudice_nombre_heures || 0 }}</p>
          </div>
          <div class="fr-col-4">
            <span class="fr-text-mention--grey">Véhicules</span>
            <p class="fr-text--sm fr-mb-0 fr-text--bold">{{ procedure.prejudice_nombre_vehicules || 0 }}</p>
          </div>
          <div class="fr-col-4">
            <span class="fr-text-mention--grey">Kilomètres</span>
            <p class="fr-text--sm fr-mb-0 fr-text--bold">{{ procedure.prejudice_kilometrage || 0 }}</p>
          </div>
          <div class="fr-col-8">
            <span class="fr-text-mention--grey">Autres coûts</span>
            <p class="fr-text--sm fr-mb-0 fr-text--bold">{{ procedure.prejudice_autres_couts ? `${procedure.prejudice_autres_couts} €` : '0 €' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  procedure: any
}>()
</script>
