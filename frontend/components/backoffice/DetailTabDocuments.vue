<template>
  <div class="premium-box fr-p-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
    <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
      <span class="fr-icon-file-pdf-line fr-mr-1w"></span> Documents de la Procédure
    </h3>
    <div style="display: flex; flex-direction: column; gap: 1rem">
      <!-- Rapport de constatation -->
      <div class="fr-p-1w" style="display: flex; justify-content: space-between; align-items: center; background: var(--background-alt-grey); border-radius: 6px">
        <div>
          <p class="fr-text--sm fr-mb-0"><strong>Rapport de constatation</strong></p>
          <p class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey)">
            Généré le : {{ formatDate(procedure.doc_constat_generated_at) }}
          </p>
        </div>
        <a
          v-if="procedure.doc_constat_generated_at"
          :href="`/api/constatations/${procedure.id}/documents/doc_constat/`"
          target="_blank"
          class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
        >
          Télécharger
        </a>
        <span v-else class="fr-text--xs" style="color: var(--text-mention-grey)">Non généré</span>
      </div>

      <!-- Lettre d'information -->
      <div class="fr-p-1w" style="display: flex; justify-content: space-between; align-items: center; background: var(--background-alt-grey); border-radius: 6px">
        <div>
          <p class="fr-text--sm fr-mb-0"><strong>Lettre d'information</strong></p>
          <p class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey)">
            Généré le : {{ formatDate(procedure.lettre_info_generated_at) }}
          </p>
        </div>
        <a
          v-if="procedure.lettre_info_generated_at"
          :href="`/api/constatations/${procedure.id}/documents/lettre_info/`"
          target="_blank"
          class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
        >
          Télécharger
        </a>
        <span v-else class="fr-text--xs" style="color: var(--text-mention-grey)">Non générée</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/utils/backoffice'

defineProps<{
  procedure: any
}>()
</script>
