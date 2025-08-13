<template>
  <div class="fr-container fr-grid-row fr-grid-row--center fr-mb-4w">
    <div class="fr-col-12 fr-col-md-8 fr-col-lg-6 fr-text--center fr-mt-4w">
      <h1 class="fr-h2">Commencer la procédure</h1>
      <p class="fr-text fr-mb-3w">
        Ce formulaire vous guide en <span class="fr-text--bold">5 étapes</span> pour signaler un dépôt sauvage.
      </p>
      <p class="fr-text fr-mb-3w">
        À la fin, vous pourrez récupérer des documents  générés et personnalisés pour vous permettre d'initier une procédure administrative et faciliter un éventuel dépôt de plainte.
      </p>
      <p class="fr-text fr-mb-3w">
        Des bulles d'aide s'affichent pour vous expliquer les informations à saisir.
        Survolez
        <button
          type="button"
          data-fr-tooltip
          class="fr-btn--icon fr-btn--tertiary-no-outline fr-icon-question-line"
          title="Passez la souris sur l’icône pour obtenir une aide sur les champs à remplir."
        >
          <span class="fr-sr-only">Passez la souris sur l’icône pour obtenir une aide sur les champs à remplir.</span>
        </button>
        pour les afficher.
      </p>
      <div class="fr-p-3w fr-mb-3w fr-background-alt--grey fr-border--grey fr-border fr-radius">
        <ul>
          <li>Temps estimé : 2 minutes</li>
          <li>Documents utiles : Ajoutez des photos si disponibles (facultatif)</li>
        </ul>
      </div>
      <div class="fr-grid-row fr-grid-row--center">
        <RouterLink to="/debuter-procedure/formulaire" class="fr-btn fr-mt-3w" @click="startProcedure">
          Démarrez la procédure
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useSignalementStore } from '@/stores/signalement'

const router = useRouter()
const store = useSignalementStore()

const startProcedure = () => {
  store.currentStep = 1
  router.push('/debuter-procedure/formulaire')
}
</script>
