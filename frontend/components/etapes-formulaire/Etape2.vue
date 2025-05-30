<template>
  <div class="fr-container--sm">
    <p>Les champs avec <abbr title="Champ obligatoire">*</abbr> sont obligatoires</p>
    <form @submit.prevent="handleSubmit">
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
          <DsfrInput
            v-model="store.formData.nomEntreprise"
            label="Nom de l'entreprise"
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
        </template>

        <template v-if="store.formData.statutAuteur === 'particulier'">
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
        </template>
      </template>

      <DsfrRadioButtonSet
        :model-value="store.formData.souhaitePorterPlainte ? 'oui' : 'non'"
        @update:model-value="(value) => store.updateBooleanField('souhaitePorterPlainte', value)"
        name="souhaite-porter-plainte"
        legend="Souhaitez-vous porter plainte ?"
        :options="yesNoOptions"
        required
      />

      <div class="fr-form-group">
        <legend class="fr-fieldset__legend fr-text--regular">
          🔍 Des indices pourraient-ils permettre d'identifier l'auteur ?
        </legend>
        <div class="fr-fieldset__content">
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
      </div>

      <DsfrInput
        v-model="store.formData.precisionsIndices"
        label="Avez vous d'autres éléments à ajouter ?"
        hint="Exemple: identité et qualité des personnes rencontrées, nature des vérifications auxquelles il a été procédé, etc."
        :isTextarea="true"
      />

      <hr />

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

      <DsfrRadioButtonSet
        :model-value="store.formData.prejudiceMontantConnu ? 'oui' : 'non'"
        @update:model-value="(value) => store.updateBooleanField('prejudiceMontantConnu', value)"
        name="prejudice-montant-connu"
        hint="Le préjudice peut comprendre les frais engagés par la mairie : prestation d'une entreprise de nettoyage, coût en déchetterie, emploi de personnels et matériels municipaux, etc."
        legend="Connaissez-vous le montant du préjudice ?"
        :options="yesNoOptions"
        required
      />

      <template v-if="store.formData.prejudiceMontantConnu">
        <DsfrInput
          v-model="store.formData.prejudiceMontant"
          type="number"
          label="Montant du préjudice"
          min="0"
          required
        />
      </template>

      <template v-else>
        <fieldset class="fr-fieldset fr-ml-0 fr-pl-0">
          <legend class="fr-fieldset__legend">Estimation du préjudice</legend>
          <DsfrInput
            v-model="store.formData.prejudiceNombrePersonnes"
            type="number"
            label="Nombre de personnes mobilisées"
          />
          <DsfrInput
            v-model="store.formData.prejudiceNombreHeures"
            type="number"
            label="Nombre d'heures"
          />
          <DsfrInput
            v-model="store.formData.prejudiceNombreVehicules"
            type="number"
            label="Nombre de véhicules"
          />
          <DsfrInput
            v-model="store.formData.prejudiceKilometrage"
            type="number"
            label="Kilométrage"
          />
          <DsfrInput
            v-model="store.formData.prejudiceAutresCouts"
            type="number"
            label="Autres coûts"
          />
        </fieldset>
      </template>

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
          label="Valider"
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
import { indicesDisponiblesOptions, statutAuteurOptions, yesNoOptions } from './form-data'

const store = useSignalementStore()
const isSubmitting = ref(false)
const showBlocAuteur = computed(() => store.formData.auteurIdentifie)

const handleSubmit = async (event: Event) => {
  event.preventDefault()
  isSubmitting.value = true
  try {
    await store.saveFormData()
    store.updateStep(3)
  } catch (error) {
    console.error('Failed to save:', error)
  } finally {
    isSubmitting.value = false
  }
}

const handlePrevious = () => store.updateStep(1)
</script>

<style scoped>
.actions-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
</style>
