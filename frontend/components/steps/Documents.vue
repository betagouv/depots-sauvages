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

const actions = computed(() => {
  const baseActions = [
    {
      label: props.auteurIdentifie
        ? "Télécharger le rapport de constatation et la lettre d'information"
        : 'Télécharger le rapport de constatation',
      completed: false,
    },
    {
      label: 'Joindre les éléments de preuve et les photos au rapport de constatation',
      completed: false,
    },
    {
      label:
        "Compléter et faire signer le rapport de constatation par un agent habilité : le maire, ses adjoints ou conseillers délégués, les policiers municipaux ou gardes champêtres, les agents commissionnés et/ou assermentés de la commune ou de l'EPCI",
      completed: false,
    },
  ]

  if (props.auteurIdentifie) {
    baseActions.push({
      label:
        "Compléter et faire signer la lettre d'information par l'autorité titulaire du pouvoir de police administrative : le maire, adjoints ou conseillers par délégation, président d'EPCI par transfert de compétence",
      completed: false,
    })
  }

  return baseActions
})

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
