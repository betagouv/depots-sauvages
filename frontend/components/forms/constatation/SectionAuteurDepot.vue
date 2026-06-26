<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">4</span>
        Identification de l'auteur présumé
      </h2>
    </legend>

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
      <BooleanRadioSet
        v-model="store.formData.auteurIdentifie"
        legend="L'auteur présumé des faits est-il identifié ou identifiable partiellement ?"
        hint="Indiquer NON uniquement s'il n'y a absolument rien qui permettrait d'identifier l'auteur présumé."
        id-prefix="auteur-identifie"
        :required="true"
        :error-message="store.errors.auteurIdentifie"
        @update:model-value="store.clearFieldError('auteurIdentifie')"
      />
    </div>

    <template v-if="store.formData.auteurIdentifie === false">
      <div class="fr-fieldset__element">
        <div class="fr-callout fr-mb-2w fr-callout--blue-cumulus">
          <h3 class="fr-h4 fr-callout__title">
            Sans auteur identifié, le dépôt sauvage n'est pas éligible à la procédure
            administrative.
          </h3>
          <p class="fr-callout__text">
            Vous pouvez cependant déposer plainte en brigade ou commissariat. (Trouvez le point
            d'accueil le plus proche
            <a
              href="https://www.masecurite.interieur.gouv.fr/fr/trouver-un-commissariat-une-gendarmerie/"
              target="_blank"
              rel="noopener noreferrer"
              >ici</a
            >)
          </p>
          <p class="fr-callout__text">
            Protect'Envi peut vous aider à <strong>générer un rapport de constatation</strong>. Ce
            document permet de matérialiser les faits et peut appuyer votre dépôt de plainte.
          </p>
        </div>
      </div>
    </template>

    <template v-if="store.formData.auteurIdentifie === true">
      <div class="fr-fieldset__element">
        <DsfrRadioButtonSet
          v-model="store.formData.statutAuteur"
          legend="S'agit-il d'une entreprise ou d'un particulier ?"
          :required="true"
          :options="[
            { label: 'Entreprise', value: 'entreprise', id: 'statut-entreprise' },
            { label: 'Particulier', value: 'particulier', id: 'statut-particulier' },
          ]"
          :error-message="store.errors.statutAuteur"
          @update:model-value="store.clearFieldError('statutAuteur')"
        />
      </div>

      <template v-if="store.formData.statutAuteur === 'entreprise'">
        <div class="fr-fieldset__element">
          <DsfrCallout
            title="Avec un auteur présumé identifié, vous pouvez débuter une procédure administrative."
          >
            <p>
              Le maire ou l'adjoint par délégation, ou le président d'EPCI par transfert de
              compétence peut engager une <strong>procédure administrative</strong> (article L.541-3
              du Code de l'environnement).
            </p>
            <p>
              Elle permet de <strong>sanctionner efficacement</strong> les auteurs présumés, avec
              une <strong>amende pouvant aller jusqu'à 15 000 €</strong>, recouvrée au profit de la
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
            :error-message="store.errors.entrepriseFrancaise"
            @update:model-value="store.clearFieldError('entrepriseFrancaise')"
          />
        </div>

        <div v-if="store.formData.entrepriseFrancaise === false" class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.auteurNom"
            :required="true"
            label="Nom de l'entreprise présumée auteur du dépôt"
            :error-message="store.errors.auteurNom"
          />
        </div>

        <div v-if="store.formData.entrepriseFrancaise === true" class="fr-fieldset__element">
          <CompanyAutocomplete
            id="auteur-entreprise-recherche"
            v-model="store.formData.auteurNom"
            label="Rechercher l'entreprise par son nom ou son SIRET"
            hint="Saisissez le nom complet ou le numéro SIRET/SIREN de l'entreprise pour l'identifier facilement."
            :error-message="store.errors.auteurNom"
            :required="true"
            @select="onCompanySelect"
          />

          <div class="fr-grid-row fr-grid-row--gutters fr-mt-2w">
            <div class="fr-col-12">
              <DsfrInputGroup
                v-model="store.formData.auteurNom"
                label="Nom de l'entreprise présumée auteur du dépôt"
                :required="true"
                :error-message="store.errors.auteurNom"
                @update:model-value="store.clearFieldError('auteurNom')"
              />
            </div>
            <div class="fr-col-12 fr-col-md-6">
              <DsfrInputGroup
                v-model="store.formData.auteurSiret"
                label="Numéro SIRET"
                :required="true"
                hint="Format attendu : 14 chiffres."
                :error-message="store.errors.auteurSiret"
                @update:model-value="store.clearFieldError('auteurSiret')"
              />
            </div>
            <div class="fr-col-12 fr-col-md-6">
              <DsfrInputGroup
                v-model="store.formData.auteurAdresse"
                label="Adresse de l'entreprise"
                :required="true"
                hint="Adresse du siège social de l'entreprise."
                :error-message="store.errors.auteurAdresse"
                @update:model-value="store.clearFieldError('auteurAdresse')"
              />
            </div>
          </div>
        </div>

        <div v-if="store.formData.entrepriseFrancaise === false" class="fr-fieldset__element">
          <DsfrInputGroup
            v-model="store.formData.auteurAdresse"
            :is-textarea="true"
            :required="true"
            label="Adresse postale complète de l'entreprise étrangère"
            hint="Merci de préciser le pays"
          />
        </div>
      </template>

      <template v-if="store.formData.statutAuteur === 'particulier'">
        <div class="fr-fieldset__element">
          <DsfrCheckboxSet
            v-model="store.formData.informationsAuteur"
            :required="true"
            :options="InfoAuteurOptions"
            :error-message="store.errors.informationsAuteur"
            @update:model-value="store.clearFieldError('informationsAuteur')"
          >
            <template #legend>
              De quelles informations disposez vous sur l'auteur présumé des faits ? *
              <span class="fr-hint-text">Vous pouvez sélectionner un ou plusieurs choix.</span>
            </template>
          </DsfrCheckboxSet>
        </div>

        <div
          v-if="hasInfo('Plaque d\'immatriculation') || hasInfo('Aucune')"
          class="fr-fieldset__element"
        >
          <div class="fr-callout fr-mb-2w fr-callout--blue-cumulus">
            <h3 class="fr-h4 fr-callout__title">
              Sans l'identité complète de l'auteur présumé, la procédure administrative ne peut pas
              être initiée.
            </h3>
            <p class="fr-callout__text">
              Vous pouvez cependant déposer plainte en brigade ou commissariat pour initier une
              procédure judiciaire. En cas d’identification de l'auteur présumé, la communication de
              l’identité pourra être sollicitée auprès du procureur de la République.
            </p>
            <p class="fr-callout__text">
              Continuez cette démarche afin de générer un rapport de constatation pour matérialiser
              les faits et appuyer votre dépôt de plainte.
            </p>
          </div>
        </div>

        <div
          v-if="
            hasInfo('Plaque d\'immatriculation') &&
            !hasInfo('Nom et prénom') &&
            !hasInfo('Adresse postale')
          "
          class="fr-fieldset__element"
        >
          <DsfrCallout
            title="Rapprochez vous de la gendarmerie ou du commissariat pour obtenir l'identité"
          >
            <p>
              La gendarmerie peut communiquer à la police municipale les informations du SIV
              (système d'immatriculation des véhicules).
            </p>
          </DsfrCallout>
        </div>

        <div
          v-if="hasInfo('Nom et prénom') && !hasInfo('Adresse postale')"
          class="fr-fieldset__element"
        >
          <div class="fr-callout fr-mb-2w fr-callout--blue-cumulus">
            <h3 class="fr-h4 fr-callout__title">
              Vous avez le nom et le prénom mais vous n'avez pas l'adresse
            </h3>
            <p class="fr-callout__text">
              Sans l'identité complète de l'auteur présumé, la procédure administrative ne peut pas
              être initiée.
            </p>
            <p class="fr-callout__text">
              Vous pouvez cependant déposer plainte en brigade ou commissariat pour initier une
              procédure judiciaire. En cas d’identification de l'auteur présumé, la communication de
              l’identité pourra être sollicitée auprès du procureur de la République.
            </p>
            <p class="fr-callout__text">
              Continuez cette démarche afin de générer un rapport de constatation pour matérialiser
              les faits et appuyer votre dépôt de plainte
            </p>
            <p class="fr-callout__text">
              En tant qu’OPJ, le maire peut demander la communication de l’adresse de l'auteur
              présumé au procureur de la République.
            </p>
          </div>
        </div>

        <div
          v-if="hasInfo('Nom et prénom') || hasInfo('Adresse postale')"
          class="fr-fieldset__element"
        >
          <DsfrCallout
            title="Avec un auteur présumé identifié, vous pouvez débuter une procédure administrative."
          >
            <p>
              Le maire ou l'adjoint par délégation, ou le président d'EPCI par transfert de
              compétence peut engager une <strong>procédure administrative</strong> (article L.541-3
              du Code de l'environnement).
            </p>
            <p>
              Elle permet de <strong>sanctionner efficacement</strong> les auteurs présumés, avec
              une <strong>amende pouvant aller jusqu'à 15 000 €</strong>, recouvrée au profit de la
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

        <div
          v-if="hasInfo('Nom et prénom') && hasInfo('Adresse postale')"
          class="fr-fieldset__element"
        >
          <DsfrCallout
            title="Avec le nom/prénom et l'adresse postale vous disposez de l'identité complète"
          >
            <p>
              Dans le cas où vous avez bien le nom/prénom ET l'adresse postale vous disposez de
              l'identité complète nécessaire à la procédure administrative.
            </p>
          </DsfrCallout>
        </div>

        <div v-if="hasInfo('Nom et prénom')" class="fr-fieldset__element">
          <DsfrRadioButtonSet
            v-model="store.formData.auteurCivilite"
            legend="Civilité de l'auteur présumé"
            :required="true"
            :options="CiviliteOptions"
            :error-message="store.errors.auteurCivilite"
            @update:model-value="store.clearFieldError('auteurCivilite')"
          />
        </div>
        <div v-if="hasInfo('Nom et prénom')" class="fr-fieldset__element">
          <div class="fr-grid-row fr-grid-row--gutters">
            <div class="fr-col-12 fr-col-md-6">
              <DsfrInputGroup
                v-model="store.formData.auteurNom"
                :required="true"
                label="Nom de famille de l'auteur présumé"
                :error-message="store.errors.auteurNom"
              />
            </div>
            <div class="fr-col-12 fr-col-md-6">
              <DsfrInputGroup
                v-model="store.formData.auteurPrenom"
                :required="true"
                label="Prénom de l'auteur présumé"
                :error-message="store.errors.auteurPrenom"
              />
            </div>
          </div>
        </div>
        <div v-if="hasInfo('Adresse postale')" class="fr-fieldset__element">
          <div v-if="!hasNoExactAuteurAddress">
            <AddressAutocomplete
              id="auteur-adresse"
              v-model="store.formData.auteurAdresse"
              label="Adresse postale de l'auteur présumé"
              :required="true"
              :error-message="store.errors.auteurAdresse"
            />
          </div>
          <div v-else>
            <DsfrInputGroup
              id="auteur-adresse-manuel"
              v-model="store.formData.auteurAdresse"
              :is-textarea="true"
              :required="true"
              label="Adresse postale de l'auteur présumé"
              :error-message="store.errors.auteurAdresse"
              hint="Saisissez l'adresse postale complète"
            />
          </div>
          <div class="fr-mt-2w">
            <DsfrCheckbox
              v-model="hasNoExactAuteurAddress"
              label="Je ne trouve pas l'adresse dans les suggestions, je souhaite la saisir manuellement"
              name="hasNoExactAuteurAddress"
            />
          </div>
        </div>
      </template>
    </template>

    <div v-if="showPlainteSection" class="fr-fieldset__element fr-mt-2w">
      <DsfrRadioButtonSet
        v-model="store.formData.plainteEtat"
        legend="Si la mairie ne peut pas identifier l'auteur des faits, un dépôt de plainte est nécessaire pour initier une procédure pénale."
        :required="true"
        :options="PlainteOptions"
        :error-message="store.errors.plainteEtat"
        @update:model-value="store.clearFieldError('plainteEtat')"
      />
    </div>

    <template v-if="store.formData.auteurIdentifie !== null">
      <div class="fr-fieldset__element">
        <DsfrCheckboxSet
          v-model="store.formData.indicesDisponibles"
          :required="true"
          :options="IndicesOptions"
          :error-message="store.errors.indicesDisponibles"
          @update:model-value="store.clearFieldError('indicesDisponibles')"
        >
          <template #legend>
            Par quels moyens l'auteur présumé peut-il être identifié ? *
            <span class="fr-hint-text">Vous pouvez sélectionner un ou plusieurs choix.</span>
          </template>
        </DsfrCheckboxSet>
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.precisionsIndices"
          :is-textarea="true"
          :required="true"
          label="Ajoutez les éléments qui permettraient d'identifier l'auteur présumé"
          :error-message="store.errors.precisionsIndices"
          hint='Exemple : 
  "Nous constatons la présence des colis et des factures qui ont été retrouvés dans le dépôts sur lesquels est indiqué l’identité d’une personne"
  "Un voisin témoin de la scène a pu relever la plaque d’immatriculation du véhicule"
  "Aucun élément ne permet d’identifier l’auteur présumé"'
        />
      </div>
    </template>
  </fieldset>
</template>

<script setup lang="ts">
import AddressAutocomplete from '@/components/shared/AddressAutocomplete.vue'
import BooleanRadioSet from '@/components/shared/BooleanRadioSet.vue'
import CompanyAutocomplete from '@/components/shared/CompanyAutocomplete.vue'
import { useConstatationStore } from '@/stores/constatation'
import {
  CiviliteOptions,
  IndicesOptions,
  InfoAuteurOptions,
  PlainteOptions,
} from '@/types/constatation'
import {
  DsfrCallout,
  DsfrCheckbox,
  DsfrCheckboxSet,
  DsfrInputGroup,
  DsfrRadioButtonSet,
} from '@gouvminint/vue-dsfr'
import { computed, ref, watch } from 'vue'

const store = useConstatationStore()
const hasNoExactAuteurAddress = ref(false)

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
  }
)

const showPlainteSection = computed(() => {
  if (store.formData.auteurIdentifie === null) return false
  if (store.formData.auteurIdentifie === false) return true

  if (store.formData.statutAuteur === 'particulier') {
    const info = store.formData.informationsAuteur || []
    if (info.length === 0) return false

    // Need both Nom et prénom AND Adresse postale to hide plainte section
    if (hasInfo('Nom et prénom') && hasInfo('Adresse postale')) {
      return false
    }
    return true
  }

  if (store.formData.statutAuteur === 'entreprise') {
    // For Enterprise, it's considered complete if we have the SIRET (French) or Adresse (Foreign)
    if (store.formData.entrepriseFrancaise === true) {
      return (
        !store.formData.auteurSiret || !store.formData.auteurNom || !store.formData.auteurAdresse
      )
    }
    if (store.formData.entrepriseFrancaise === false) {
      return !store.formData.auteurAdresse || !store.formData.auteurNom
    }
    return false
  }

  return false
})

const onCompanySelect = ({
  name,
  siret,
  address,
}: {
  name: string
  siret: string
  address: string
}) => {
  store.formData.auteurNom = name
  store.formData.auteurSiret = siret
  store.formData.auteurAdresse = address
  store.clearFieldError('auteurNom')
  store.clearFieldError('auteurSiret')
  store.clearFieldError('auteurAdresse')
}
</script>
