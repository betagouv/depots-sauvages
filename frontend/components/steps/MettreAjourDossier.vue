<template>
  <div class="step-update-dn">
    <DsfrAlert type="success" title="Identification réussie" class="fr-mb-4w">
      <p class="fr-mb-1w">
        Vous avez identifié l'auteur. Vous pouvez maintenant
        <a :href="modifyUrl" target="_blank" @click.prevent="openExternalLink(modifyUrl)"
          >modifier le dossier sur Démarche numérique</a
        >
        pour y ajouter l'identité de l'auteur.
      </p>
    </DsfrAlert>
  </div>
</template>

<script setup lang="ts">
import { openExternalLink } from '../../utils/browser'

defineProps<{
  modifyUrl: string
}>()
</script>

<style scoped></style>
