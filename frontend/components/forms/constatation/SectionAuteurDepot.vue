<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h3 class="fr-h2">4. Identification de l'auteur présumé du dépôt</h3>
    </legend>

    <div class="fr-fieldset__element">
      <BooleanRadioSet
        v-model="store.formData.auteurIdentifie"
        legend="L'auteur présumé des faits est-il identifié ou identifiable partiellement ?"
        hint="Indiquer NON uniquement s'il n'y a absolument rien qui permettrait d'identifier l'auteur présumé."
        id-prefix="auteur-identifie"
        :required="true"
      />
    </div>

    <!-- IDENTIFIED FLOW -->
    <template v-if="store.formData.auteurIdentifie">
      <div class="fr-fieldset__element">
        <DsfrCallout title="Comment identifier l'auteur présumé ?">
          <p>
            L'auteur présumé peut être celui qui a déposé les déchets, mais aussi le détenteur ou le
            producteur de ces déchets.
          </p>
          <p>
            Un nom sur un colis ou une facture peut permettre d'identifier quelqu'un et suffit par
            exemple à initier une procédure administrative.
          </p>
          <p>
            La mairie peut effectuer des recherches complémentaires (source ouverte, témoignages,
            etc.) mais ne bénéficie pas de pouvoirs d'enquête judiciaire.
          </p>
        </DsfrCallout>
      </div>

      <div class="fr-fieldset__element">
        <DsfrRadioButtonSet
          v-model="store.formData.statutAuteur"
          legend="S'agit-il d'une entreprise ou d'un particulier ?"
          :required="true"
          :options="[
            { label: 'Entreprise', value: 'Entreprise', id: 'statut-entreprise' },
            { label: 'Particulier', value: 'Particulier', id: 'statut-particulier' },
          ]"
        />
      </div>

      <!-- SECTION ENTREPRISE -->
      <template v-if="store.formData.statutAuteur === 'Entreprise'">
        <div class="fr-fieldset__element">
          <DsfrCallout
            title="Avec un auteur présumé identifié, vous pouvez débuter une procédure administrative."
          >
            <p>
              Le maire ou l'adjoint par délégation, ou le président d'EPCI par transfert de compétence
              peut engager une <strong>procédure administrative</strong> (article L.541-3 du Code de
              l'environnement).
            </p>
            <p>
              Elle permet de <strong>sanctionner efficacement</strong> les auteurs présumés, avec une
              <strong>amende pouvant aller jusqu'à 15 000 €</strong>, recouvrée au profit de la
              mairie.
            </p>
            <p>
              Plus d'informations sur :
              <a
                href="https://protect-envi.beta.gouv.fr/comprendre-la-procedure"
                target="_blank"
                rel="noopener noreferrer"
                >https://protect-envi.beta.gouv.fr/comprendre-la-procedure</a
              >
            </p>
          </DsfrCallout>
        </div>

        <div class="fr-fieldset__element">
          <BooleanRadioSet
            v-model="store.formData.entrepriseFrancaise"
            legend="S'agit-il d'une entreprise française ?"
            id-prefix="entreprise-francaise"
            :required="true"
          />
        </div>

        <div class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.auteurNom"
            :required="true"
            label="Nom de l'entreprise présumée auteur du dépôt"
          />
        </div>

        <div v-if="store.formData.entrepriseFrancaise === true" class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.auteurSiret"
            label="Numéro SIRET de l'entreprise présumée auteur"
            hint="Pour trouver le numéro SIRET d'une entreprise vous pouvez utiliser https://annuaire-entreprises.data.gouv.fr/. Format attendu : 14 chiffres."
          />
        </div>

        <div v-if="store.formData.entrepriseFrancaise === false" class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.auteurAdresse"
            :is-textarea="true"
            label="Adresse postale complète de l'entreprise étrangère"
            hint="Merci de préciser le pays"
          />
        </div>

        <div class="fr-fieldset__element fr-mt-2w">
          <BooleanRadioSet
            v-model="store.formData.arreteSuppressionPris"
            legend="Avez-vous pris un arrêté municipal ordonnant la suppression du dépôt ? *"
            id-prefix="arrete-suppression"
            :required="true"
          />
        </div>

        <div v-if="store.formData.arreteSuppressionPris === true" class="fr-fieldset__element">
          <DsfrCallout title="Merci de joindre cet arrêté à votre démarche">
            <p>
              Le rapport de constatation que vous allez générer viendra en appui de cet arrêté pour
              justifier la procédure administrative.
            </p>
          </DsfrCallout>
        </div>

        <div v-if="store.formData.arreteSuppressionPris === false" class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.arreteSuppressionPourquoi"
            :is-textarea="true"
            :required="true"
            label="Merci de nous préciser pourquoi vous ne l'avez pas fait."
          />
        </div>
      </template>

      <!-- SECTION PARTICULIER -->
      <template v-if="store.formData.statutAuteur === 'Particulier'">
        <div class="fr-fieldset__element">
          <DsfrCheckboxSet
            v-model="store.formData.informationsAuteur"
            legend="De quelles informations disposez vous sur l'auteur présumé des faits ?"
            hint="Vous pouvez sélectionner un ou plusieurs choix."
            :required="true"
            :options="InfoAuteurOptions"
          />
        </div>

        <!-- CALLOUTS PARTICULIER -->
        <div v-if="hasInfo('Nom et prénom') && hasInfo('Adresse postale')" class="fr-fieldset__element">
          <DsfrCallout
            title="Avec le nom/prénom et l'adresse postale vous disposez de l'identité complète"
          >
            <p>
              Dans le cas où vous avez bien le nom/prénom ET l'adresse postale vous disposez de
              l'identité complète nécessaire à la procédure administrative.
            </p>
          </DsfrCallout>
        </div>

        <div v-else-if="hasInfo('Nom et prénom') && !hasInfo('Adresse postale')" class="fr-fieldset__element">
          <DsfrCallout title="Vous avez le nom et le prénom mais vous n'avez pas l'adresse">
            <p>
              Sans l'identité complète de l'auteur présumé, la procédure administrative ne peut pas être
              initiée.
            </p>
            <p>
              En tant qu'OPJ, le maire peut demander la communication de l'adresse de l'auteur présumé
              au procureur de la République.
            </p>
          </DsfrCallout>
        </div>

        <div v-else-if="hasInfo('Plaque d\'immatriculation') && !hasInfo('Nom et prénom') && !hasInfo('Adresse postale')" class="fr-fieldset__element">
          <DsfrCallout title="Rapprochez vous de la gendarmerie ou du commissariat pour obtenir l'identité">
            <p>
              La gendarmerie peut communiquer à la police municipale les informations du SIV
              (système d'immatriculation des véhicules).
            </p>
          </DsfrCallout>
        </div>

        <!-- FIELDS PARTICULIER -->
        <div v-if="hasInfo('Nom et prénom')" class="fr-fieldset__element">
          <DsfrRadioButtonSet
            v-model="store.formData.auteurCivilite"
            legend="Civilité de l'auteur présumé"
            :required="true"
            :options="CiviliteOptions"
          />
        </div>
        <div v-if="hasInfo('Nom et prénom')" class="fr-fieldset__row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="store.formData.auteurNom"
              :required="true"
              label="Nom de famille de l'auteur présumé"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="store.formData.auteurPrenom"
              label="Prénom de l'auteur présumé"
            />
          </div>
        </div>
        <div v-if="hasInfo('Adresse postale')" class="fr-fieldset__element">
          <AddressAutocomplete
            v-model="store.formData.auteurAdresse"
            label="Adresse postale de l'auteur présumé"
          />
        </div>
      </template>
    </template>

    <!-- NOT IDENTIFIED FLOW (Specific Info) -->
    <template v-else>
      <div class="fr-fieldset__element">
        <DsfrCallout title="Comment identifier l'auteur présumé ?">
          <p>
            L'auteur présumé peut être celui qui a déposé les déchets, mais aussi le détenteur ou le
            producteur de ces déchets.
          </p>
          <p>
            Un nom sur un colis ou une facture peut permettre d'identifier quelqu'un et suffit par
            exemple à initier une procédure administrative.
          </p>
          <p>
            La mairie peut effectuer des recherches complémentaires (source ouverte, témoignages,
            etc.) mais ne bénéficie pas de pouvoirs d'enquête judiciaire.
          </p>
        </DsfrCallout>
      </div>

      <div class="fr-callout fr-mb-2w fr-callout--blue-cumulus">
        <h3 class="fr-callout__title">
          Sans l'identité complète de l'auteur présumé, la procédure administrative ne peut pas être
          initiée.
        </h3>
        <p class="fr-callout__text">
          Vous pouvez cependant déposer plainte en brigade ou commissariat pour initier une
          procédure judiciaire. En cas d’identification de l'auteur présumé, la communication de l’identité pourra être sollicitée auprès du procureur de la République.
        </p>
        <p class="fr-callout__text">
          Continuez cette démarche afin de générer un rapport de constatation pour matérialiser les faits et appuyer votre dépôt de plainte.
        </p>
      </div>
    </template>

    <!-- PLAINTE SECTION (TRIGGERED IF INCOMPLETE OR NOT IDENTIFIED) -->
    <div v-if="showPlainteSection" class="fr-fieldset__element fr-mt-2w">
      <DsfrRadioButtonSet
        v-model="store.formData.plainteEtat"
        legend="Un dépôt de plainte est indispensable pour espérer obtenir une identification de l'auteur présumé :"
        :required="true"
        :options="PlainteOptions"
      />
    </div>

    <!-- COMMON SECTION (Indices/Moyens) - ALWAYS VISIBLE -->
    <div class="fr-fieldset__element">
      <DsfrCheckboxSet
        v-model="store.formData.indicesDisponibles"
        legend="Par quels moyens l'auteur présumé peut-il être identifié ?"
        hint="Vous pouvez sélectionner un ou plusieurs choix."
        :options="IndicesOptions"
      />
    </div>

    <div class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.precisionsIndices"
        :is-textarea="true"
        :required="true"
        label="Ajoutez les éléments qui permettraient d'identifier l'auteur présumé"
        hint='Exemple : 
"Nous constatons la présence des colis et des factures qui ont été retrouvés dans le dépôts sur lesquels est indiqué l’identité d’une personne"
"Un voisin témoin de la scène a pu relever la plaque d’immatriculation du véhicule"
"Aucun élément ne permet d’identifier l’auteur présumé"'
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import AddressAutocomplete from '@/components/shared/AddressAutocomplete.vue'
import BooleanRadioSet from '@/components/shared/BooleanRadioSet.vue'
import { useConstatationStore } from '@/stores/constatation'
import {
  CiviliteOptions,
  IndicesOptions,
  InfoAuteurOptions,
  PlainteOptions,
} from '@/types/constatation'
import {
  DsfrCallout,
  DsfrCheckboxSet,
  DsfrInputGroup,
  DsfrRadioButtonSet,
} from '@gouvminint/vue-dsfr'
import { computed, watch } from 'vue'

const store = useConstatationStore()

const hasInfo = (info: string) => {
  const infos = store.formData.informationsAuteur || []
  return infos.includes(info as any)
}

watch(
  () => store.formData.informationsAuteur,
  (newVal, oldVal) => {
    if (!newVal) return
    const info = newVal as string[]
    const oldInfo = (oldVal || []) as string[]

    if (info.includes('Aucune') && !oldInfo.includes('Aucune')) {
      store.formData.informationsAuteur = ['Aucune'] as any
    } else if (info.length > 1 && info.includes('Aucune')) {
      store.formData.informationsAuteur = info.filter((i) => i !== 'Aucune') as any
    }
  },
)

const showPlainteSection = computed(() => {
  if (!store.formData.auteurIdentifie) return true

  if (store.formData.statutAuteur === 'Particulier') {
    const info = store.formData.informationsAuteur || []
    if (info.includes('Aucune') || info.length === 0) return true
    // Need Nom et prénom AND Adresse to be "complete"
    return !hasInfo('Nom et prénom') || !hasInfo('Adresse postale')
  }

  if (store.formData.statutAuteur === 'Entreprise') {
    // For Enterprise, it's considered complete if we have the SIRET (French) or Adresse (Foreign)
    // and the Nom is mandatory anyway.
    if (store.formData.entrepriseFrancaise === true) {
      return !store.formData.auteurSiret
    }
    if (store.formData.entrepriseFrancaise === false) {
      return !store.formData.auteurAdresse
    }
    return true
  }

  return true
})
</script>
