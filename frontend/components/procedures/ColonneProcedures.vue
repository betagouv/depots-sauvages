<template>
  <section
    class="colonne-procedures fr-p-1w"
    :data-colonne-id="id"
    :aria-labelledby="`colonne-${id}`"
  >
    <h2 :id="`colonne-${id}`" class="colonne-procedures__entete fr-h6 fr-mb-1w fr-px-1w">
      {{ titre }}
      <span class="fr-text--regular">({{ items.length }})</span>
    </h2>
    <ul v-if="items.length" class="colonne-procedures__liste">
      <li v-for="item in items" :key="item.procedure.id" class="fr-mb-1w">
        <CarteProcedure :procedure="item.procedure" :placement="item.placement" />
      </li>
    </ul>
    <p v-else class="fr-text--sm fr-text-mention--grey fr-px-1w fr-mb-0">Aucun dossier</p>
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
}>()
</script>

<style scoped>
.colonne-procedures {
  display: flex;
  flex-direction: column;
  background-color: var(--background-alt-grey);
  border-radius: 0.25rem;
  max-height: 100%;
}

.colonne-procedures__entete {
  flex: 0 0 auto;
}

.colonne-procedures__liste {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  list-style: none;
  padding-left: 0;
  padding-right: 0.25rem;
  margin: 0;
  scrollbar-width: thin;
}

.colonne-procedures__liste > li:last-child {
  margin-bottom: 0;
}
</style>
