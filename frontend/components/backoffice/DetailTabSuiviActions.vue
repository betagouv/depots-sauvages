<template>
  <div class="premium-box fr-p-3w bo-card">
    <h3 class="fr-h6 fr-mb-3w bo-card-title">
      <span class="fr-icon-survey-line fr-mr-1w"></span> Actions du Suivi
    </h3>

    <!-- CASE: Auteur identifié -->
    <template v-if="auteurIdentifie">
      <!-- Étape 1 : Constitution du dossier -->
      <div class="bo-step-section bo-step-section--green">
        <h4 class="fr-text--sm fr-mb-1w bo-step-title--green fr-text--bold">
          Étape 1 : Constitution du dossier
        </h4>
        <div class="bo-flex-col">
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.preuves_fournies"
              disabled
            />
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
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.lettre_signe" disabled />
            Lettre d'information signée
          </label>
        </div>
      </div>

      <!-- Étape 2 : Notification à l'auteur -->
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
          Étape 2 : Notification à l'auteur
        </h4>
        <div class="bo-flex-col">
          <!-- lettre_envoyee & date -->
          <div class="bo-flex-space-between">
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input
                type="checkbox"
                :checked="procedure.suivi_procedure?.lettre_envoyee"
                disabled
              />
              Lettre d'information envoyée
            </label>
            <input
              v-if="procedure.suivi_procedure?.lettre_envoyee"
              type="date"
              class="fr-input fr-input--sm bo-input-date-sm"
              :value="procedure.suivi_procedure?.lettre_envoyee_date"
              disabled
            />
          </div>
          <!-- ar_recu, ar_statut & date -->
          <div class="bo-flex-space-between">
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input type="checkbox" :checked="procedure.suivi_procedure?.ar_recu" disabled />
              Accusé de réception (AR) reçu
            </label>
          </div>
          <div v-if="procedure.suivi_procedure?.ar_recu" class="bo-flex-gap-05 fr-ml-2w">
            <input
              type="text"
              class="fr-input fr-input--sm bo-input-text-sm"
              placeholder="Statut AR (ex: Distribué)"
              :value="procedure.suivi_procedure?.ar_statut"
              disabled
            />
            <input
              type="date"
              class="fr-input fr-input--sm bo-input-date-sm"
              :value="procedure.suivi_procedure?.ar_presentation_date"
              disabled
            />
          </div>
          <!-- copie_archives -->
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.copie_archives" disabled />
            Copie archivée dans le dossier
          </label>
        </div>
      </div>

      <!-- Étape 3 : Décision de poursuite -->
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
          Étape 3 : Décision de poursuite
        </h4>
        <p class="fr-text--xs fr-mb-0">
          <span
            v-if="!procedure.suivi_procedure?.decision_poursuite"
            class="fr-text-mention--grey fr-text--italic"
          >
            Aucune décision renseignée
          </span>
          <strong v-else>
            {{
              procedure.suivi_procedure?.decision_poursuite === 'sanction'
                ? 'Sanction administrative'
                : procedure.suivi_procedure?.decision_poursuite === 'abandon'
                  ? 'Abandon de la procédure'
                  : procedure.suivi_procedure?.decision_poursuite === 'recherche_adresse'
                    ? "Recherche d'adresse en cours"
                    : procedure.suivi_procedure?.decision_poursuite
            }}
          </strong>
        </p>
      </div>

      <!-- Étape 4 : Exécution de la décision -->
      <div
        :class="[
          'bo-step-section',
          procedure.suivi_procedure?.etape_en_cours >= 4
            ? 'bo-step-section--green'
            : 'bo-step-section--grey',
        ]"
      >
        <h4
          :class="[
            'fr-text--sm',
            'fr-text--bold',
            'fr-mb-1w',
            procedure.suivi_procedure?.etape_en_cours >= 4
              ? 'bo-step-title--green'
              : 'bo-step-title--grey',
          ]"
        >
          Étape 4 : Exécution de la décision
        </h4>

        <!-- Cas : Sanction -->
        <div
          v-if="procedure.suivi_procedure?.decision_poursuite === 'sanction'"
          class="bo-flex-col"
        >
          <div class="bo-flex-space-between">
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input type="checkbox" :checked="procedure.suivi_procedure?.montant_fixe" disabled />
              Montant de l'amende fixé
            </label>
            <input
              v-if="procedure.suivi_procedure?.montant_fixe"
              type="number"
              step="0.01"
              class="fr-input fr-input--sm bo-input-number-sm"
              placeholder="Montant €"
              :value="procedure.suivi_procedure?.montant_amende"
              disabled
            />
          </div>
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.arrete_redige" disabled />
            Arrêté de sanction rédigé
          </label>
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.titre_recette_emis"
              disabled
            />
            Titre de recette émis au Trésor Public
          </label>
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.notification_sanction_envoyee"
              disabled
            />
            Notification de sanction envoyée à l'auteur
          </label>
        </div>

        <!-- Cas : Abandon -->
        <div
          v-else-if="procedure.suivi_procedure?.decision_poursuite === 'abandon'"
          class="bo-flex-col"
        >
          <div>
            <label class="fr-label fr-text--xs fr-mb-1v" for="motif-abandon-select"
              >Motif d'abandon</label
            >
            <select
              id="motif-abandon-select"
              class="fr-select fr-select--sm bo-input-select-sm"
              :value="procedure.suivi_procedure?.motif_abandon"
              disabled
            >
              <option value="">-- Sélectionner le motif --</option>
              <option value="Auteur introuvable (NPAI)">Auteur introuvable (NPAI)</option>
              <option value="Dépôt sans gravité">Dépôt sans gravité / Mineur</option>
              <option value="Régularisation immédiate">Régularisation spontanée immédiate</option>
              <option value="Autre">Autre motif</option>
            </select>
          </div>
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.souhaite_notifier_abandon"
              disabled
            />
            Notifier l'abandon à l'auteur
          </label>
          <label
            v-if="procedure.suivi_procedure?.souhaite_notifier_abandon"
            class="fr-text--xs fr-mb-0 bo-flex-center-gap"
          >
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.notification_abandon_envoyee"
              disabled
            />
            Notification d'abandon envoyée
          </label>
        </div>

        <div v-else class="fr-text--xs fr-text-mention--grey">Pas de réponse</div>
      </div>

      <!-- Étape 5 : Clôture & Recouvrement -->
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
          Étape 5 : Clôture & Recouvrement
        </h4>
        <div class="bo-flex-col">
          <!-- Nettoyage fait -->
          <div class="bo-flex-space-between">
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input
                type="checkbox"
                :checked="procedure.suivi_procedure?.nettoyage_fait"
                disabled
              />
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
          <!-- Sanction-specific closing steps -->
          <div
            v-if="procedure.suivi_procedure?.decision_poursuite === 'sanction'"
            class="bo-flex-col"
          >
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input
                type="checkbox"
                :checked="procedure.suivi_procedure?.titre_recette_confirme"
                disabled
              />
              Titre de recette confirmé par le Trésor
            </label>
            <div class="bo-flex-space-between">
              <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
                <input
                  type="checkbox"
                  :checked="procedure.suivi_procedure?.montant_recouvre"
                  disabled
                />
                Amende recouvrée
              </label>
              <input
                v-if="procedure.suivi_procedure?.montant_recouvre"
                type="date"
                class="fr-input fr-input--sm bo-input-date-sm"
                :value="procedure.suivi_procedure?.date_recouvrement_effective"
                disabled
              />
            </div>
          </div>
          <!-- dossier_archive -->
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.dossier_archive" disabled />
            Dossier clos et archivé
          </label>
        </div>
      </div>
    </template>

    <!-- CASE: Auteur non identifié -->
    <template v-else>
      <!-- Étape 1 : Constitution du dossier -->
      <div class="bo-step-section bo-step-section--green">
        <h4 class="fr-text--sm fr-mb-1w bo-step-title--green fr-text--bold">
          Étape 1 : Constitution du dossier
        </h4>
        <div class="bo-flex-col">
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input
              type="checkbox"
              :checked="procedure.suivi_procedure?.preuves_fournies"
              disabled
            />
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

      <!-- Étape 2 : Identifier l'auteur -->
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

      <!-- Étape 3 : Recherche & Actions -->
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

      <!-- Étape 5 : Clôture de la procédure -->
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
          <!-- Nettoyage fait -->
          <div class="bo-flex-space-between">
            <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
              <input
                type="checkbox"
                :checked="procedure.suivi_procedure?.nettoyage_fait"
                disabled
              />
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
          <!-- dossier_archive -->
          <label class="fr-text--xs fr-mb-0 bo-flex-center-gap">
            <input type="checkbox" :checked="procedure.suivi_procedure?.dossier_archive" disabled />
            Dossier clos et archivé
          </label>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  procedure: any
}>()

const auteurIdentifie = computed(() => props.procedure?.auteur_identifie ?? false)
</script>
