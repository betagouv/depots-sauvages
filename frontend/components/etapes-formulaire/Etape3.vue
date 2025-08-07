<template>
  <div class="fr-container--sm fr-m-1w">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <div class="fr-form-group">
        <h3 class="fr-h5">À propos de l’auteur des faits</h3>
        <fieldset
          class="fr-form-group fr-fieldset--no-border fr-mb-3w"
          :class="{ 'fr-form-group--error': showAuteurIdentifieError }"
        >
          <legend
            class="fr-text--regular"
            :class="{ 'fr-pb-2w': !showAuteurIdentifieError }"
          >
            L’auteur des faits est-il identifié ? *
          </legend>
          <p
            v-if="showAuteurIdentifieError"
            class="fr-error-text fr-my-2w"
            tabindex="-1"
            ref="auteurIdentifieErrorMessage"
            id="error-message-auteurIdentifie"
            aria-live="polite"
          >
            {{ store.errors.auteurIdentifie }}
          </p>
          <div class="fr-radio-group fr-my-1w fr-py-1w">
            <input
              type="radio"
              id="auteurIdentifie-oui"
              name="auteur-identifie"
              :value="true"
              v-model="store.formData.auteurIdentifie"
              @change="clearError('auteurIdentifie')"
              aria-describedby="error-message-auteurIdentifie"
            />
            <label class="fr-label" for="auteurIdentifie-oui">Oui</label>
          </div>

          <div class="fr-radio-group fr-my-1w">
            <input
              type="radio"
              id="auteurIdentifie-non"
              name="auteur-identifie"
              :value="false"
              v-model="store.formData.auteurIdentifie"
              @change="clearError('auteurIdentifie')"
              aria-describedby="error-message-auteurIdentifie"
            />
            <label class="fr-label" for="auteurIdentifie-non">Non</label>
          </div>
        </fieldset>

        <StatutAuteur v-if="store.formData.auteurIdentifie === true" />

        <AuteurDetails
          v-if="showBlocAuteur && (store.formData.statutAuteur === 'entreprise' || store.formData.statutAuteur === 'particulier')"
          :statutAuteur="store.formData.statutAuteur"
          :formData="store.formData"
          :errors="store.errors"
          :clearError="clearError"
        />

        <fieldset class="fr-form-group fr-pl-0 fr-fieldset--no-border">
          <legend class="fr-pb-2w fr-text--regular">
            Disposez-vous d’éléments pouvant aider à identifier l’auteur ?
          </legend>
          <div class="fr-fieldset__content fr-ml-0">
            <div
              v-for="option in indicesDisponiblesOptions"
              :key="option.value"
              class="fr-checkbox-group"
            >
              <input
                type="checkbox"
                :id="option.id"
                :name="option.name"
                :value="option.value"
                v-model="store.formData.indicesDisponibles"
              />
              <label class="fr-label" :for="option.id">{{ option.label }}</label>
            </div>
          </div>
        </fieldset>

      </div>

      <div class="fr-form-group">
        <h3 class="fr-h5">Souhaitez-vous engager une procédure ?</h3>
        <DsfrRadioButtonSet
          :model-value="store.formData.souhaitePorterPlainte ? 'oui' : 'non'"
          @update:model-value="(value) => store.updateBooleanField('souhaitePorterPlainte', value)"
          name="souhaite-porter-plainte"
          legend="Souhaitez-vous que la collectivité engage une procédure (plainte, signalement, etc.) ?"
          :options="yesNoOptions"
          required
        />
      </div>

      <div class="fr-form-group">
        <h3 class="fr-h5">Ce que vous avez constaté</h3>
        <DsfrInput
          v-model="store.formData.precisionsIndices"
          label="Décrivez brièvement les faits constatés, autres éléments à ajouter"
          hint="Exemple: identité et qualité des personnes rencontrées, nature des vérifications auxquelles il a été procédé, etc."
          :isTextarea="true"
        />
      </div>

      <div class="fr-form-group fr-mt-3w">
        <h3 class="fr-h5">Estimation du préjudice</h3>
        <DsfrRadioButtonSet
          :model-value="store.formData.arreteMunicipalExiste ? 'oui' : 'non'"
          @update:model-value="(value) => store.updateBooleanField('arreteMunicipalExiste', value)"
          name="arrete-municipal"
          legend="Disposez-vous d'un arrêté ou d'une délibération municipale encadrant ce type d'infraction et fixant le montant d'un forfait d'enlèvement ?"
          :options="yesNoOptions"
          required
        />

        <DsfrInput
          v-if="store.formData.arreteMunicipalExiste"
          type="number"
          name="forfait-enlevement"
          label="Indiquez le montant du forfait d'enlèvement (en euros)"
          v-model="store.formData.montantForfaitEnlevement"
          min="0"
          required
        />

        <fieldset class="fr-form-group fr-fieldset--no-border fr-mb-3w">
          <legend class="fr-text--regular">
            Connaissez-vous le montant du préjudice (en euros) ? *
            <span class="fr-hint-text fr-mt-1w">
              Exemple : les frais engagés par la mairie ; prestation d'une entreprise de nettoyage, coût en déchetterie, emploi de personnels et matériels municipaux, etc.
            </span>
          </legend>
          <div class="fr-radio-group fr-my-1w fr-py-1w">
            <input
              type="radio"
              id="prejudice-oui"
              name="prejudice-montant-connu"
              value="oui"
              :checked="store.formData.prejudiceMontantConnu === true"
              @change="store.updateBooleanField('prejudiceMontantConnu', 'oui')"
              required
            />
            <label class="fr-label" for="prejudice-oui">Oui</label>
          </div>

          <div class="fr-radio-group fr-my-1w">
            <input
              type="radio"
              id="prejudice-non"
              name="prejudice-montant-connu"
              value="non"
              :checked="store.formData.prejudiceMontantConnu === false"
              @change="store.updateBooleanField('prejudiceMontantConnu', 'non')"
              required
            />
            <label class="fr-label" for="prejudice-non">Non</label>
          </div>
        </fieldset>

        <template v-if="store.formData.prejudiceMontantConnu">
          <DsfrInput
            v-model="store.formData.prejudiceMontant"
            type="number"
            label="Montant du préjudice (en euros)"
            min="0"
            required
          />
        </template>

        <template v-else>
          <fieldset class="fr-form-group fr-fieldset--no-border">
            <legend class="fr-pb-2w fr-text--regular">Ajouter un détail estimatif du montant</legend>
            <DsfrInput
              v-model="store.formData.prejudiceNombrePersonnes"
              type="number"
              label="Nombre de personnes mobilisées"
            />
            <DsfrInput
              v-model="store.formData.prejudiceNombreHeures"
              type="number"
              label="Nombre d'heures travaillées"
            />
            <DsfrInput
              v-model="store.formData.prejudiceNombreVehicules"
              type="number"
              label="Nombre de véhicules utilisés"
            />
            <DsfrInput
              v-model="store.formData.prejudiceKilometrage"
              type="number"
              label="Kilométrage estimé"
            />
            <DsfrInput
              v-model="store.formData.prejudiceAutresCouts"
              type="number"
              label="Autres coûts"
            />
          </fieldset>
        </template>
      </div>

      <div class="fr-mt-3w actions-row">
        <DsfrButton
          type="button"
          label="Précédent"
          icon="fr-icon-arrow-left-line"
          secondary
          @click="handlePrevious"
        />
        <DsfrButton
          type="submit"
          label="Suivant"
          icon="fr-icon-arrow-right-line"
          icon-right
          :disabled="isSubmitting"
        />
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import '@/styles/form-steps.css'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrInput, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed, nextTick, ref, watch } from 'vue'
import { indicesDisponiblesOptions, yesNoOptions } from './form-data'
import AuteurDetails from './AuteurDetails.vue'
import StatutAuteur from './StatutAuteur.vue'

const store = useSignalementStore()
const isSubmitting = ref(false)
const showBlocAuteur = computed(() => store.formData.auteurIdentifie === true)
const showAuteurIdentifieError = computed(() => !!store.errors.auteurIdentifie)

watch(() => store.formData.auteurIdentifie, (value) => {
  if (value !== true) {
    Object.assign(store.formData, {
      statutAuteur: '',
      nomEntreprise: '',
      numeroSiret: '',
      prenomParticulier: '',
      nomParticulier: ''
    })
  }
})

watch(() => store.formData.statutAuteur, (newValue) => {
  if (newValue === 'entreprise') {
    store.formData.prenomParticulier = ''
    store.formData.nomParticulier = ''
  } else if (newValue === 'particulier') {
    store.formData.nomEntreprise = ''
    store.formData.numeroSiret = ''
  }
})

const validateStep3 = () => {
  const errors: Record<string, string> = {}

  const { auteurIdentifie, statutAuteur } = store.formData

  if (auteurIdentifie !== true && auteurIdentifie !== false) {
    errors.auteurIdentifie = "Le champ « L’auteur des faits est-il identifié ? » est vide. Veuillez sélectionner une option."
  }

  if (auteurIdentifie === true) {
    validateStatutAuteur(errors, statutAuteur)
  }

  store.errors = errors
  return Object.keys(errors).length === 0
}

function validateStatutAuteur(errors: Record<string, string>, statutAuteur: string) {
  if (!statutAuteur || (statutAuteur !== 'entreprise' && statutAuteur !== 'particulier')) {
    errors.statutAuteur = "Le champ « S'agit-il d'une entreprise ou d'un particulier ? » est vide. Veuillez sélectionner une option."
    return
  }

  if (statutAuteur === 'entreprise') {
    validateAuteurEntreprise(errors)
  } else if (statutAuteur === 'particulier') {
    validateAuteurParticulier(errors)
  }
}

function validateAuteurEntreprise(errors: Record<string, string>) {
  const { nomEntreprise, numeroSiret } = store.formData

  if (!nomEntreprise || nomEntreprise.trim() === '') {
    errors.nomEntreprise = 'Le champ "Nom de l’entreprise" est vide. Veuillez renseigner le nom.'
  }

  const siretRegex = /^\d{14}$/
  const numeroSiretStr = numeroSiret?.trim()

  if (numeroSiretStr && !siretRegex.test(numeroSiretStr)) {
    errors.numeroSiret = 'Le numéro de SIRET doit contenir 14 chiffres.'
  }
}

function validateAuteurParticulier(errors: Record<string, string>) {
  const { prenomParticulier, nomParticulier } = store.formData

  if (!prenomParticulier || prenomParticulier.trim() === '') {
    errors.prenomParticulier = 'Le champ "Prénom du particulier" est vide. Veuillez renseigner le prénom.'
  }

  if (!nomParticulier || nomParticulier.trim() === '') {
    errors.nomParticulier = 'Le champ "Nom du particulier" est vide. Veuillez renseigner le nom.'
  }
}

const clearError = (field: string) => {
  if (store.errors[field]) {
    delete store.errors[field]
  }
}

const handleSubmit = async (event: Event) => {
  event.preventDefault()

  const isValid = validateStep3()


  if (!isValid) {
    await nextTick()
    const firstErrorElement = document.querySelector(
      '.fr-input-group--error select, .fr-input-group--error input, .fr-form-group--error input, .fr-error-text'
      )
    if (firstErrorElement instanceof HTMLElement) {
      firstErrorElement.focus()
    }
    return
  }

  isSubmitting.value = true
  try {
    await store.saveFormData()
    store.updateStep(4)
  } catch (error) {
    console.error('Failed to save:', error)
  } finally {
    isSubmitting.value = false
  }
}

const handlePrevious = () => store.updateStep(2)
</script>

<style scoped>
.actions-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.fr-fieldset--no-border {
  border: none;
  margin: 0;
  padding: 0;
  color: #161616 !important;
}

</style>
