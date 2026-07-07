<template>
  <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
    <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
      <span class="fr-icon-user-line fr-mr-1w"></span> Général & Contact
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Commune</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.commune }}</strong></p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Agent Constatant</span>
        <p class="fr-text--md fr-mb-1w">{{ procedure.agent }} ({{ procedure.constatant_role || 'Rôle non spécifié' }})</p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Date & Heure</span>
        <p class="fr-text--md fr-mb-1w">{{ formatConstatationDate(procedure.date_constat, procedure.heure_constat) }}</p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">N° Procédure</span>
        <p class="fr-text--md fr-mb-1w"><code>#{{ procedure.id }}</code></p>
      </div>
      <div class="fr-col-12" style="border-top: 1px dashed var(--border-default-grey); padding-top: 1rem">
        <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Contact Collectivité</span>
        <p class="fr-text--sm fr-mb-0">
          <strong>{{ procedure.contact_prenom }} {{ procedure.contact_nom }}</strong>
          <span v-if="procedure.contact_email"> | ✉ {{ procedure.contact_email }}</span>
          <span v-if="procedure.contact_telephone"> | 📞 {{ procedure.contact_telephone }}</span>
        </p>
        <p class="fr-text--xs fr-mt-1v fr-mb-0" style="color: var(--text-mention-grey)">
          Accompagnement souhaité : <strong>{{ procedure.accepte_accompagnement ? 'Oui' : 'Non' }}</strong>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatConstatationDate } from '@/utils/date'

defineProps<{
  procedure: any
}>()
</script>
