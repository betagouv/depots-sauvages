<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">3</span>
        Description du dépôt
      </h2>
    </legend>

    <div class="fr-fieldset__element">
      <BooleanRadioSet
        v-model="store.formData.photoDispo"
        legend="Disposez vous de photos du dépôt ?"
        hint="À la fin de cette démarche, vous pourrez récupérer le rapport de constatation. Vous devrez y insérer vos photos."
        id-prefix="photo-dispo"
        :required="true"
      />
    </div>

    <div class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.precisionsDepot"
        :is-textarea="true"
        :required="true"
        label="Description du dépôt"
        :error-message="store.errors.precisionsDepot"
      >
        <template #hint>
          <div class="fr-hint-text">
            Décrivez en quelques lignes le dépôt constaté.
            <br />
            Apportez également tout autre élément important :
            <ul class="fr-m-0 fr-pl-2w">
              <li>présence d'habitation, présence d'élevage, voie ferrée ;</li>
              <li>identité du propriétaire du terrain (si terrain privé) ;</li>
              <li>
                zone particulière (zone agricole, zone forestière, zone naturelle, zone humide, zone
                Natura 2000, zone Ramsar, etc.) ;
              </li>
              <li>
                risque d'écoulement (présence de liquide, proximité avec un cours d'eau ou captage
                d'eau) ;
              </li>
              <li>
                dernière date à laquelle le dépôt n'était pas présent (si vous en avez
                connaissance).
              </li>
            </ul>
          </div>
        </template>
      </DsfrInputGroup>
    </div>

    <div class="fr-fieldset__element">
      <DsfrRadioButtonSet
        v-model="store.formData.volumeDepot"
        legend="Volume estimé"
        :required="true"
        :options="VolumeOptions"
        :error-message="store.errors.volumeDepot"
      />
    </div>

    <div class="fr-fieldset__element">
      <DsfrCheckboxSet
        v-model="store.formData.typesDepot"
        legend="Type de dépôt"
        :required="true"
        :options="TypeDepotOptions"
        :error-message="store.errors.typesDepot"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import BooleanRadioSet from '@/components/shared/BooleanRadioSet.vue'
import { useConstatationStore } from '@/stores/constatation'
import { TypeDepotOptions, VolumeOptions } from '@/types/constatation'
import { DsfrCheckboxSet, DsfrInputGroup, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()


</script>
