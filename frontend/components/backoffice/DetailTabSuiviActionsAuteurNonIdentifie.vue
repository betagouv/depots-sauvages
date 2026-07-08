<template>
  <div>
    <div class="bo-step-section bo-step-section--green">
      <h4 class="fr-text--sm fr-mb-1w bo-step-title--green fr-text--bold">
        Étape 1 : Constitution du dossier
      </h4>
      <div class="bo-flex-col">
        <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
          <input type="checkbox" :checked="procedure.suivi_procedure?.preuves_fournies" disabled />
          Éléments de preuve joints
        </label>
        <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
          <input
            type="checkbox"
            :checked="procedure.suivi_procedure?.constatation_signee"
            disabled
          />
          Rapport de constatation signé
        </label>
      </div>
    </div>

    <div
      :class="[
        'bo-step-section',
        procedure.suivi_procedure?.etape_en_cours >= 2
          ? 'bo-step-section--green'
          : 'bo-step-section--grey',
      ]"
    >
      <h4
        :class="[
          'fr-text--sm',
          'fr-text--bold',
          'fr-mb-1w',
          procedure.suivi_procedure?.etape_en_cours >= 2
            ? 'bo-step-title--green'
            : 'bo-step-title--grey',
        ]"
      >
        Étape 2 : Identifier l'auteur
      </h4>
      <div class="bo-flex-col">
        <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
          <input
            type="checkbox"
            :checked="procedure.suivi_procedure?.identification_reussie !== null"
            disabled
          />
          Recherche d'identité effectuée
        </label>
        <div class="fr-text--xs fr-ml-2w fr-mt-1v">
          Résultat :
          <span
            v-if="procedure.suivi_procedure?.identification_reussie === true"
            class="fr-text--bold fr-text-success"
          >
            Auteur identifié
          </span>
          <span
            v-else-if="procedure.suivi_procedure?.identification_reussie === false"
            class="fr-text--bold fr-text-danger"
          >
            Auteur non identifié
          </span>
          <span v-else class="fr-text-mention--grey fr-text--italic"> En cours </span>
        </div>
      </div>
    </div>

    <div
      :class="[
        'bo-step-section',
        procedure.suivi_procedure?.etape_en_cours >= 3
          ? 'bo-step-section--green'
          : 'bo-step-section--grey',
      ]"
    >
      <h4
        :class="[
          'fr-text--sm',
          'fr-text--bold',
          'fr-mb-1w',
          procedure.suivi_procedure?.etape_en_cours >= 3
            ? 'bo-step-title--green'
            : 'bo-step-title--grey',
        ]"
      >
        Étape 3 : Recherche & Actions
      </h4>
      <p class="fr-text--xs fr-mb-0">
        <span
          v-if="procedure.suivi_procedure?.identification_reussie === null"
          class="fr-text-mention--grey fr-text--italic"
        >
          En attente de l'identification de l'auteur
        </span>
        <span
          v-else-if="procedure.suivi_procedure?.identification_reussie === true"
          class="fr-text--bold"
        >
          Action requise : Mettre à jour le dossier pour saisir l'identité de l'auteur.
        </span>
        <span
          v-else-if="procedure.suivi_procedure?.identification_reussie === false"
          class="fr-text--bold"
        >
          Action requise : Clôture sans auteur.
        </span>
      </p>
    </div>

    <div
      :class="[
        'bo-step-section',
        procedure.suivi_procedure?.etape_en_cours >= 5
          ? 'bo-step-section--green'
          : 'bo-step-section--grey',
      ]"
      class="fr-mb-0"
    >
      <h4
        :class="[
          'fr-text--sm',
          'fr-text--bold',
          'fr-mb-1w',
          procedure.suivi_procedure?.etape_en_cours >= 5
            ? 'bo-step-title--green'
            : 'bo-step-title--grey',
        ]"
      >
        Étape 5 : Clôture de la procédure
      </h4>
      <div class="bo-flex-col">
        <div class="bo-flex-space-between">
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.nettoyage_fait" disabled />
            Nettoyage du dépôt effectué
          </label>
          <input
            v-if="procedure.suivi_procedure?.nettoyage_fait"
            type="text"
            class="fr-input fr-input--sm bo-input-text-sm bo-input-date-sm"
            placeholder="Par (ex: Auteur)"
            :value="procedure.suivi_procedure?.nettoyage_par"
            disabled
          />
        </div>
        <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
          <input type="checkbox" :checked="procedure.suivi_procedure?.dossier_archive" disabled />
          Dossier clos et archivé
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  procedure: any
}>()
</script>
