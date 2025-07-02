<template>
  <div class="fr-container--sm fr-m-1w">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
      <div class="fr-form-group">
        <h3 class="fr-h5">À propos de l’auteur des faits</h3>
        <DsfrRadioButtonSet
          :model-value="store.formData.auteurIdentifie ? 'oui' : 'non'"
          @update:model-value="(value) => store.updateBooleanField('auteurIdentifie', value)"
          name="auteur-identifie"
          legend="L'auteur des faits est-il identifié ?"
          :options="yesNoOptions"
          required
        />

        <DsfrRadioButtonSet
          v-if="showBlocAuteur"
          v-model="store.formData.statutAuteur"
          name="statut-auteur"
          legend="S'agit-il d'une entreprise ou d'un particulier ?"
          :options="statutAuteurOptions"
          required
        />

        <template v-if="showBlocAuteur">
          <template v-if="store.formData.statutAuteur === 'entreprise'">
            <div class="fr-mb-4w">
              <DsfrInput
                class="fr-mb-3w"
                v-model="store.formData.nomEntreprise"
                label="Nom de l'entreprise ou raison sociale"
                name="nom-entreprise"
                type="text"
                required
              />
              <DsfrInput
                v-model="store.formData.numeroSiret"
                label="Numéro de SIRET"
                name="numero-siret"
                type="text"
                inputmode="numeric"
                pattern="[0-9]{14}"
                hint="14 chiffres sans espaces"
              />
            </div>
          </template>

          <template v-if="store.formData.statutAuteur === 'particulier'">
            <div class="fr-mb-3w">
              <DsfrInput
                v-model="store.formData.prenomParticulier"
                label="Prénom du particulier"
                name="prenom-particulier"
                type="text"
                required
              />
              <DsfrInput
                v-model="store.formData.nomParticulier"
                label="Nom du particulier"
                name="nom-particulier"
                type="text"
                required
              />
            </div>
          </template>
        </template>

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
import { computed, ref } from 'vue'
import {
  indicesDisponiblesOptions,
  statutAuteurOptions,
  yesNoOptions,
} from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false)
const showBlocAuteur = computed(() => store.formData.auteurIdentifie)

const handleSubmit = async (event: Event) => {
  event.preventDefault()
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
