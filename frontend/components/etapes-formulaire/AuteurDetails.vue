<template>
  <div>
    <template v-if="statutAuteur === 'entreprise'">
      <div class="fr-mb-4w">
        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': errors.nomEntreprise }"
        >
          <label class="fr-label" for="nom-entreprise">Nom de l'entreprise ou raison sociale *</label>
          <input
            id="nom-entreprise"
            type="text"
            v-model="formData.nomEntreprise"
            @input="clearError('nomEntreprise')"
            class="fr-input"
            aria-describedby="error-message-nomEntreprise"
          />
          <p
            v-if="errors.nomEntreprise"
            class="fr-error-text"
            id="error-message-nomEntreprise"
            aria-live="polite"
          >
            {{ errors.nomEntreprise }}
          </p>
        </div>

        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': errors.numeroSiret }"
        >
          <label class="fr-label" for="numero-siret">Numéro de SIRET</label>
          <span class="fr-hint-text">14 chiffres sans espaces</span>
          <input
            id="numero-siret"
            type="text"
            v-model="formData.numeroSiret"
            @input="clearError('numeroSiret')"
            class="fr-input"
            aria-describedby="error-message-numeroSiret"
            inputmode="numeric"
            @invalid.prevent
          />
          <p
            v-if="errors.numeroSiret"
            class="fr-error-text"
            id="error-message-numeroSiret"
            aria-live="polite"
          >
            {{ errors.numeroSiret }}
          </p>
        </div>
      </div>
    </template>

    <template v-else-if="statutAuteur === 'particulier'">
      <div class="fr-mb-3w">
        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': errors.prenomParticulier }"
        >
          <label class="fr-label" for="prenom-particulier">Prénom du particulier *</label>
          <input
            id="prenom-particulier"
            type="text"
            v-model="formData.prenomParticulier"
            @input="clearError('prenomParticulier')"
            class="fr-input"
            aria-describedby="error-message-prenomParticulier"
          />
          <p
            v-if="errors.prenomParticulier"
            class="fr-error-text"
            id="error-message-prenomParticulier"
            aria-live="polite"
          >
            {{ errors.prenomParticulier }}
          </p>
        </div>

        <div
          class="fr-col-12 fr-col-md-6 fr-input-group"
          :class="{ 'fr-input-group--error': errors.nomParticulier }"
        >
          <label class="fr-label" for="nom-particulier">Nom du particulier *</label>
          <input
            id="nom-particulier"
            type="text"
            v-model="formData.nomParticulier"
            @input="clearError('nomParticulier')"
            class="fr-input"
            aria-describedby="error-message-nomParticulier"
          />
          <p
            v-if="errors.nomParticulier"
            class="fr-error-text"
            id="error-message-nomParticulier"
            aria-live="polite"
          >
            {{ errors.nomParticulier }}
          </p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

interface FormData {
  nomEntreprise: string
  numeroSiret: string
  prenomParticulier: string
  nomParticulier: string
}

interface Errors {
  [key: string]: string
}

const props = defineProps<{
  statutAuteur: string
  formData: FormData
  errors: Errors
  clearError: (field: string) => void
}>()

const { statutAuteur, formData, errors, clearError } = toRefs(props)
</script>
