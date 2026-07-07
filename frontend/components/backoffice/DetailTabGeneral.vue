<template>
  <div class="premium-box fr-p-3w fr-mb-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-user-line fr-mr-1w"></span> Général & Contact
    </h3>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Commune</span>
        <p class="fr-text--md fr-mb-1w"><strong>{{ procedure.commune }}</strong></p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Agent Constatant</span>
        <p class="fr-text--md fr-mb-1w">{{ procedure.agent }} ({{ procedure.constatant_role || 'Rôle non spécifié' }})</p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Date & Heure</span>
        <p class="fr-text--md fr-mb-1w">{{ formatConstatationDate(procedure.date_constat, procedure.heure_constat) }}</p>
      </div>
      <div class="fr-col-6">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">N° Procédure</span>
        <p class="fr-text--md fr-mb-1w"><code>#{{ procedure.id }}</code></p>
      </div>
      <div class="fr-col-12 bo-dashed-separator">
        <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Contact Collectivité</span>
        <p class="fr-text--sm fr-mb-0">
          <strong>{{ procedure.contact_prenom }} {{ procedure.contact_nom }}</strong>
          <span v-if="procedure.contact_email"> | ✉ {{ procedure.contact_email }}</span>
          <span v-if="procedure.contact_telephone"> | 📞 {{ procedure.contact_telephone }}</span>
        </p>
        <p class="fr-text--xs fr-mt-1v fr-mb-0 fr-text-mention--grey">
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
