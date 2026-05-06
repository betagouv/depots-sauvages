<template>
  <div class="fr-container fr-py-6w">
    <h1 class="fr-h1 fr-mb-2w">Création d'une constatation</h1>

    <div class="fr-highlight fr-mb-6w">
      <p class="fr-text--sm">
        <strong>Les champs suivis d'un astérisque (*) sont obligatoires.</strong><br />
        Votre dossier est enregistré automatiquement après chaque modification. Vous pouvez à tout
        moment fermer la fenêtre et reprendre plus tard là où vous en étiez.
      </p>
    </div>

    <form @submit.prevent="submitForm">
      <DsfrAlert
        v-if="Object.keys(store.errors).length > 0"
        type="error"
        title="Le formulaire contient des erreurs"
        class="fr-mb-4w"
      >
        Veuillez corriger les champs indiquant une erreur avant de soumettre le formulaire.
      </DsfrAlert>

      <ConstatationForm />

      <div class="fr-mt-6w fr-mb-4w">
        <button type="submit" class="fr-btn fr-btn--lg">Enregistrer la constatation</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import ConstatationForm from '@/components/forms/constatation/ConstatationForm.vue'
import { useConstatationStore } from '@/stores/constatation'
import { DsfrAlert } from '@gouvminint/vue-dsfr'
import { useRouter } from 'vue-router'

const store = useConstatationStore()
const router = useRouter()

const submitForm = async () => {
  if (!store.validate()) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  try {
    await store.saveFormData()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}
</script>
