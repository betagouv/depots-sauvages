<template>
  <section class="colonne-procedures fr-p-1w" :aria-labelledby="`colonne-${id}`">
    <h2 :id="`colonne-${id}`" class="fr-h6 fr-mb-1w fr-px-1w">
      {{ titre }}
      <span class="fr-text--regular">({{ items.length }})</span>
    </h2>
    <ul v-if="items.length" class="colonne-procedures__liste">
      <li v-for="item in items" :key="item.procedure.id" class="fr-mb-1w">
        <CarteProcedure
          :procedure="item.procedure"
          :placement="item.placement"
          :afficher-commune="afficherCommune"
        />
      </li>
    </ul>
    <p v-else class="fr-text--sm fr-text-mention--grey fr-px-1w">Aucun dossier</p>
  </section>
</template>

<script setup lang="ts">
import type { ProcedureOverview } from '../../services/api'
import type { PlacementProcedure } from '../../utils/tableau-de-bord'
import CarteProcedure from './CarteProcedure.vue'

defineProps<{
  id: string
  titre: string
  items: { procedure: ProcedureOverview; placement: PlacementProcedure }[]
  afficherCommune: boolean
}>()
</script>

<style scoped>
.colonne-procedures {
  background-color: var(--background-alt-grey);
  height: 100%;
}

.colonne-procedures__liste {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
</style>
