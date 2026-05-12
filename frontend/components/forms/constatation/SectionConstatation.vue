<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h3 class="fr-h2">2. Détail de la constatation</h3>
    </legend>

    <div class="fr-fieldset__element">
      <DsfrSelect
        v-model="store.formData.constatantRole"
        :required="true"
        label="Au sein de la collectivité, qui est en charge de la constatation de ce dépôt sauvage ?"
        :options="ConstatantOptions"
        :error-message="store.errors.constatantRole"
      />
    </div>

    <div
      v-if="
        ['agent communautaire', 'conseiller communautaire'].includes(
          store.formData.constatantRole
        )
      "
      class="fr-fieldset__element"
    >
      <DsfrAlert
        type="warning"
        title="Vérifiez que la personne constatant le dépôt sauvage est bien habilitée"
      >
        Le conseiller communautaire ou l'agent communautaire peuvent constater un dépôt sauvage
        seulement si ils ont une délégation de pouvoir du président de l'EPCI, qui a lui même reçu
        transfert de compétence du maire – article L.5211-9-2 du CGCT.
      </DsfrAlert>
    </div>

    <div
      v-if="
        ['adjoint au maire', 'conseiller municipal'].includes(store.formData.constatantRole)
      "
      class="fr-fieldset__element"
    >
      <DsfrAlert
        type="warning"
        title="Vérifiez que la personne constatant le dépôt sauvage est bien habilitée"
      >
        Seuls les adjoints ou conseillers municipaux ayant reçu délégation du maire peuvent établir
        un rapport de constatation – article L 2122-18 du CGCT.
      </DsfrAlert>
    </div>

    <div v-if="store.formData.constatantRole === 'president ECPI'" class="fr-fieldset__element">
      <DsfrAlert
        type="warning"
        title="Vérifiez que la personne constatant le dépôt sauvage est bien habilitée"
      >
        Le président de l'EPCI peut établir un rapport de constatation seulement en cas de transfert
        de compétence du maire – article L 2122-9-2 du CGCT.
      </DsfrAlert>
    </div>

    <div v-if="store.formData.constatantRole === 'autre'" class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.constatantRoleAutre"
        label="Saisir votre option"
        :error-message="store.errors.constatantRoleAutre"
      />
      <DsfrAlert
        type="warning"
        title="Vérifiez que la personne constatant le dépôt sauvage est bien habilitée"
        class="fr-mt-2w"
      >
        Si la personne sélectionnée n'est pas habilitée à réaliser un rapport de constatation, il
        n'aura pas de valeur juridique. Nous vous conseillons de faire constater le dépôt sauvage
        par une personne habilitée. Plus d'information
        <a
          href="https://www.ecologie.gouv.fr/lutte-contre-depots-sauvages"
          target="_blank"
          rel="noopener noreferrer"
          >ici</a
        >.
      </DsfrAlert>
    </div>

    <div class="fr-fieldset__element">
      <DsfrRadioButtonSet
        v-model="store.formData.constatantEstUtilisateurConnecte"
        legend="La personne qui remplit ce formulaire est-elle la personne en charge de la constatation du dépôt sauvage ?"
        :options="[
          { label: 'Oui', value: true },
          { label: 'Non', value: false },
        ]"
        :required="true"
        :inline="true"
      />
    </div>

    <template v-if="!store.formData.constatantEstUtilisateurConnecte">
      <div class="fr-fieldset__element">
        <DsfrRadioButtonSet
          v-model="store.formData.constatantCivilite"
          legend="Civilité"
          :options="CiviliteOptions"
          :required="true"
          :error-message="store.errors.constatantCivilite"
          :inline="true"
        />
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInputGroup
            v-model="store.formData.constatantPrenom"
            :required="true"
            label="Prénom"
            :error-message="store.errors.constatantPrenom"
          />
        </div>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrInputGroup
            v-model="store.formData.constatantNom"
            :required="true"
            label="Nom"
            :error-message="store.errors.constatantNom"
          />
        </div>
      </div>
    </template>

    <div class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.dateConstat"
        :required="true"
        type="date"
        label="Date de la constatation"
        hint="Le dépôt ne peut être antérieur au 01/01/2025. Cette date doit être comprise entre le 01/01/2025 et le 31/12/2100."
        :error-message="store.errors.dateConstat"
      />
    </div>

    <div class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.heureConstat"
        :required="true"
        type="time"
        label="Heure de la constatation"
        :error-message="store.errors.heureConstat"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { useConstatationStore } from '@/stores/constatation'
import { CiviliteOptions, ConstatantOptions } from '@/types/constatation'
import { DsfrAlert, DsfrInputGroup, DsfrRadioButtonSet, DsfrSelect } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()
</script>
