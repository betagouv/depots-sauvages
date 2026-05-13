<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">5</span>
        Estimation du préjudice
      </h2>
    </legend>

    <DsfrCallout
      title="Pourquoi évaluer le préjudice ?"
      class="fr-mb-2w"
    >
      <p>
        L'estimation du préjudice est indispensable pour la solidité de la procédure.
      </p>
      <p class="fr-text--bold fr-mt-2w">
        Attention le montant du préjudice ne correspond pas au montant de l'amende administrative
        qui peut être émise contre l'auteur présumé des faits.
      </p>
      <p>
        Le montant de l'amende est décidé par la collectivité dans un second temps, il doit être juste et proportionné avec un maximum de 15 000 €.
      </p>
      <p class="fr-mt-2w">
        Si vous souhaitez évaluer le montant de l'amende vous pouvez
        <a href="https://protect-envi.beta.gouv.fr/simulateur-amende" target="_blank" rel="noopener noreferrer"
          >utiliser notre simulateur</a
        >.
      </p>
    </DsfrCallout>

    <div class="fr-fieldset__element">
      <BooleanRadioSet
        v-model="store.formData.prejudiceMontantConnu"
        legend="Connaissez-vous le montant du préjudice (en euros) ?"
        hint="Exemple : les frais engagés par la mairie; prestation d'une entreprise de nettoyage, coût en déchetterie, emploi de personnels et matériels municipaux, etc."
        id-prefix="prejudice-connu"
        :required="true"
      />
    </div>

    <template v-if="store.formData.prejudiceMontantConnu === true">
      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceMontant"
          type="number"
          :required="true"
          label="Montant du préjudice (en euros)"
          hint="Format attendu : De 1 à 3 décimales après le point. Exemple: 3.141. Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 1000000."
        />
      </div>

      <DsfrCallout
        title="Joignez vos justificatifs"
        class="fr-mb-2w"
      >
        <p>
          Pensez à numériser vos justificatifs et à les insérer dans le rapport de constatation
          généré à la fin de cette démarche
        </p>
      </DsfrCallout>
    </template>

    <template v-if="store.formData.prejudiceMontantConnu === false">
      <DsfrCallout
        title="Nous pouvons vous aider à estimer le préjudice"
        class="fr-mb-2w"
      >
        <p>
          Merci de nous donner les informations suivantes afin que nous puissions vous aider à
          estimer le préjudice lié au traitement de ce dépôt sauvage.
        </p>
      </DsfrCallout>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombrePersonnes"
          type="number"
          :required="true"
          label="Nombre de personnes mobilisées"
          hint="Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 100. élu, agents techniques"
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombreHeures"
          type="number"
          :required="true"
          label="Nombre d'heures travaillées"
          hint="Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 1000. Temps pour retirer le dépôt ou pour gérer son traitement"
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceNombreVehicules"
          type="number"
          :required="true"
          label="Nombre de véhicules utilisés"
          hint="Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 100."
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceKilometrage"
          type="number"
          :required="true"
          label="Kilométrage estimé"
          hint="Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 1000. pour retirer le dépôt et/ou pour aller en déchetterie"
        />
      </div>

      <div class="fr-fieldset__element">
        <DsfrInputGroup
          v-model="store.formData.prejudiceAutresCouts"
          type="number"
          :required="true"
          label="Autres coûts (en euros)"
          hint="Format attendu : De 1 à 3 décimales après le point. Exemple: 3.141. Ce nombre doit être positif. Ce nombre doit être compris entre 0 et 100000. Mise en décharge, forfait enlèvement, traitement spécifique, achat de matériel, location de matériel"
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
