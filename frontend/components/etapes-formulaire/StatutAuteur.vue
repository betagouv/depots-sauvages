<template>
  <fieldset
    v-if="store.formData.auteurIdentifie"
    class="fr-form-group fr-fieldset--no-border fr-mb-3w"
    :class="{ 'fr-form-group--error': showStatutAuteurError }"
  >
    <legend
      class="fr-text--regular"
      :class="{ 'fr-pb-2w': !showStatutAuteurError }"
    >
      S'agit-il d'une entreprise ou d'un particulier ? *
    </legend>
    <p
      v-if="showStatutAuteurError"
      class="fr-error-text fr-my-2w"
      tabindex="-1"
      ref="statutAuteurErrorMessage"
      id="error-message-statutAuteur"
      aria-live="polite"
    >
      {{ store.errors.statutAuteur }}
    </p>
    <div class="fr-radio-group fr-my-1w fr-py-1w">
      <input
        type="radio"
        id="statutAuteur-entreprise"
        name="statut-auteur"
        value="entreprise"
        v-model="store.formData.statutAuteur"
        @change="clearError('statutAuteur')"
        aria-describedby="error-message-statutAuteur"
      />
      <label class="fr-label" for="statutAuteur-entreprise">Entreprise</label>
    </div>

    <div class="fr-radio-group fr-my-1w">
      <input
        type="radio"
        id="statutAuteur-particulier"
        name="statut-auteur"
        value="particulier"
        v-model="store.formData.statutAuteur"
        @change="clearError('statutAuteur')"
        aria-describedby="error-message-statutAuteur"
      />
      <label class="fr-label" for="statutAuteur-particulier">Particulier</label>
    </div>
  </fieldset>
</template>
<script>
export default {
  name: 'jaja',
}
</script>
<style scoped>

.fr-fieldset--no-border {
  border: none;
  margin: 0;
  padding: 0;
  color: #161616 !important;
}

</style>