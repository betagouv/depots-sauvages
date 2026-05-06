<template>
  <fieldset class="fr-fieldset fr-my-0">
    <legend class="fr-fieldset__legend">
      <h3 class="fr-h2">Localisation du dépôt</h3>
    </legend>

    <div class="fr-fieldset__element">
      <AddressAutocomplete
        id="address-input"
        label="Adresse du dépôt *"
        hint="Saisissez une adresse, une voie, un lieu-dit ou une commune. Exemple : 11 rue Réaumur, Paris"
        v-model="store.formData.localisationDepot"
        :error-message="store.errors.localisationDepot"
        @select="onAddressSelect"
      />
    </div>

    <div class="fr-fieldset__element fr-mt-2w">
      <DsfrCheckboxSet
        v-model="store.formData.natureTerrain"
        :required="true"
        :options="NatureTerrainOptions"
        :error-message="store.errors.natureTerrain"
      >
        <template #legend>
          Nature du terrain
          <span class="fr-hint-text">Vous pouvez sélectionner un ou plusieurs choix.</span>
        </template>
      </DsfrCheckboxSet>
    </div>

    <div v-if="isTerrainPrive" class="fr-fieldset__element fr-mt-2w">
      <DsfrCallout title="Dépôt sur terrain privé" class="fr-mb-4w">
        Vous pouvez agir sur un terrain privé en cas d'atteinte à la salubrité publique (pollution
        de toute nature) ou à la sécurité (risque d'incendie).
        <br />
        A ce titre, le pouvoir de police municipale s'applique même sur une propriété privée et
        permet de prendre des mesures pour prévenir ces atteintes.
        <br />
        Cette spécificité sera mentionnée dans le rapport de constatation.
      </DsfrCallout>

      <DsfrRadioButtonSet
        v-model="store.formData.proprietaireTerrainPrive"
        :required="true"
        :options="[
          {
            label: 'Le propriétaire est victime du dépôt sauvage',
            value: 'Victime',
            id: 'prop-victime',
          },
          {
            label:
              'Le propriétaire est responsable ou complice du dépôt sauvage, ou fait preuve de négligence',
            value: 'Responsable',
            id: 'prop-responsable',
          },
        ]"
      >
        <template #legend>
          Concernant le propriétaire du terrain privé où se situe le dépôt
          <span class="fr-hint-text">
            Vous avez indiqué que le dépôt sauvage était situé - tout ou partie - sur un terrain
            privé. Merci de préciser la situation du propriétaire.
          </span>
        </template>
      </DsfrRadioButtonSet>

      <DsfrCallout
        v-if="isProprietaireVictime"
        title="Le propriétaire est victime"
        class="fr-mt-2w"
      >
        Dans un premier temps, vous pouvez encourager le propriétaire à déposer plainte au
        commissariat ou en gendarmerie.
        <br />
        ⚠️ Si le propriétaire refuse ou tarde à nettoyer ou fait preuve de négligence, il peut être
        considéré comme détenteur des déchets et devenir responsable au titre de la procédure
        administrative.
      </DsfrCallout>

      <DsfrCallout
        v-if="isProprietaireResponsable"
        title="La responsabilité du propriétaire est engagée"
        class="fr-mt-2w"
      >
        ⚠️ Si le propriétaire refuse ou tarde à nettoyer ou fait preuve de négligence, il peut être
        considéré comme détenteur des déchets et en devenir responsable.
        <br />
        La procédure administrative peut être initiée contre lui.
      </DsfrCallout>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import AddressAutocomplete from '@/components/shared/AddressAutocomplete.vue'
import { useConstatationStore } from '@/stores/constatation'
import { NatureTerrainOptions } from '@/types/constatation'
import { DsfrCallout, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const store = useConstatationStore()

const onAddressSelect = (data: { label: string; city: string }) => {
  store.formData.localisationDepot = data.label
  store.formData.commune = data.city
}

const isTerrainPrive = computed(() => {
  const nature = store.formData.natureTerrain || []
  return nature.includes('Terrain privé')
})

const isProprietaireVictime = computed(() => store.formData.proprietaireTerrainPrive === 'Victime')
const isProprietaireResponsable = computed(
  () => store.formData.proprietaireTerrainPrive === 'Responsable'
)
</script>
