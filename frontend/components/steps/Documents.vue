<template>
  <div class="documents-integration">
    <DnBandeauAccueil :has-procedure="hasProcedure" :auteur-identifie="auteurIdentifie" />

    <div class="fr-mt-2w">
      <DnDocuments
        v-if="hasProcedure"
        :auteur-identifie="auteurIdentifie"
        :doc-constat-url="docConstatUrl"
        :lettre-info-url="lettreInfoUrl"
      />

      <div v-else class="fr-mb-4w">
        <p class="">
          Pour récupérer vos documents, merci de
          <a
            :href="modifyUrl"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
            rel="noopener noreferrer"
            >mettre à jour votre dossier sur la plateforme Démarches Numériques</a
          >.
        </p>
        <DsfrAlert
          type="info"
          title="Note"
          description="Les formulaires de Protect’Envi évoluent régulièrement. Si vous avez rempli une version antérieure, une mise à jour de certaines informations peut être nécessaire pour accéder à vos documents."
          small
        />
      </div>

      <div v-if="hasProcedure" class="fr-mb-4w fr-mt-4w">
        <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire</h4>
        <ListeActions
          step-id="constat-documents"
          :actions="actions"
          @updateCase="(action, val) => (action.completed = val)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

import DnBandeauAccueil from '../dn/DnBandeauAccueil.vue'
import DnDocuments from '../dn/DnDocuments.vue'
import ListeActions from './ListeActions.vue'

const actions = computed(() => [
  {
    label: props.auteurIdentifie
      ? "Numériser et conserver les éléments d'identification de l'auteur et de constat du dépôt"
      : 'Numériser et conserver les éléments de constat du dépôt',
    completed: false,
  },
  {
    label: props.auteurIdentifie
      ? "Télécharger, compléter le rapport de constatation et la lettre d'information"
      : 'Télécharger et compléter le rapport de constatation',
    completed: false,
  },
  {
    label:
      "Signer ou faire signer par l'autorité compétente : maire, adjoint par délégation, ou président d'EPCI par transfert de compétence",
    completed: false,
  },
])

const props = defineProps<{
  dossierData: any
  hasProcedure: boolean
  auteurIdentifie: boolean
  docConstatUrl: string
  lettreInfoUrl: string
  modifyUrl: string
}>()
</script>

<style scoped>
.documents-integration :deep(.fr-container) {
  padding-left: 0;
  padding-right: 0;
  margin-left: 0;
  margin-right: 0;
  max-width: 100%;
}

.documents-integration :deep(.hero-section) {
  margin-bottom: 1rem;
}

.documents-integration :deep(.hero-section) {
  margin-bottom: 1rem;
}
</style>
