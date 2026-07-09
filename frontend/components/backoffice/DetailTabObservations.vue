<template>
  <div
    v-if="
      procedure.suivi_procedure?.observations_internes || procedure.suivi_procedure?.nettoyage_fait
    "
    class="premium-box fr-p-3w fr-mb-3w bo-card"
  >
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-clipboard-line fr-mr-1w"></span> Observations de la collectivité
    </h3>
    <div v-if="procedure.suivi_procedure?.nettoyage_fait !== null" class="fr-mb-2w fr-text--xs">
      <strong>Nettoyage :</strong>
      {{ procedure.suivi_procedure?.nettoyage_fait ? 'Effectué' : 'Non effectué' }}
      <span
        v-if="procedure.suivi_procedure?.nettoyage_fait && procedure.suivi_procedure?.nettoyage_par"
      >
        (par :
        {{
          procedure.suivi_procedure.nettoyage_par === 'mairie'
            ? 'la collectivité'
            : procedure.suivi_procedure.nettoyage_par === 'auteur'
              ? "l'auteur"
              : procedure.suivi_procedure.nettoyage_par
        }})
      </span>
    </div>
    <div v-if="procedure.suivi_procedure?.observations_internes">
      <strong class="fr-text--xs">Observations :</strong>
      <p class="bo-obs-text fr-mb-0">
        {{ procedure.suivi_procedure.observations_internes }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  procedure: any
}>()
</script>
