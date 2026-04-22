<template>
  <div class="documents-integration">
    <BandeauInformation :has-procedure="hasProcedure" :auteur-identifie="auteurIdentifie" />

    <div class="fr-mt-2w">
      <CartesDocuments
        :auteur-identifie="auteurIdentifie"
        :doc-constat-url="docConstatUrl"
        :lettre-info-url="lettreInfoUrl"
      />

      <div class="fr-mb-4w fr-mt-4w">
        <h4 class="fr-h6 fr-mb-2w">Ce qu'il vous reste à faire :</h4>
        <ListeActions step-id="constat-documents" :actions="actions" @update-case="onUpdateCase" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { SuiviProcedure } from '../../stores/suivi-procedure'
import BandeauInformation from '../dossiers/BandeauInformation.vue'
import CartesDocuments from '../dossiers/CartesDocuments.vue'
import ListeActions, { type Action } from './ListeActions.vue'

const props = defineProps<{
  suivi: SuiviProcedure
  hasProcedure: boolean
  auteurIdentifie: boolean
  docConstatUrl: string
  lettreInfoUrl: string
  modifyUrl: string
}>()

const actions = computed((): Action[] => {
  const baseActions: Action[] = [
    {
      id: 'preuve_photos',
      label: 'Joindre les éléments de preuve et les photos au rapport de constatation',
      completed: props.suivi.preuves_fournies,
    },
    {
      id: 'rapport_signe',
      label:
        (props.auteurIdentifie ? '' : 'Compléter et ') +
        "<strong>Faire signer le rapport de constatation</strong> par un agent habilité : le maire, ses adjoints ou conseillers délégués, les policiers municipaux ou gardes champêtres, les agents commissionnés et/ou assermentés de la commune ou de l'EPCI",
      completed: props.suivi.constatation_signee,
    },
  ]

  if (props.auteurIdentifie) {
    baseActions.push({
      id: 'lettre_signee',
      label:
        "<strong>Faire signer la lettre d'information</strong> par l'autorité titulaire du pouvoir de police administrative : le maire, adjoints ou conseillers par délégation, président d'EPCI par transfert de compétence",
      completed: props.suivi.lettre_signe,
    })
  }

  return baseActions
})

const onUpdateCase = (action: Action, val: boolean) => {
  switch (action.id) {
    case 'preuve_photos':
      props.suivi.preuves_fournies = val
      break
    case 'rapport_signe':
      props.suivi.constatation_signee = val
      break
    case 'lettre_signee':
      props.suivi.lettre_signe = val
      break
  }
}

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
</style>
