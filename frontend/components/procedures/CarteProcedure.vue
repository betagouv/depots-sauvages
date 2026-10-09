<template>
  <article class="carte-procedure fr-p-2w" :aria-labelledby="`carte-titre-${procedure.id}`">
    <h3 :id="`carte-titre-${procedure.id}`" class="fr-text--md fr-text--bold fr-mb-1v">
      {{ nom || placement.libelle }}
    </h3>
    <p class="fr-text--xs fr-text-mention--grey fr-mb-1w">Dossier n°{{ procedure.id }}</p>

    <p v-if="nom && placement.libelle" class="fr-mb-1w">
      <span class="fr-badge fr-badge--sm fr-badge--no-icon">{{ placement.libelle }}</span>
    </p>

    <ul class="carte-procedure__infos fr-text--sm fr-mb-1w">
      <li v-if="procedure.date_constat">
        <span class="fr-icon-calendar-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        Constat du {{ dateConstat }}
      </li>
      <li v-if="afficherCommune && procedure.commune" class="carte-procedure__lieu">
        <span class="fr-icon-map-pin-2-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        {{ procedure.commune
        }}<template v-if="procedure.localisation_depot">
          · {{ procedure.localisation_depot }}</template
        >
      </li>
      <li v-if="placement.info">
        <span class="fr-icon-time-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        {{ placement.info }}
      </li>
    </ul>

    <ul v-if="placement.alertes.length" class="carte-procedure__alertes fr-text--sm fr-mb-1w">
      <li v-for="alerte in placement.alertes" :key="alerte" class="fr-text-default--warning">
        <span class="fr-icon-warning-fill fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        <span class="fr-sr-only">Attention : </span>{{ alerte }}
      </li>
    </ul>

    <p v-if="placement.issue" class="fr-mb-1w">
      <span class="fr-tag fr-tag--sm">Issue : {{ placement.issue }}</span>
    </p>

    <router-link
      :to="placement.action.to"
      class="fr-btn fr-btn--sm"
      :class="{ 'fr-btn--secondary': placement.action.secondaire }"
    >
      {{ placement.action.label }}
      <span class="fr-sr-only"> — dossier n°{{ procedure.id }} {{ nom }}</span>
    </router-link>
  </article>
</template>

<script setup lang="ts">
import dayjs from 'dayjs'
import { computed } from 'vue'
import type { ProcedureOverview } from '../../services/api'
import { getNomContrevenant, type PlacementProcedure } from '../../utils/tableau-de-bord'

const props = defineProps<{
  procedure: ProcedureOverview
  placement: PlacementProcedure
  afficherCommune: boolean
}>()

const nom = computed(() => getNomContrevenant(props.procedure))
const dateConstat = computed(() => dayjs(props.procedure.date_constat).format('DD/MM/YYYY'))
</script>

<style scoped>
.carte-procedure {
  /* Ancre les textes réservés aux lecteurs d'écran dans la zone de défilement */
  position: relative;
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
}

.carte-procedure__infos,
.carte-procedure__alertes {
  list-style: none;
  padding-left: 0;
  margin-top: 0;
}

.carte-procedure__infos li,
.carte-procedure__alertes li {
  padding-bottom: 0.25rem;
}

.carte-procedure__lieu {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
