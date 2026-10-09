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
        <p v-if="procedure.contact_prenom || procedure.contact_nom" class="fr-text--sm fr-mb-0">
          <strong>{{ procedure.contact_prenom }} {{ procedure.contact_nom }}</strong>
        </p>
        <div class="fr-grid-row fr-grid-row--gutters fr-mt-0">
          <div class="fr-col-6">
            <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Email</span>
            <p class="fr-text--sm fr-mb-0" data-testid="contact-email">
              <a v-if="contactEmail" :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
              <em v-else class="bo-text-non-renseigne">Non renseigné</em>
            </p>
          </div>
          <div class="fr-col-6">
            <span class="fr-text--xs fr-mb-0 bo-text-mention-uppercase">Téléphone</span>
            <p class="fr-text--sm fr-mb-0" data-testid="contact-telephone">
              <a v-if="procedure.contact_telephone" :href="`tel:${procedure.contact_telephone}`">{{
                procedure.contact_telephone
              }}</a>
              <em v-else class="bo-text-non-renseigne">Non renseigné</em>
            </p>
          </div>
        </div>
        <p v-if="procedure.besoin_accompagnement" class="fr-mb-0 fr-mt-1w">
          <span class="fr-badge fr-badge--sm fr-badge--info">Accompagnement demandé</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { formatConstatationDate } from '@/utils/date'

const props = defineProps<{
  procedure: any
}>()

// L'email du compte est la source fiable (contact_email n'est plus saisi dans le formulaire)
const contactEmail = computed(() => props.procedure.user_email || props.procedure.contact_email)
</script>

<style scoped>
.bo-text-non-renseigne {
  color: var(--text-mention-grey);
}
</style>
