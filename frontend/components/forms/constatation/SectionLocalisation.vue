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
      <DsfrRadioButtonSet
        v-model="store.formData.proprietaireTerrainPrive"
        legend="Concernant le propriétaire du terrain privé où se situe le dépôt :"
        :required="true"
        :options="[
          {
            label: 'Le propriétaire est victime du dépôt sauvage',
            value: 'Victime',
            id: 'prop-victime',
          },
          {
            label: 'Le propriétaire est responsable du dépôt sauvage',
            value: 'Responsable',
            id: 'prop-responsable',
          },
        ]"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import AddressAutocomplete from '@/components/shared/AddressAutocomplete.vue'
import { useConstatationStore } from '@/stores/constatation'
import { NatureTerrainOptions } from '@/types/constatation'
import { DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const store = useConstatationStore()

const onAddressSelect = (data: { label: string; city: string }) => {
  store.formData.localisationDepot = data.label
  store.formData.commune = data.city
}

const isTerrainPrive = computed(() => store.formData.natureTerrain.includes('Terrain privé'))
</script>
