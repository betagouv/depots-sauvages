<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">5</span>
        Estimation du préjudice
      </h2>
    </legend>

    <DsfrCallout title="Pourquoi évaluer le préjudice ?" class="fr-mb-2w">
      <p>L'estimation du préjudice est indispensable pour la solidité de la procédure.</p>
    </DsfrCallout>

    <div class="fr-fieldset__element">
      <BooleanRadioSet
        v-model="store.formData.prejudiceMontantConnu"
        legend="Connaissez-vous le montant du préjudice (en euros) ?"
        hint="Exemple : les frais engagés par la mairie; prestation d'une entreprise de nettoyage, coût en déchetterie, emploi de personnels et matériels municipaux, etc."
        id-prefix="prejudice-connu"
        :required="true"
        :error-message="store.errors.prejudiceMontantConnu"
      />
    </div>

    <template v-if="store.formData.prejudiceMontantConnu === true">
      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceMontant"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="true"
          label="Montant du préjudice (en euros)"
          :error-message="store.errors.prejudiceMontant"
          hint="Exemple : 1500 ou 1500.50"
        />
      </div>

      <DsfrCallout title="Joignez vos justificatifs" class="fr-mb-2w">
        <p>
          Pensez à numériser vos justificatifs et à les insérer dans le rapport de constatation
          généré à la fin de cette démarche
        </p>
      </DsfrCallout>
    </template>

    <template v-if="store.formData.prejudiceMontantConnu === false">
      <DsfrCallout title="Nous pouvons vous aider à estimer le préjudice" class="fr-mb-2w">
        <p>
          Merci de nous donner les informations suivantes afin que nous puissions vous aider à
          estimer le préjudice lié au traitement de ce dépôt sauvage.
        </p>
      </DsfrCallout>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombrePersonnes"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="false"
          label="Nombre de personnes mobilisées"
          :error-message="store.errors.prejudiceNombrePersonnes"
          hint="Exemple : 3 (élus, agents techniques...)"
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombreHeures"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="false"
          label="Nombre d'heures travaillées"
          :error-message="store.errors.prejudiceNombreHeures"
          hint="Temps passé à retirer le dépôt ou à gérer son traitement."
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombreVehicules"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="false"
          label="Nombre de véhicules utilisés"
          :error-message="store.errors.prejudiceNombreVehicules"
          hint="Nombre de véhicules municipaux ou de location mobilisés."
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceKilometrage"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="false"
          label="Kilométrage estimé"
          :error-message="store.errors.prejudiceKilometrage"
          hint="Distance totale parcourue pour collecter et acheminer le dépôt."
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceAutresCouts"
          type="number"
          min="0"
          step="any"
          inputmode="decimal"
          :required="false"
          label="Autres coûts (en euros)"
          :error-message="store.errors.prejudiceAutresCouts"
          hint="Exemple : 150.50 (frais de mise en décharge, traitement spécifique...)"
        />
      </div>
    </template>
  </fieldset>
</template>

<script setup lang="ts">
import BooleanRadioSet from '@/components/shared/BooleanRadioSet.vue'
import { useConstatationStore } from '@/stores/constatation'
import { DsfrCallout, DsfrInputGroup } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()
</script>
