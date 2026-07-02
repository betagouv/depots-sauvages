<template>
  <div class="premium-box fr-p-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
    <h3 class="fr-h6 fr-mb-3w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
      <span class="fr-icon-survey-line fr-mr-1w"></span> Actions du Suivi
    </h3>

    <!-- ÉTAPE 1: Constitution du dossier -->
    <div class="fr-mb-3w" style="border-left: 2px solid #22C55E; padding-left: 1rem">
      <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700; color: #15803D">Étape 1 : Constitution du dossier</h4>
      <div style="display: flex; flex-direction: column; gap: 0.5rem">
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.preuves_fournies" disabled />
          Éléments de preuve joints
        </label>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.constatation_signee" disabled />
          Rapport de constatation signé
        </label>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.lettre_signe" disabled />
          Lettre d'information signée
        </label>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.identification_reussie === true" disabled />
          Identification auteur : <strong>{{ getAuteurIdentifieText(procedure.suivi_procedure?.identification_reussie) }}</strong>
        </label>
      </div>
    </div>

    <!-- ÉTAPE 2: Notification -->
    <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (procedure.suivi_procedure?.etape_en_cours >= 2 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
      <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: procedure.suivi_procedure?.etape_en_cours >= 2 ? '#15803D' : '#4B5563' }">Étape 2 : Notification à l'auteur</h4>
      <div style="display: flex; flex-direction: column; gap: 0.5rem">
        <!-- lettre_envoyee & date -->
        <div style="display: flex; align-items: center; justify-content: space-between">
          <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
            <input type="checkbox" :checked="procedure.suivi_procedure?.lettre_envoyee" disabled />
            Lettre d'information envoyée
          </label>
          <input
            v-if="procedure.suivi_procedure?.lettre_envoyee"
            type="date"
            class="fr-input fr-input--sm"
            style="width: 120px; padding: 0.2rem"
            :value="procedure.suivi_procedure?.lettre_envoyee_date"
            disabled
          />
        </div>
        <!-- ar_recu, ar_statut & date -->
        <div style="display: flex; align-items: center; justify-content: space-between">
          <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
            <input type="checkbox" :checked="procedure.suivi_procedure?.ar_recu" disabled />
            Accusé de réception (AR) reçu
          </label>
        </div>
        <div v-if="procedure.suivi_procedure?.ar_recu" style="display: flex; gap: 0.5rem; margin-left: 1.25rem">
          <input
            type="text"
            class="fr-input fr-input--sm"
            placeholder="Statut AR (ex: Distribué)"
            :value="procedure.suivi_procedure?.ar_statut"
            disabled
            style="flex: 1; padding: 0.2rem"
          />
          <input
            type="date"
            class="fr-input fr-input--sm"
            :value="procedure.suivi_procedure?.ar_presentation_date"
            disabled
            style="width: 120px; padding: 0.2rem"
          />
        </div>
        <!-- copie_archives -->
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.copie_archives" disabled />
          Copie archivée dans le dossier
        </label>
      </div>
    </div>

    <!-- ÉTAPE 3: Décision de poursuite -->
    <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (procedure.suivi_procedure?.etape_en_cours >= 3 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
      <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: procedure.suivi_procedure?.etape_en_cours >= 3 ? '#15803D' : '#4B5563' }">Étape 3 : Décision de poursuite</h4>
      <p class="fr-text--xs fr-mb-0">
        <span v-if="!procedure.suivi_procedure?.decision_poursuite" style="color: var(--text-mention-grey); font-style: italic">
          Aucune décision renseignée
        </span>
        <strong v-else>
          {{ 
            procedure.suivi_procedure?.decision_poursuite === 'sanction' ? 'Sanction administrative' :
            procedure.suivi_procedure?.decision_poursuite === 'abandon' ? 'Abandon de la procédure' :
            procedure.suivi_procedure?.decision_poursuite === 'recherche_adresse' ? "Recherche d'adresse en cours" :
            procedure.suivi_procedure?.decision_poursuite
          }}
        </strong>
      </p>
    </div>

    <!-- ÉTAPE 4: Exécution de la décision -->
    <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (procedure.suivi_procedure?.etape_en_cours >= 4 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
      <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: procedure.suivi_procedure?.etape_en_cours >= 4 ? '#15803D' : '#4B5563' }">Étape 4 : Exécution de la décision</h4>
      
      <!-- Cas : Sanction -->
      <div v-if="procedure.suivi_procedure?.decision_poursuite === 'sanction'" style="display: flex; flex-direction: column; gap: 0.5rem">
        <div style="display: flex; align-items: center; justify-content: space-between">
          <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
            <input type="checkbox" :checked="procedure.suivi_procedure?.montant_fixe" disabled />
            Montant de l'amende fixé
          </label>
          <input
            v-if="procedure.suivi_procedure?.montant_fixe"
            type="number"
            step="0.01"
            class="fr-input fr-input--sm"
            style="width: 100px; padding: 0.2rem"
            placeholder="Montant €"
            :value="procedure.suivi_procedure?.montant_amende"
            disabled
          />
        </div>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.arrete_redige" disabled />
          Arrêté de sanction rédigé
        </label>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.titre_recette_emis" disabled />
          Titre de recette émis au Trésor Public
        </label>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.notification_sanction_envoyee" disabled />
          Notification de sanction envoyée à l'auteur
        </label>
      </div>

      <!-- Cas : Abandon -->
      <div v-else-if="procedure.suivi_procedure?.decision_poursuite === 'abandon'" style="display: flex; flex-direction: column; gap: 0.5rem">
        <div>
          <label class="fr-label fr-text--xs fr-mb-1v" for="motif-abandon-select">Motif d'abandon</label>
          <select
            id="motif-abandon-select"
            class="fr-select fr-select--sm"
            :value="procedure.suivi_procedure?.motif_abandon"
            disabled
            style="padding: 0.25rem"
          >
            <option value="">-- Sélectionner le motif --</option>
            <option value="Auteur introuvable (NPAI)">Auteur introuvable (NPAI)</option>
            <option value="Dépôt sans gravité">Dépôt sans gravité / Mineur</option>
            <option value="Régularisation immédiate">Régularisation spontanée immédiate</option>
            <option value="Autre">Autre motif</option>
          </select>
        </div>
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.souhaite_notifier_abandon" disabled />
          Notifier l'abandon à l'auteur
        </label>
        <label v-if="procedure.suivi_procedure?.souhaite_notifier_abandon" class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.notification_abandon_envoyee" disabled />
          Notification d'abandon envoyée
        </label>
      </div>

      <div v-else class="fr-text--xs" style="color: var(--text-mention-grey)">
        Pas de réponse
      </div>
    </div>

    <!-- ÉTAPE 5: Clôture & Recouvrement -->
    <div class="fr-mb-0" :style="{ borderLeft: '2px solid ' + (procedure.suivi_procedure?.etape_en_cours >= 5 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
      <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: procedure.suivi_procedure?.etape_en_cours >= 5 ? '#15803D' : '#4B5563' }">Étape 5 : Clôture & Recouvrement</h4>
      <div style="display: flex; flex-direction: column; gap: 0.5rem">
        <!-- Nettoyage fait -->
        <div style="display: flex; align-items: center; justify-content: space-between">
          <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
            <input type="checkbox" :checked="procedure.suivi_procedure?.nettoyage_fait" disabled />
            Nettoyage du dépôt effectué
          </label>
          <input
            v-if="procedure.suivi_procedure?.nettoyage_fait"
            type="text"
            class="fr-input fr-input--sm"
            style="width: 120px; padding: 0.2rem"
            placeholder="Par (ex: Auteur)"
            :value="procedure.suivi_procedure?.nettoyage_par"
            disabled
          />
        </div>
        <!-- Sanction-specific closing steps -->
        <div v-if="procedure.suivi_procedure?.decision_poursuite === 'sanction'" style="display: flex; flex-direction: column; gap: 0.5rem">
          <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
            <input type="checkbox" :checked="procedure.suivi_procedure?.titre_recette_confirme" disabled />
            Titre de recette confirmed par le Trésor
          </label>
          <div style="display: flex; align-items: center; justify-content: space-between">
            <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
              <input type="checkbox" :checked="procedure.suivi_procedure?.montant_recouvre" disabled />
              Amende recouvrée
            </label>
            <input
              v-if="procedure.suivi_procedure?.montant_recouvre"
              type="date"
              class="fr-input fr-input--sm"
              style="width: 120px; padding: 0.2rem"
              :value="procedure.suivi_procedure?.date_recouvrement_effective"
              disabled
            />
          </div>
        </div>
        <!-- dossier_archive -->
        <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
          <input type="checkbox" :checked="procedure.suivi_procedure?.dossier_archive" disabled />
          Dossier clos et archivé
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getAuteurIdentifieText } from '@/utils/backoffice'

defineProps<{
  procedure: any
}>()
</script>
